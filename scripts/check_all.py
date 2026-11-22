"""Run all wiki checks and append the result to reports/check-runs.md.

Usage:
  python scripts/check_all.py --label "ingest d2l-ch7 round 1"
Exit code is 1 when any check reports a problem.
"""
import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links  # noqa: E402
import check_quotes  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RUN_LOG = ROOT / "reports" / "check-runs.md"
RUN_LOG_HEADER = "# Check runs\n\nAppend-only record of every `scripts/check_all.py` run.\n\n"
CHECKS = {"check_quotes": check_quotes.check_wiki, "check_links": check_links.check_wiki}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", required=True, help="what this run is for, e.g. 'ingest d2l-ch7 round 1'")
    args = parser.parse_args()

    results = {name: check() for name, check in CHECKS.items()}
    total = sum(len(problems) for problems in results.values())
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    verdict = "PASS" if total == 0 else f"FAIL ({total})"
    lines = [f"## [{stamp}] {args.label} | {verdict}", ""]
    for name, problems in results.items():
        lines.append(f"- {name}: {len(problems)} problem(s)")
        lines += [f"  - `{p}`" for p in problems]
    text = "\n".join(lines) + "\n\n"

    print(text, end="")
    RUN_LOG.parent.mkdir(exist_ok=True)
    if not RUN_LOG.exists():
        RUN_LOG.write_text(RUN_LOG_HEADER, encoding="utf-8")
    with RUN_LOG.open("a", encoding="utf-8") as f:
        f.write(text)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
