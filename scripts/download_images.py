"""Download images used by a raw source page, keeping their original relative paths.

Usage:
  python scripts/download_images.py raw/<slug>/<page>.html <page URL> [relative paths ...]

Without relative paths, every relative <img src> in the page is downloaded (images in
HTML comments are ignored). Give paths explicitly for images that the page loads from
JavaScript. Files listed under "Figures not stored here" in raw/SOURCES.md are skipped,
existing files are never overwritten, and nothing is written outside raw/<slug>/.
"""
import fnmatch
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
SOURCES_MD = RAW / "SOURCES.md"
EXCLUDED_SECTION = "## Figures not stored here"
USER_AGENT = "Mozilla/5.0 (wiki source mirror)"
TIMEOUT_S = 60


class _ImgCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        src = dict(attrs).get("src") if tag == "img" else None
        if src and "://" not in src and not src.startswith(("//", "data:")) and src not in self.srcs:
            self.srcs.append(src)


def excluded_patterns(slug):
    """Backticked file patterns for this slug in the SOURCES.md exclusion table."""
    text = SOURCES_MD.read_text(encoding="utf-8")
    section = text.split(EXCLUDED_SECTION, 1)[1].split("\n## ", 1)[0] if EXCLUDED_SECTION in text else ""
    patterns = []
    for row in section.splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] == slug:
            patterns += re.findall(r"`([^`]+)`", cells[1])
    return patterns


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    page = Path(sys.argv[1]).resolve()
    page_url, explicit = sys.argv[2], sys.argv[3:]
    slug_dir = RAW / page.relative_to(RAW).parts[0]
    collector = _ImgCollector()
    collector.feed(page.read_text(encoding="utf-8"))
    srcs = explicit or collector.srcs
    patterns = excluded_patterns(slug_dir.name)

    counts = {"downloaded": 0, "existing": 0, "excluded": 0, "failed": 0}
    for src in srcs:
        target = (page.parent / src).resolve()
        rel = target.relative_to(slug_dir).as_posix() if target.is_relative_to(slug_dir) else None
        if rel is None:
            print(f"failed   {src}: resolves outside {slug_dir.name}/")
            counts["failed"] += 1
        elif any(fnmatch.fnmatch(rel, p) for p in patterns):
            print(f"excluded {rel}")
            counts["excluded"] += 1
        elif target.exists():
            counts["existing"] += 1
        else:
            url = urljoin(page_url, src)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                    data = resp.read()
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                print(f"ok       {rel} ({len(data)} B)")
                counts["downloaded"] += 1
            except OSError as e:
                print(f"failed   {rel}: {e}")
                counts["failed"] += 1
    print(", ".join(f"{k} {v}" for k, v in counts.items()))
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
