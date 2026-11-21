#!/usr/bin/env python3
"""Regenerate _includes/critical.css from the built site.

The site's own stylesheets (bootstrap.min.css, main.css, ...) block first
paint, and on mobile that costs ~2 s of LCP render delay. head.html instead
inlines the subset of rules that match something on the site and loads the
full files asynchronously, dropping the inline copy once they arrive.

That subset is produced here: every page in _site/sitemap.xml (plus a few
pages the sitemap leaves out) is opened in headless Chromium after main.js
has run, and a style rule is kept if any selector in it matches an element
on any page. Media-query wrappers are kept around their matching rules.
@font-face is dropped (only Bootstrap's unused Glyphicons declares one).

Rerun after changing CSS, layouts or includes:

    bundle exec jekyll build
    python3 tools/critical_css.py

Needs Python Playwright with Chromium (a dev tool, not a site dependency).
"""
import functools
import http.server
import pathlib
import re
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
OUT = ROOT / "_includes" / "critical.css"
EXTRA_PATHS = ["/page2/", "/tags/", "/404.html"]

# Collect matching rules in the page. Pseudo-classes that depend on state
# (:hover, :focus, ...) and pseudo-elements are stripped before matching,
# since the element they style is what matters. A selector the engine can't
# parse is kept, to err on the side of keeping too much.
COLLECT_JS = r"""
() => {
  const DYNAMIC = /::?(hover|focus|focus-within|focus-visible|active|visited|link|target|checked|disabled|enabled|indeterminate|placeholder|placeholder-shown|-webkit-[a-z-]+|-moz-[a-z-]+|-ms-[a-z-]+|before|after|first-line|first-letter|selection|marker|backdrop)(\([^)]*\))?/g;
  const matches = (sel) => sel.split(",").some((part) => {
    const s = part.replace(DYNAMIC, "").trim() || "*";
    try { return document.querySelector(s) !== null; } catch (e) { return true; }
  });
  const out = [], sheets = [];
  [...document.styleSheets].forEach((sheet, si) => {
    if (!sheet.href || !sheet.href.startsWith(location.origin)) return;
    sheets.push(new URL(sheet.href).pathname);
    const href = new URL(sheet.href).pathname;
    const walk = (rules, path) => {
      [...rules].forEach((rule, ri) => {
        const key = path.concat(ri);
        if (rule instanceof CSSStyleRule) {
          if (matches(rule.selectorText)) out.push({href, key, css: rule.cssText, media: null});
        } else if (rule instanceof CSSMediaRule) {
          const before = out.length;
          walk(rule.cssRules, key);
          for (let i = before; i < out.length; i++) {
            out[i].media = out[i].media || rule.conditionText;
          }
        } else if (rule instanceof CSSKeyframesRule) {
          out.push({href, key, css: rule.cssText, media: null});
        }
      });
    };
    walk(sheet.cssRules, []);
  });
  return {sheets, rules: out};
}
"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve():
    handler = functools.partial(QuietHandler, directory=str(SITE))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    sitemap = (SITE / "sitemap.xml").read_text()
    paths = [re.sub(r"^https?://[^/]+", "", u) for u in re.findall(r"<loc>([^<]+)</loc>", sitemap)]
    paths = [p for p in paths if not p.endswith(".pdf")] + EXTRA_PATHS

    httpd = serve()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    order = []   # stylesheet hrefs in document order
    rules = {}   # (href, key) -> (media, css)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 360, "height": 780})
        for path in paths:
            page.goto(base + path, wait_until="load")
            found = page.evaluate(COLLECT_JS)
            # Merge this page's stylesheet order into the global one: a
            # sheet not seen before goes right after its predecessor here.
            for i, href in enumerate(found["sheets"]):
                if href not in order:
                    prev = found["sheets"][i - 1] if i else None
                    order.insert(order.index(prev) + 1 if prev in order else 0, href)
            for r in found["rules"]:
                rules[(r["href"], tuple(r["key"]))] = (r["media"], r["css"])
        browser.close()
    httpd.shutdown()

    # Emit in cascade order: stylesheet order, then rule position. Adjacent
    # rules under the same media query share one @media block.
    lines, open_media = [], None
    for key in sorted(rules, key=lambda k: (order.index(k[0]), k[1])):
        media, css = rules[key]
        if media != open_media:
            if open_media:
                lines.append("}")
            if media:
                lines.append(f"@media {media}{{")
            open_media = media
        lines.append(css)
    if open_media:
        lines.append("}")
    text = "\n".join(lines) + "\n"
    header = f"/* Generated by tools/critical_css.py from {', '.join(order)} -- do not edit by hand. */\n"
    OUT.write_text(header + text)
    print(f"{len(paths)} pages, {len(rules)} rules, {len(text)} bytes -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
