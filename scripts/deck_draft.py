"""Parse deck/outline.md and the page drafts in deck/drafts/pNN.md."""
import re
from dataclasses import dataclass, field
from pathlib import Path

BLOCKS = ("重點", "內文", "圖", "圖內文字", "互動", "名詞")
MAP_NODES = ("影像", "低層", "中層", "高層", "類別機率")
ALL_NODES = "全部"
MAP_SEPARATOR = " → "
EVIDENCE_SEPARATOR = "｜"
SECTION_RANGES = (
    ("開始之前", 1, 1),
    ("CNN 怎麼看圖", 2, 5),
    ("一個神經元", 6, 9),
    ("一張圖", 10, 11),
    ("一整層", 12, 14),
    ("能信多少", 15, 15),
)
DRAFT_NAME_RE = re.compile(r"^p(\d{2})\.md$")
OUTLINE_PAGE_RE = re.compile(r"^## 第 (\d+) 頁：(.+?)\s*$")
BACKTICK_RE = re.compile(r"`([^`]+)`")
FIELD_RE = re.compile(r"^(?P<indent>- |  )(?P<key>白話|依據|檔案|裁切)：(?P<value>.*)$")
META_RE = re.compile(r"^- (?P<key>區段|地圖|圖見原文)：(?P<value>.+)$")


class DraftError(ValueError):
    """A draft or outline does not follow the format in deck/workflow.md."""


@dataclass
class Evidence:
    page: str
    sentence: str


@dataclass
class Item:
    block: str
    text: str = ""
    evidence: list = field(default_factory=list)
    file: str = ""
    crop: tuple = ()


@dataclass
class Draft:
    number: int
    path: Path
    title: str = ""
    section: str = ""
    map_nodes: list = field(default_factory=list)
    figure_links: list = field(default_factory=list)
    items: list = field(default_factory=list)

    def block(self, name):
        return [item for item in self.items if item.block == name]


@dataclass
class OutlinePage:
    number: int
    title: str
    wiki_pages: list = field(default_factory=list)
    figures: list = field(default_factory=list)
    map_nodes: list = field(default_factory=list)


def section_for(number):
    for name, first, last in SECTION_RANGES:
        if first <= number <= last:
            return name
    raise DraftError(f"page {number} is outside the deck")


def parse_map(value):
    value = value.strip()
    if value == ALL_NODES:
        return list(MAP_NODES)
    nodes = [node.strip() for node in value.split(MAP_SEPARATOR)]
    unknown = [node for node in nodes if node not in MAP_NODES]
    if unknown:
        raise DraftError(f"unknown map position: {unknown}")
    if len(nodes) == 1:
        return nodes
    start, end = MAP_NODES.index(nodes[0]), MAP_NODES.index(nodes[-1])
    return list(MAP_NODES[start:end + 1])


def _parse_crop(value, where):
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4 or not all(part.isdigit() for part in parts):
        raise DraftError(f"{where}: crop must be x,y,width,height")
    return tuple(int(part) for part in parts)


def _parse_evidence(value, where):
    if EVIDENCE_SEPARATOR not in value:
        raise DraftError(f"{where}: evidence needs page{EVIDENCE_SEPARATOR}sentence")
    page, sentence = value.split(EVIDENCE_SEPARATOR, 1)
    return Evidence(page.strip(), sentence.strip())


def _apply_field(item, key, value, where):
    if key == "白話":
        item.text = value.strip()
    elif key == "依據":
        item.evidence.append(_parse_evidence(value, where))
    elif key == "檔案":
        if item.block != "圖":
            raise DraftError(f"{where}: only the 圖 block can name a file")
        item.file = value.strip()
    else:
        item.crop = _parse_crop(value, where)


def parse_draft(path):
    path = Path(path)
    match = DRAFT_NAME_RE.match(path.name)
    if not match:
        raise DraftError(f"{path.name}: draft files are named pNN.md")
    draft = Draft(number=int(match.group(1)), path=path)
    block, item = None, None
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        where = f"{path.name}:{line_number}"
        if not raw.strip():
            continue
        if raw.startswith("# "):
            draft.title = raw[2:].strip()
        elif raw.startswith("## "):
            block = raw[3:].strip()
            item = None
            if block not in BLOCKS:
                raise DraftError(f"{where}: unknown block {block!r}")
        elif block is None:
            meta = META_RE.match(raw)
            if not meta:
                raise DraftError(f"{where}: unexpected line before the first block")
            if meta["key"] == "區段":
                draft.section = meta["value"].strip()
            elif meta["key"] == "地圖":
                draft.map_nodes = parse_map(meta["value"])
            else:
                draft.figure_links.append(meta["value"].strip())
        else:
            parsed = FIELD_RE.match(raw)
            if not parsed:
                raise DraftError(f"{where}: unexpected line in block {block}")
            if parsed["indent"] == "- ":
                item = Item(block=block)
                draft.items.append(item)
            elif item is None:
                raise DraftError(f"{where}: field outside an item")
            _apply_field(item, parsed["key"], parsed["value"], where)
    if not draft.title:
        raise DraftError(f"{path.name}: missing title")
    for item in draft.items:
        if not item.text:
            raise DraftError(f"{path.name}: item in {item.block} has no text")
    return draft


def load_drafts(root):
    drafts_dir = Path(root) / "deck" / "drafts"
    paths = sorted(p for p in drafts_dir.glob("p*.md") if DRAFT_NAME_RE.match(p.name))
    return [parse_draft(path) for path in paths]


def parse_outline(path):
    pages, current = {}, None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        heading = OUTLINE_PAGE_RE.match(raw)
        if heading:
            current = OutlinePage(number=int(heading.group(1)), title=heading.group(2))
            pages[current.number] = current
        elif current is not None and raw.startswith("- Wiki："):
            current.wiki_pages = BACKTICK_RE.findall(raw)
        elif current is not None and raw.startswith("- 圖："):
            current.figures = [p for p in BACKTICK_RE.findall(raw) if p.startswith("raw/")]
        elif current is not None and raw.startswith("- 地圖位置："):
            current.map_nodes = parse_map(raw.split("：", 1)[1])
    return pages
