"""Screenshot figures that a page draws with JavaScript, using headless Edge over CDP.

Usage:
  python scripts/screenshot_figures.py <page URL> --list
  python scripts/screenshot_figures.py <page URL> --out raw/<slug>/screenshots --only 0,3,5

Figures are the page's <figure> and <d-figure> elements, numbered from 0 in page order.
Each capture is saved as figNN.png and shows the figure's default state, including labels
that stick a little out of the figure box. Only what is on screen is captured: capturing
beyond the window makes pages that draw figures on scroll (Distill) re-layout mid-capture,
so a figure taller than the window is reported as failed. A shot is kept only once the
figure's images have loaded and its position stayed the same while it was taken.
Existing files are not overwritten.
A figure that fails is reported and skipped; after a timeout the browser can be left in a bad
state, so rerun failed figures one per call and check every image.
Requires Microsoft Edge and the websocket-client package.
"""
import argparse
import base64
import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9333
VIEWPORT = (1280, 1000)
DEVICE_SCALE = 2
LOAD_WAIT_S = 8
FIGURE_WAIT_S = 2
CALL_TIMEOUT_S = 30
CAPTURE_TRIES = 10
# Count images in the figure that have not arrived yet: <img> tags, and CSS background images
# with no finished request (the resource-timing buffer is enlarged so none are dropped).
PENDING_IMAGES_JS = (
    "els.filter(e => e.tagName === 'IMG' && !e.complete).length"
    " + (() => { const done = new Set(performance.getEntriesByType('resource').map(r => r.name));"
    " return els.flatMap(e => [...getComputedStyle(e).backgroundImage.matchAll(/url\\(\"?([^\")]+)\"?\\)/g)])"
    ".filter(m => !m[1].startsWith('data:') && !done.has(new URL(m[1], location.href).href)).length; })()")
FIGURES = "document.querySelectorAll('figure, d-figure')"
PAD_PX = 8            # blank space kept around the figure
MAX_OVERFLOW_PX = 24  # how far labels may stick out of the figure box and still be captured


def capture_box(figure, parts, pad=PAD_PX, max_overflow=MAX_OVERFLOW_PX):
    """Area to capture: the figure box grown to hold its parts, then padded.

    Labels often stick out of a figure's fixed height; parts further out than max_overflow
    (hidden tooltips and the like) are cut off there. Boxes are dicts with x, y, w, h in page pixels.
    """
    left, top = figure["x"], figure["y"]
    right, bottom = left + figure["w"], top + figure["h"]
    for p in parts:
        if p["w"] <= 0 or p["h"] <= 0:
            continue
        left = min(left, max(p["x"], figure["x"] - max_overflow))
        top = min(top, max(p["y"], figure["y"] - max_overflow))
        right = max(right, min(p["x"] + p["w"], figure["x"] + figure["w"] + max_overflow))
        bottom = max(bottom, min(p["y"] + p["h"], figure["y"] + figure["h"] + max_overflow))
    left, top = max(left - pad, 0), max(top - pad, 0)
    right, bottom = right + pad, bottom + pad
    return {"x": left, "y": top, "w": right - left, "h": bottom - top}


def fits_viewport(box, scroll_y, height=VIEWPORT[1]):
    """True if the box lies within the visible part of the page (page pixels)."""
    return box["y"] >= scroll_y and box["y"] + box["h"] <= scroll_y + height


def capture_when_still(read, capture, ready=lambda layout: True, tries=CAPTURE_TRIES,
                       wait=lambda: time.sleep(FIGURE_WAIT_S)):
    """Once the figure is ready, capture, then read the layout again; keep the shot only if
    nothing moved meanwhile.

    Images loading above the figure push it down after it was measured, which leaves the
    shot showing whatever slid into its place; images still loading inside it leave holes.
    Returns None if the figure never gets ready and holds still.
    """
    for _ in range(tries):
        before = read()
        if ready(before):
            shot = capture(before)
            if read() == before:
                return shot
        wait()
    return None


class Browser:
    def __init__(self, profile_dir):
        self.proc = subprocess.Popen(
            [EDGE, "--headless=new", f"--remote-debugging-port={PORT}", "--remote-allow-origins=*",
             f"--user-data-dir={profile_dir}", f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tabs = None
        for _ in range(50):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
                break
            except OSError:
                time.sleep(0.2)
        if tabs is None:
            self.close()
            raise RuntimeError("Edge DevTools endpoint did not start")
        tab = next(t for t in tabs if t["type"] == "page")
        self.ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=CALL_TIMEOUT_S)
        self.msg_id = 0

    def call(self, method, **params):
        self.msg_id += 1
        self.ws.send(json.dumps({"id": self.msg_id, "method": method, "params": params}))
        while True:
            reply = json.loads(self.ws.recv())
            if reply.get("id") == self.msg_id:
                if "error" in reply:
                    raise RuntimeError(f"{method}: {reply['error']}")
                return reply["result"]

    def js(self, expression):
        result = self.call("Runtime.evaluate", expression=expression, returnByValue=True)
        return result["result"].get("value")

    def close(self):
        self.proc.terminate()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url")
    parser.add_argument("--list", action="store_true", help="list figures with their first words")
    parser.add_argument("--out", type=Path, help="output folder for figNN.png")
    parser.add_argument("--only", help="comma-separated figure numbers to capture")
    args = parser.parse_args()
    if not args.list and not (args.out and args.only):
        parser.error("use --list, or --out together with --only")

    failed = 0
    with tempfile.TemporaryDirectory() as profile:
        browser = Browser(profile)
        try:
            browser.call("Emulation.setDeviceMetricsOverride", width=VIEWPORT[0], height=VIEWPORT[1],
                         deviceScaleFactor=DEVICE_SCALE, mobile=False)
            browser.call("Emulation.setScrollbarsHidden", hidden=True)
            browser.call("Page.addScriptToEvaluateOnNewDocument",
                         source="performance.setResourceTimingBufferSize(100000)")
            browser.call("Page.navigate", url=args.url)
            time.sleep(LOAD_WAIT_S)
            count = browser.js(f"{FIGURES}.length")
            if args.list:
                for i in range(count):
                    text = browser.js(f"({FIGURES}[{i}].innerText || '').replace(/\\s+/g, ' ').slice(0, 80)")
                    print(f"{i:02d}: {text}")
                return 0
            args.out.mkdir(parents=True, exist_ok=True)
            for i in (int(n) for n in args.only.split(",")):
                path = args.out / f"fig{i:02d}.png"
                if path.exists():
                    print(f"fig {i:02d}: exists, skipped")
                    continue
                if not 0 <= i < count:
                    print(f"fig {i:02d}: failed (page has {count} figures)")
                    failed += 1
                    continue
                try:
                    browser.js(f"{FIGURES}[{i}].scrollIntoView({{block: 'center'}})")
                    time.sleep(FIGURE_WAIT_S)

                    def read_layout():
                        return browser.js(f"(() => {{ const f = {FIGURES}[{i}]; const els = [f, ...f.querySelectorAll('*')];"
                                          f" return {{scrollY, pending: {PENDING_IMAGES_JS}, boxes: els.map(e => {{"
                                          " const r = e.getBoundingClientRect();"
                                          " return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height};"
                                          " })}; })()")

                    def capture(layout):
                        box = capture_box(layout["boxes"][0], layout["boxes"][1:])
                        if not fits_viewport(box, layout["scrollY"]):
                            raise RuntimeError(f"taller than the {VIEWPORT[1]}px window")
                        shot = browser.call("Page.captureScreenshot", format="png", captureBeyondViewport=False,
                                            clip={"x": box["x"], "y": box["y"], "width": box["w"],
                                                  "height": box["h"], "scale": 1})
                        return shot, box

                    result = capture_when_still(read_layout, capture, ready=lambda layout: layout["pending"] == 0)
                    if result is None:
                        print(f"fig {i:02d}: failed (images kept loading or layout kept moving)")
                        failed += 1
                        continue
                    shot, box = result
                    path.write_bytes(base64.b64decode(shot["data"]))
                    print(f"fig {i:02d}: {box['w']:.0f}x{box['h']:.0f} -> {path.name}")
                except (OSError, RuntimeError, websocket.WebSocketException) as e:
                    print(f"fig {i:02d}: failed ({type(e).__name__}: {e})")
                    failed += 1
        finally:
            browser.close()
            time.sleep(1)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
