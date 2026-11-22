"""Screenshot figures that a page draws with JavaScript, using headless Edge over CDP.

Usage:
  python scripts/screenshot_figures.py <page URL> --list
  python scripts/screenshot_figures.py <page URL> --out raw/<slug>/screenshots --only 0,3,5

Figures are the page's <figure> and <d-figure> elements, numbered from 0 in page order.
Each capture is saved as figNN.png and shows the figure's default state. Existing files
are not overwritten. A figure that fails is reported and skipped.
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
FIGURES = "document.querySelectorAll('figure, d-figure')"


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
                    browser.js(f"{FIGURES}[{i}].scrollIntoView({{block: 'start'}})")
                    time.sleep(FIGURE_WAIT_S)
                    box = browser.js(f"(() => {{ const r = {FIGURES}[{i}].getBoundingClientRect();"
                                     " return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; })()")
                    shot = browser.call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                                        clip={"x": box["x"], "y": box["y"], "width": box["w"],
                                              "height": box["h"], "scale": 1})
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
