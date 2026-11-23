"""Build deck/index.html from the checked page drafts, the template and the layouts.

Usage:
  python scripts/build_deck.py [--wiki-base https://github.com/<owner>/<repo>/blob/main/wiki/]

The build never changes a word. Layout files hold markup and placeholders only, and every
draft item must be placed exactly once.
"""
import argparse
import html
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck_draft  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = Path("deck") / "template.html"
LAYOUTS = Path("deck") / "layouts"
OUTPUT = Path("deck") / "index.html"
SOURCES = Path("raw") / "SOURCES.md"
WIKI = Path("wiki")
SLIDES_MARK = "<!--SLIDES-->"
ASSET_PREFIX = "../"

KEY_POINT_LABEL = "重點"
SOURCE_LABEL = "資料來源："
FIGURE_LABEL = "圖："
FIGURE_LINK_LABEL = "圖見原文"
CROPPED_NOTE = "，經裁切"
SKIP_HINT = "學過 CNN 的人可以從第 6 頁開始"
SKIP_TO_PAGE = 6
PLACED_BLOCKS = ("內文", "圖", "圖內文字", "互動")
TERM_BLOCK = "名詞"
TERM_LABEL = "名詞"
TERM_SEPARATOR = "："
MAX_TERMS = 3
WIDE_ASPECT = 2.0
MANY_FIGURES = 3

PLACEHOLDER_RE = re.compile(r"\{\{([^{}]+)\}\}")
TAG_RE = re.compile(r"<[^>]*>")
SVG_SIZE_RE = re.compile(r'<svg[^>]*?\swidth="([\d.]+)[a-z]*"[^>]*?\sheight="([\d.]+)[a-z]*"', re.S)
FULL_WIDTH_NOTE_RE = re.compile(r"（.*?）")

PAGER = (
    '<div class="pager">'
    '<button type="button" data-go="-1" aria-label="上一頁"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>'
    '<button type="button" data-go="1" aria-label="下一頁"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>'
    "</div>"
)


class BuildError(ValueError):
    """The drafts, template or layouts cannot be built without changing a word."""


@dataclass
class Source:
    slug: str
    title: str
    authors: str
    year: str
    url: str
    licence: str


@dataclass
class Slide:
    number: int
    html: str
    texts: list = field(default_factory=list)  # every text node outside the source line
    source: str = ""


def e(text):
    return html.escape(text, quote=True)


def load_sources(path):
    sources = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 7 and cells[0] != "Slug" and set(cells[0]) != {"-"}:
            sources[cells[0]] = Source(*cells[:6])
    return sources


def figure_slug(file):
    parts = PurePosixPath(file).parts
    if len(parts) < 3 or parts[0] != "raw":
        raise BuildError(f"figure path is not under raw/<slug>/: {file}")
    return parts[2] if parts[1] == "screenshots" else parts[1]


def short_authors(authors):
    names = [name.strip().split()[-1] for name in authors.split(",")]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} & {names[1]}"
    return f"{names[0]} et al."


def image_size(path):
    path = Path(path)
    if path.suffix.lower() == ".svg":
        match = SVG_SIZE_RE.search(path.read_text(encoding="utf-8", errors="replace"))
        if not match:
            raise BuildError(f"{path}: svg has no width and height")
        return float(match.group(1)), float(match.group(2))
    with Image.open(path) as image:
        return image.size


def figure_aspect(item, root):
    if item.crop:
        return item.crop[2] / item.crop[3]
    width, height = image_size(root / item.file)
    return width / height


def figure_html(item, root, where):
    src = e(ASSET_PREFIX + item.file)
    alt = e(item.text)
    if item.crop:
        x, y, width, height = item.crop
        natural_w, natural_h = image_size(root / item.file)
        if x + width > natural_w or y + height > natural_h:
            raise BuildError(f"{where}: crop {item.crop} is outside {item.file} ({natural_w}x{natural_h})")
        media = (
            f'<svg class="crop" viewBox="0 0 {width} {height}" role="img" aria-label="{alt}" '
            f'style="aspect-ratio:{width}/{height}">'
            f'<svg width="{width}" height="{height}" viewBox="{x} {y} {width} {height}">'
            f'<image href="{src}" width="{natural_w}" height="{natural_h}"/></svg></svg>'
        )
    else:
        media = f'<img src="{src}" alt="{alt}">'
    return f'<figure class="fig">{media}<figcaption>{alt}</figcaption></figure>'


def _horizontal_map(texts):
    texts.extend(deck_draft.MAP_NODES)
    return '<ol class="flow">' + "".join(f"<li>{e(node)}</li>" for node in deck_draft.MAP_NODES) + "</ol>"


def _section_list(texts):
    items = []
    for name, first, _ in deck_draft.SECTION_RANGES[1:]:
        texts.append(name)
        items.append(f'<li><a href="#{first}">{e(name)}</a></li>')
    return '<ol class="sections">' + "".join(items) + "</ol>"


def _skip_hint(texts):
    texts.append(SKIP_HINT)
    return f'<a class="skip" href="#{SKIP_TO_PAGE}">{e(SKIP_HINT)}</a>'


SYSTEM_PLACEHOLDERS = {"地圖": _horizontal_map, "區段列表": _section_list, "跳讀": _skip_hint}


def _place_item(item, mode, root, where, texts):
    if item.block == "圖":
        if mode:
            raise BuildError(f"{where}: figures take no mode")
        texts.append(item.text)
        return figure_html(item, root, where)
    if mode == "cells":
        cells = item.text.split()
        texts.extend(cells)
        return "".join(f'<span class="cell" data-v="{e(cell)}">{e(cell)}</span>' for cell in cells)
    if mode:
        raise BuildError(f"{where}: unknown mode {mode}")
    texts.append(item.text)
    return e(item.text)


def fill_layout(fragment, draft, root, texts):
    where = f"p{draft.number:02d} layout"
    leftover = TAG_RE.sub("", PLACEHOLDER_RE.sub("", fragment)).strip()
    if leftover:
        raise BuildError(f"{where}: layouts cannot hold words: {leftover[:30]}")
    used = Counter()

    def replace(match):
        key, _, mode = match.group(1).strip().partition("|")
        if key in SYSTEM_PLACEHOLDERS:
            return SYSTEM_PLACEHOLDERS[key](texts)
        block, _, index = key.partition(".")
        items = draft.block(block) if block in PLACED_BLOCKS else []
        if not index.isdigit() or not 1 <= int(index) <= len(items):
            raise BuildError(f"{where}: unknown placeholder {match.group(0)}")
        used[(block, int(index))] += 1
        return _place_item(items[int(index) - 1], mode, root, where, texts)

    filled = PLACEHOLDER_RE.sub(replace, fragment)
    for block in PLACED_BLOCKS:
        for index in range(1, len(draft.block(block)) + 1):
            if used[(block, index)] != 1:
                raise BuildError(f"{where}: {block}.{index} used {used[(block, index)]} times")
    return filled


def auto_layout(draft, root):
    if draft.block("圖內文字") or draft.block("互動"):
        raise BuildError(f"p{draft.number:02d}: labels and interaction need a layout file")
    figures, notes = draft.block("圖"), draft.block("內文")
    figure_part = "".join(f"{{{{圖.{i}}}}}" for i in range(1, len(figures) + 1))
    note_part = "".join(f"<li>{{{{內文.{i}}}}}</li>" for i in range(1, len(notes) + 1))
    stacked = len(figures) >= MANY_FIGURES or any(figure_aspect(f, root) >= WIDE_ASPECT for f in figures)
    kind = "stack" if stacked else "side"
    return (
        f'<div class="content {kind}"><div class="figs figs-{len(figures)}">{figure_part}</div>'
        f'<ol class="how how-{len(notes)}">{note_part}</ol></div>'
    )


def _wiki_title(root, page):
    for line in (root / WIKI / page).read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return FULL_WIDTH_NOTE_RE.sub("", line[2:]).strip()
    raise BuildError(f"wiki page {page} has no title")


def source_line(draft, root, sources, wiki_base):
    """Return (html, plain text) of the generated source line."""
    pages = list(dict.fromkeys(ev.page for item in draft.items for ev in item.evidence))
    wiki_html, wiki_text = [], []
    for page in pages:
        title = _wiki_title(root, page)
        wiki_text.append(f"〈{title}〉")
        linked = f'<a href="{e(wiki_base + page)}">{e(title)}</a>' if wiki_base else e(title)
        wiki_html.append(f"〈{linked}〉")
    parts_html = [SOURCE_LABEL + "Wiki" + "".join(wiki_html)]
    parts_text = [SOURCE_LABEL + "Wiki" + "".join(wiki_text)]

    credits = {}
    for item in draft.block("圖"):
        slug = figure_slug(item.file)
        credits[slug] = credits.get(slug, False) or bool(item.crop)
    if credits:
        credit_html, credit_text = [], []
        for slug, cropped in credits.items():
            if slug not in sources:
                raise BuildError(f"p{draft.number:02d}: {slug} is not in raw/SOURCES.md")
            source = sources[slug]
            who = short_authors(source.authors)
            tail = f" ({source.year}), {source.licence}" + (CROPPED_NOTE if cropped else "")
            credit_html.append(f'{e(who)}, <a href="{e(source.url)}">{e(source.title)}</a>{e(tail)}')
            credit_text.append(f"{who}, {source.title}{tail}")
        parts_html.append(FIGURE_LABEL + "；".join(credit_html))
        parts_text.append(FIGURE_LABEL + "；".join(credit_text))
    for link in draft.figure_links:
        parts_html.append(f'<a href="{e(link)}">{FIGURE_LINK_LABEL}</a>')
        parts_text.append(FIGURE_LINK_LABEL)
    return "｜".join(parts_html), "｜".join(parts_text)


def term_strip(draft, texts):
    """Return the glossary strip for this page; each item is written as term：definition."""
    items = draft.block(TERM_BLOCK)
    if not items:
        return ""
    if len(items) > MAX_TERMS:
        raise BuildError(f"p{draft.number:02d}: at most {MAX_TERMS} terms per page, found {len(items)}")
    texts.append(TERM_LABEL)
    entries = []
    for item in items:
        term, separator, definition = item.text.partition(TERM_SEPARATOR)
        if not (term and separator and definition):
            raise BuildError(f"p{draft.number:02d}: {TERM_BLOCK} item must be term：definition: {item.text}")
        texts += [term, definition]
        entries.append(f"<li><dfn>{e(term)}</dfn><span>{e(definition)}</span></li>")
    return f'<aside class="terms"><b>{TERM_LABEL}</b><ul class="terms-{len(items)}">{"".join(entries)}</ul></aside>'


def render_slide(draft, total, root, sources, wiki_base=""):
    texts = []
    layout_path = root / LAYOUTS / f"p{draft.number:02d}.html"
    fragment = layout_path.read_text(encoding="utf-8") if layout_path.exists() else auto_layout(draft, root)
    content = fill_layout(fragment, draft, root, texts)
    terms = term_strip(draft, texts)

    page_label = f"{draft.number:02d} / {total:02d}"
    map_items = "".join(
        f'<li class="here">{e(node)}</li>' if node in draft.map_nodes else f"<li>{e(node)}</li>"
        for node in deck_draft.MAP_NODES
    )
    here = "、".join(draft.map_nodes)
    key_points = draft.block("重點")
    if len(key_points) != 1:
        raise BuildError(f"p{draft.number:02d}: needs exactly one 重點")
    key_point = key_points[0].text
    source_html, source_text = source_line(draft, root, sources, wiki_base)
    texts += [page_label, *deck_draft.MAP_NODES, draft.section, draft.title, KEY_POINT_LABEL, key_point]

    markup = (
        f'<section class="slide" id="p{draft.number}" aria-label="第 {draft.number} 頁">'
        f'<nav class="rail" aria-label="全程地圖，目前在{e(here)}"><span class="pg">{page_label}</span>'
        f'<ol class="map">{map_items}</ol>{PAGER}</nav>'
        f'<div class="body"><header><p class="part">{e(draft.section)}</p><h1>{e(draft.title)}</h1></header>'
        f"{content}{terms}"
        f'<p class="take"><b>{KEY_POINT_LABEL}</b>{e(key_point)}</p>'
        f'<p class="src">{source_html}</p></div></section>'
    )
    return Slide(draft.number, markup, texts, source_text)


def render_deck(root=ROOT, wiki_base=""):
    root = Path(root)
    drafts = deck_draft.load_drafts(root)
    if not drafts:
        raise BuildError("no drafts in deck/drafts")
    sources = load_sources(root / SOURCES)
    return [render_slide(draft, len(drafts), root, sources, wiki_base) for draft in drafts]


def build(root=ROOT, wiki_base=""):
    root = Path(root)
    template = (root / TEMPLATE).read_text(encoding="utf-8")
    if template.count(SLIDES_MARK) != 1:
        raise BuildError(f"{TEMPLATE} needs exactly one {SLIDES_MARK}")
    slides = render_deck(root, wiki_base)
    output = root / OUTPUT
    output.write_text(template.replace(SLIDES_MARK, "\n".join(s.html for s in slides)), encoding="utf-8")
    return output


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wiki-base", default="", help="URL prefix that turns Wiki page names into links")
    args = parser.parse_args()
    try:
        output = build(ROOT, args.wiki_base)
    except (BuildError, deck_draft.DraftError) as error:
        print(f"build failed: {error}")
        return 1
    print(f"wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
