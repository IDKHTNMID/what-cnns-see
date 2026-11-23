"""Check every deck draft sentence against the Wiki sentence it cites.

Usage:
  python scripts/check_deck_evidence.py --label "round 1" [--page 6]
Appends the result to deck/reports/evidence.md. Exit code is 1 on any problem.
"""
import argparse
import datetime
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck_draft  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPORT = Path("deck") / "reports" / "evidence.md"
REPORT_HEADER = "# 依據檢查紀錄\n\n每次執行 `scripts/check_deck_evidence.py` 的結果，只往後加。\n\n"
MIN_EVIDENCE_CHARS = 6
WORK_TERMS = ("帶走", "依據", "段落", "地圖位置", "逐頁稿", "節點", "大綱", "白話", "工作流", "workflow", "關卡")
HEDGES = ("可能", "似乎", "不一定", "作者說", "作者認為", "大致", "不完全", "很難", "但", "只", "不是", "看起來", "通常", "未必", "還沒")
CITATION_RE = re.compile(r"（[^（）]*§[^（）]*）")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
EMPHASIS_RE = re.compile(r"\*\*|`")
SPACE_RE = re.compile(r"\s+")
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
ALIAS_NOTE_RE = re.compile(r"（[^）]*）|\([^)]*\)")
ALIAS_SPLIT_RE = re.compile(r"[、,，/／]")


@dataclass
class Result:
    problems: list = field(default_factory=list)
    review: list = field(default_factory=list)
    hedges: list = field(default_factory=list)


def plain_wiki_text(text):
    """Wiki lines without citations, link syntax and emphasis, ready for exact matching."""
    lines = []
    for line in text.splitlines():
        line = CITATION_RE.sub("", line)
        line = IMAGE_RE.sub(r"\1", line)
        line = LINK_RE.sub(r"\1", line)
        line = EMPHASIS_RE.sub("", line)
        line = SPACE_RE.sub(" ", line).strip()
        if line:
            lines.append(line)
    return lines


def numbers_in(text):
    spaced = re.sub(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: " " + m.group(1).translate(SUPERSCRIPTS) + " ", text)
    return {token.replace(",", "") for token in NUMBER_RE.findall(spaced)}


def load_terms(glossary_path):
    """Return (main terms, {alias: main term}) from the glossary table."""
    mains, aliases = [], {}
    for line in Path(glossary_path).read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("主名詞", "") or set(cells[0]) <= {"-"}:
            continue
        main = cells[0]
        mains.append(main)
        for alias in ALIAS_SPLIT_RE.split(ALIAS_NOTE_RE.sub("", cells[2])):
            alias = alias.strip()
            if alias and alias not in ("—", "-") and alias != main:
                aliases[alias] = main
    return mains, aliases


def alias_hits(text, mains, aliases):
    for main in sorted(mains, key=len, reverse=True):
        text = text.replace(main, "\0")
    return sorted((alias, main) for alias, main in aliases.items() if alias in text)


class _WikiCache:
    def __init__(self, root):
        self.wiki_dir = root / "wiki"
        self._lines, self._raw = {}, {}

    def exists(self, page):
        return (self.wiki_dir / page).is_file()

    def raw(self, page):
        if page not in self._raw:
            self._raw[page] = (self.wiki_dir / page).read_text(encoding="utf-8")
        return self._raw[page]

    def full_line(self, page, sentence):
        """The plain Wiki line holding the sentence, or None."""
        if page not in self._lines:
            self._lines[page] = plain_wiki_text(self.raw(page))
        wanted = SPACE_RE.sub(" ", sentence).strip()
        return next((line for line in self._lines[page] if wanted in line), None)

    def has_sentence(self, page, sentence):
        return self.full_line(page, sentence) is not None


def _check_item(item, draft, outline_page, wiki, terms):
    where = f"p{draft.number:02d} {item.block}「{item.text[:24]}」"
    problems = []
    if not item.evidence:
        problems.append(f"{where}: no evidence")
    for evidence in item.evidence:
        if evidence.page not in outline_page.wiki_pages:
            problems.append(f"{where}: {evidence.page} is not listed in the outline for this page")
        if not wiki.exists(evidence.page):
            problems.append(f"{where}: wiki page {evidence.page} does not exist")
        elif len(evidence.sentence) < MIN_EVIDENCE_CHARS:
            problems.append(f"{where}: evidence is too short: {evidence.sentence}")
        elif not wiki.has_sentence(evidence.page, evidence.sentence):
            problems.append(f"{where}: sentence not found in {evidence.page}: {evidence.sentence[:40]}")
    cited = " ".join(evidence.sentence for evidence in item.evidence)
    for number in sorted(numbers_in(item.text) - numbers_in(cited)):
        problems.append(f"{where}: number {number} is not in the evidence")
    for alias, main in alias_hits(item.text, *terms):
        problems.append(f"{where}: alias {alias} used instead of {main}")
    return problems


def _check_figure(item, draft, outline_page, wiki, root):
    where = f"p{draft.number:02d} figure {item.file}"
    problems = []
    if not (root / item.file).is_file():
        problems.append(f"{where}: figure file does not exist")
    if item.file not in outline_page.figures:
        problems.append(f"{where}: figure is not listed in the outline")
    used = any(wiki.exists(page) and item.file in wiki.raw(page) for page in outline_page.wiki_pages)
    if not used:
        problems.append(f"{where}: figure not used by any Wiki page listed for this page")
    return problems


def _check_draft(draft, outline, wiki, terms, root):
    page = outline.get(draft.number)
    if page is None:
        return [f"p{draft.number:02d}: page is not in the outline"]
    problems = []
    if draft.title != page.title:
        problems.append(f"p{draft.number:02d}: title differs from the outline")
    if draft.map_nodes != page.map_nodes:
        problems.append(f"p{draft.number:02d}: map position differs from the outline")
    if draft.section != deck_draft.section_for(draft.number):
        problems.append(f"p{draft.number:02d}: section should be {deck_draft.section_for(draft.number)}")
    if len(draft.block("重點")) != 1:
        problems.append(f"p{draft.number:02d}: needs exactly one 重點")
    for item in draft.items:
        problems += _check_item(item, draft, page, wiki, terms)
        if item.block == "圖":
            problems += _check_figure(item, draft, page, wiki, root)
    return problems


def _scan_work_terms(draft):
    found = []
    for text in [draft.title] + [item.text for item in draft.items]:
        for term in WORK_TERMS:
            if term in text:
                found.append(f"p{draft.number:02d} 含「{term}」：{text}")
    return found


def _scan_cut_hedges(draft, wiki):
    """List hedges that sit on the cited Wiki line but outside the quoted part and the slide text."""
    found = []
    for item in draft.items:
        for evidence in item.evidence:
            if not wiki.exists(evidence.page):
                continue
            line = wiki.full_line(evidence.page, evidence.sentence)
            if line is None:
                continue
            before, _, after = line.partition(SPACE_RE.sub(" ", evidence.sentence).strip())
            outside = before + " " + after
            words = [word for word in HEDGES if word in outside and word not in item.text]
            if words:
                found.append(f"p{draft.number:02d} {item.block}［{'、'.join(words)}］{item.text}｜整行：{line}")
    return found


def check_deck(root=ROOT, only=None):
    root = Path(root)
    result = Result()
    outline = deck_draft.parse_outline(root / "deck" / "outline.md")
    terms = load_terms(root / "wiki" / "glossary.md")
    wiki = _WikiCache(root)
    for draft in deck_draft.load_drafts(root):
        if only is not None and draft.number != only:
            continue
        result.problems += _check_draft(draft, outline, wiki, terms, root)
        result.review += _scan_work_terms(draft)
        result.hedges += _scan_cut_hedges(draft, wiki)
    return result


def write_report(root, label, result):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    verdict = "PASS" if not result.problems else f"FAIL ({len(result.problems)})"
    lines = [f"## [{stamp}] {label} | {verdict}", ""]
    lines += [f"- `{problem}`" for problem in result.problems]
    if result.review:
        lines += ["", "工作用語掃描（逐筆人工看過）：", ""] + [f"- {entry}" for entry in result.review]
    if result.hedges:
        lines += ["", "保留語掃描（依據外有保留語，逐筆人工看過）：", ""] + [f"- {entry}" for entry in result.hedges]
    text ="\n".join(lines) + "\n\n"
    path = Path(root) / REPORT
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(REPORT_HEADER, encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)
    return text


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", required=True)
    parser.add_argument("--page", type=int)
    args = parser.parse_args()
    result = check_deck(ROOT, args.page)
    print(write_report(ROOT, args.label, result), end="")
    return 1 if result.problems else 0


if __name__ == "__main__":
    sys.exit(main())
