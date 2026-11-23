"""Render deck/index.html in Edge and check every slide at 1280x720.

Usage:
  python scripts/check_deck_render.py --label "round 1"

Checks that nothing overflows, every image loads, and the text on screen equals the page
drafts plus the fixed labels. Appends to deck/reports/render.md and saves one screenshot per
slide to deck/reports/render/. Exit code is 1 on any problem.
"""
import argparse
import base64
import datetime
import json
import sys
import tempfile
import time
from collections import Counter
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_deck  # noqa: E402
from check_deck_evidence import WORK_TERMS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REPORT = Path("deck") / "reports" / "render.md"
SHOTS = Path("deck") / "reports" / "render"
REPORT_HEADER = "# 渲染檢查紀錄\n\n每次執行 `scripts/check_deck_render.py` 的結果，只往後加。\n\n"
WIDTH, HEIGHT = 1280, 720
TOLERANCE_PX = 1
LOAD_TIMEOUT_S = 30
POLL_S = 0.2
JPEG_QUALITY = 85

COLLECT_JS = """
(async (number) => {
  const slide = document.getElementById("p" + number);
  window.deck.show(number);
  await document.fonts.ready;
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const name = el => el.tagName.toLowerCase() + (el.classList.length ? "." + [...el.classList].join(".") : "");
  const texts = [];
  const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const value = walker.currentNode.textContent.trim();
    if (value && !walker.currentNode.parentElement.closest(".src")) texts.push(value);
  }
  const rect = el => { const r = el.getBoundingClientRect(); return {name: name(el), x: r.x, y: r.y, w: r.width, h: r.height}; };
  const elements = [...slide.querySelectorAll("*")].filter(el => !el.parentElement.closest("svg"));
  const clipped = [];
  const content = slide.querySelector(".content");
  if (content) {
    const outer = content.getBoundingClientRect();
    for (const el of content.querySelectorAll("*")) {
      if (el.parentElement.closest("svg")) continue;
      const r = el.getBoundingClientRect();
      if (r.width && r.height && (r.bottom > outer.bottom + 1 || r.right > outer.right + 1 || r.top < outer.top - 1 || r.left < outer.left - 1))
        clipped.push(name(el));
    }
  }
  for (const el of slide.querySelectorAll(".body, .body *")) {
    if (el.closest("svg")) continue;
    const style = getComputedStyle(el);
    if (style.display !== "inline" && el.clientHeight && (el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1))
      clipped.push(name(el) + " scrolls");
  }
  const urls = [...slide.querySelectorAll("img")].map(i => i.currentSrc || i.src)
    .concat([...slide.querySelectorAll("svg image")].map(i => new URL(i.getAttribute("href"), location.href).href));
  const failed = (await Promise.all(urls.map(u => new Promise(done => {
    const probe = new Image();
    probe.onload = () => done(probe.naturalWidth > 0 ? "" : u);
    probe.onerror = () => done(u);
    probe.src = u;
  })))).filter(Boolean);
  return JSON.stringify({texts, source: slide.querySelector(".src").textContent.trim(),
                         boxes: elements.map(rect), clipped: [...new Set(clipped)], failed, images: urls.length});
})
"""


def compare_texts(expected, actual):
    wanted, seen = Counter(expected), Counter(actual)
    problems = [f"missing text: {text}" for text in sorted((wanted - seen).elements())]
    problems += [f"unexpected text: {text}" for text in sorted((seen - wanted).elements())]
    return problems


def overflow_problems(boxes, width=WIDTH, height=HEIGHT, tolerance=TOLERANCE_PX):
    problems = []
    for b in boxes:
        if b["w"] <= 0 or b["h"] <= 0:
            continue
        if b["x"] < -tolerance or b["y"] < -tolerance or b["x"] + b["w"] > width + tolerance \
                or b["y"] + b["h"] > height + tolerance:
            problems.append(f"overflow: {b['name']} at ({b['x']:.0f}, {b['y']:.0f}) size {b['w']:.0f}x{b['h']:.0f}")
    return problems


def scan_work_terms(texts):
    return [(term, text) for text in texts for term in WORK_TERMS if term in text]


def write_report(root, label, problems, review, pages):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    verdict = "PASS" if not problems else f"FAIL ({len(problems)})"
    lines = [f"## [{stamp}] {label} | {verdict}", "", f"檢查 {pages} 頁，視窗 {WIDTH}×{HEIGHT}。"]
    if problems:
        lines += [""] + [f"- `{problem}`" for problem in problems]
    if review:
        lines += ["", "工作用語掃描（逐筆人工看過）：", ""] + [f"- {entry}" for entry in review]
    text = "\n".join(lines) + "\n\n"
    path = Path(root) / REPORT
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(REPORT_HEADER, encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)
    return text


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def _evaluate(browser, expression):
    result = browser.call("Runtime.evaluate", expression=expression, awaitPromise=True, returnByValue=True)
    if "exceptionDetails" in result:
        raise RuntimeError(f"page script failed: {result['exceptionDetails']}")
    return result["result"].get("value")


def _open_deck(browser, url):
    browser.call("Emulation.setDeviceMetricsOverride", width=WIDTH, height=HEIGHT, deviceScaleFactor=1, mobile=False)
    browser.call("Emulation.setScrollbarsHidden", hidden=True)
    browser.call("Page.enable")
    browser.call("Page.navigate", url=url)
    deadline = time.time() + LOAD_TIMEOUT_S
    while time.time() < deadline:
        if _evaluate(browser, "document.readyState === 'complete' && !!window.deck"):
            return
        time.sleep(POLL_S)
    raise RuntimeError("deck did not load")


def check_slides(root, browser, base_url):
    root = Path(root)
    slides = build_deck.render_deck(root)
    _open_deck(browser, f"{base_url}/{build_deck.OUTPUT.as_posix()}")
    shots = root / SHOTS
    shots.mkdir(parents=True, exist_ok=True)
    problems, review = [], []
    for slide in slides:
        where = f"p{slide.number:02d}"
        data = json.loads(_evaluate(browser, f"({COLLECT_JS})({slide.number})"))
        found = compare_texts(slide.texts, data["texts"])
        if data["source"] != slide.source:
            found.append(f"source line differs: {data['source']}")
        found += overflow_problems(data["boxes"])
        found += [f"content overflow: {name}" for name in data["clipped"]]
        found += [f"image failed: {url}" for url in data["failed"]]
        problems += [f"{where} {problem}" for problem in found]
        review += [f"{where} 含「{term}」：{text}" for term, text in scan_work_terms(data["texts"] + [data["source"]])]
        shot = browser.call("Page.captureScreenshot", format="jpeg", quality=JPEG_QUALITY)
        (shots / f"p{slide.number:02d}.jpg").write_bytes(base64.b64decode(shot["data"]))
    return problems, review, len(slides)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()

    from screenshot_figures import Browser  # needs websocket-client; only the real run uses it

    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(_QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
            browser = Browser(profile)
            try:
                problems, review, pages = check_slides(ROOT, browser, f"http://127.0.0.1:{server.server_port}")
            finally:
                browser.close()
    finally:
        server.shutdown()
    print(write_report(ROOT, args.label, problems, review, pages), end="")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
