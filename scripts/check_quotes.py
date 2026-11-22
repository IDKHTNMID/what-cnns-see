"""Check that wiki pages cite their sources and that quoted sentences exist in raw/.

Rules checked (see AGENTS.md, "出處格式"):
  1. Every citation points to a source folder that exists in raw/.
  2. Every "§ <section>" names a heading that exists in that source.
  3. Every "> 原文（slug）：sentence" line is found verbatim in the raw source.
  4. Every prose paragraph, list item, table row and figure in a content page
     carries at least one citation.

Usage:
  python scripts/check_quotes.py            # check the wiki, exit 1 on problems
  python scripts/check_quotes.py --dump X   # print source X as plain text, for copying quotes
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIRS = ("sources", "concepts", "methods")
GLOSSARY = "glossary.md"
EXEMPT_SECTIONS = {"相關頁面"}
WHOLE_SOURCE = "全文"

SKIP_TAGS = {"script", "style", "head", "noscript"}
BLOCK_TAGS = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "figcaption",
              "br", "tr", "section", "figure", "d-figure", "blockquote", "pre"}
HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}

CITATION_RE = re.compile(
    r"(?:\[[^\]]+\]\((?:[^)\s]*/)?sources/(?P<slug>[a-z0-9-]+)\.md\)\s*)?"
    r"§\s*(?P<section>[^）；]+?)\s*(?=[）；])")
QUOTE_RE = re.compile(r"^>\s*原文（(?P<slug>[a-z0-9-]+)）：\s*(?P<text>.+?)\s*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+")
TABLE_SEPARATOR_RE = re.compile(r"^\|?\s*:?-{3,}")
SECTION_NUMBER_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")

QUOTE_CHARS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                             " ": " ", " ": " ", " ": " "})


def normalize(text):
    """Make raw text and quotes comparable: straight quotes, single spaces."""
    return re.sub(r"\s+", " ", text.translate(QUOTE_CHARS)).strip()


def normalize_heading(text):
    text = normalize(text).rstrip("¶").strip()
    return SECTION_NUMBER_RE.sub("", text).casefold()


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.headings = [], []
        self._skip = 0
        self._heading = None

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self._skip += 1
        if tag in BLOCK_TAGS:
            self.parts.append("\n")
        if tag in HEADING_TAGS and not self._skip:
            self._heading = []

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self._skip:
            self._skip -= 1
        if tag in HEADING_TAGS and self._heading is not None:
            self.headings.append("".join(self._heading))
            self._heading = None
        if tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        self.parts.append(data)
        if self._heading is not None:
            self._heading.append(data)


class Source:
    """All HTML files under raw/<slug>/, as plain text plus heading list."""

    def __init__(self, slug, raw_dir):
        files = sorted((raw_dir / slug).rglob("*.html"))
        if not files:
            raise FileNotFoundError(f"no HTML files under raw/{slug}/")
        lines, headings = [], set()
        for f in files:
            parser = _TextExtractor()
            parser.feed(f.read_text(encoding="utf-8"))
            text = "".join(parser.parts)
            lines += [normalize(line) for line in text.split("\n") if line.strip()]
            headings |= {normalize_heading(h) for h in parser.headings if h.strip()}
        self.lines = lines
        self.text = " ".join(lines)
        self.headings = headings

    def has_section(self, title):
        return title == WHOLE_SOURCE or normalize_heading(title) in self.headings

    def has_quote(self, quote):
        return normalize(quote) in self.text


def _blocks(lines):
    """Yield (line_number, block_lines, section) for blank-line separated blocks."""
    block, start, section, in_code = [], 0, None, False
    for no, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            if block:
                yield start, block, section
                block = []
            continue
        if in_code:
            continue
        if line.startswith("#"):
            if block:
                yield start, block, section
                block = []
            if line.startswith("## "):
                section = line[3:].strip()
            continue
        if not line.strip():
            if block:
                yield start, block, section
                block = []
            continue
        if not block:
            start = no
        block.append(line)
    if block:
        yield start, block, section


def _uncited_units(block, start):
    """Return line numbers of units in this block that need a citation but lack one."""
    first = block[0].lstrip()
    if first.startswith((">", "<!--", "---")):
        return []
    if first.startswith("|"):
        return [start + i for i, row in enumerate(block)
                if i > 0 and not TABLE_SEPARATOR_RE.match(row) and not CITATION_RE.search(row)]
    if LIST_ITEM_RE.match(block[0]):
        items, current = [], None
        for i, line in enumerate(block):
            if LIST_ITEM_RE.match(line):
                current = [start + i, line]
                items.append(current)
            elif current:
                current[1] += " " + line
        return [no for no, text in items if not CITATION_RE.search(text)]
    return [] if CITATION_RE.search(" ".join(block)) else [start]


def check_page(path, wiki_dir, raw_dir, sources):
    problems = []
    rel = path.relative_to(wiki_dir.parent).as_posix()
    own_slug = path.stem if path.parent.name == "sources" else None
    is_glossary = path.name == GLOSSARY

    def source(slug):
        if slug not in sources:
            try:
                sources[slug] = Source(slug, raw_dir)
            except FileNotFoundError:
                sources[slug] = None
        return sources[slug]

    lines = path.read_text(encoding="utf-8").splitlines()
    for no, line in enumerate(lines, 1):
        for m in CITATION_RE.finditer(line):
            slug = m.group("slug") or own_slug
            if slug is None:
                problems.append(f"{rel}:{no}: '§ {m.group('section')}' has no source link")
                continue
            src = source(slug)
            if src is None:
                problems.append(f"{rel}:{no}: source '{slug}' not found in raw/")
            elif not src.has_section(m.group("section")):
                problems.append(f"{rel}:{no}: section '{m.group('section')}' not found in {slug}")
        q = QUOTE_RE.match(line)
        if q:
            src = source(q.group("slug"))
            if src is None:
                problems.append(f"{rel}:{no}: source '{q.group('slug')}' not found in raw/")
            elif not src.has_quote(q.group("text")):
                problems.append(f"{rel}:{no}: quote not found in {q.group('slug')}: {q.group('text')[:60]}")
        elif line.lstrip().startswith(">") and "原文" in line:
            problems.append(f"{rel}:{no}: quote line not in the form '> 原文（slug）：…'")

    for start, block, section in _blocks(lines):
        is_table = block[0].lstrip().startswith("|")
        if section in EXEMPT_SECTIONS or (section is None and not (is_table and is_glossary)):
            continue
        for no in _uncited_units(block, start):
            problems.append(f"{rel}:{no}: no citation")
    return problems


def content_pages(wiki_dir):
    pages = [p for d in CONTENT_DIRS for p in sorted((wiki_dir / d).glob("*.md"))]
    if (wiki_dir / GLOSSARY).exists():
        pages.append(wiki_dir / GLOSSARY)
    return pages


def check_wiki(root=ROOT):
    wiki_dir, raw_dir, sources = root / "wiki", root / "raw", {}
    problems = []
    for page in content_pages(wiki_dir):
        problems += check_page(page, wiki_dir, raw_dir, sources)
    return problems


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dump", metavar="SLUG", help="print raw/<SLUG> as plain text and its headings")
    args = parser.parse_args()
    if args.dump:
        src = Source(args.dump, ROOT / "raw")
        print("\n".join(src.lines))
        print("\n== headings ==\n" + "\n".join(sorted(src.headings)))
        return 0
    problems = check_wiki()
    for p in problems:
        print(p)
    print(f"check_quotes: {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
