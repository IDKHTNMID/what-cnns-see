"""Check links between wiki pages.

Rules checked (see AGENTS.md, "Lint"):
  1. Every relative link or image path points to a file that exists.
  2. Every content page has at least one inbound link from another content page.
  3. Every content page is listed in wiki/index.md.
index.md, log.md and glossary.md are navigation pages, not content pages.

Usage:
  python scripts/check_links.py     # exit 1 on problems
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
NAVIGATION_PAGES = {"index.md", "log.md", "glossary.md"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "#")


def links_in(path):
    """Yield (line_number, target_text, resolved_path) for each relative link."""
    for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for m in LINK_RE.finditer(line):
            target = m.group(1)
            if target.startswith(EXTERNAL_PREFIXES):
                continue
            yield no, target, (path.parent / unquote(target.split("#", 1)[0])).resolve()


def check_wiki(root=ROOT):
    wiki_dir = root / "wiki"
    pages = sorted(wiki_dir.rglob("*.md"))
    content = {p.resolve() for p in pages if p.name not in NAVIGATION_PAGES or p.parent != wiki_dir}
    inbound = {p: set() for p in content}
    indexed = set()
    problems = []
    for page in pages:
        rel = page.relative_to(root).as_posix()
        for no, target, resolved in links_in(page):
            if not resolved.exists():
                problems.append(f"{rel}:{no}: broken link '{target}'")
                continue
            if resolved in inbound and resolved != page.resolve():
                if page.resolve() in content:
                    inbound[resolved].add(page.resolve())
                elif page.name == "index.md":
                    indexed.add(resolved)
    for p in sorted(content):
        rel = p.relative_to(root.resolve()).as_posix()
        if not inbound[p]:
            problems.append(f"{rel}: orphan (no inbound link from another content page)")
        if p not in indexed:
            problems.append(f"{rel}: not listed in wiki/index.md")
    return problems


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    problems = check_wiki()
    for p in problems:
        print(p)
    print(f"check_links: {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
