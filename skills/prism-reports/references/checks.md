# Checks before handing over

Do them together in one pass, fix what one look shows, then look again.

1. **Render at 1440px and 390px**: `node <plugin>/scripts/check-report.mjs <page.html> [out-dir]` from a folder where `@playwright/test` resolves (it falls back to a global `playwright`). It prints `scrollWidth` at both widths (must equal the viewport: no sideways scroll), console and page errors, and writes full-page screenshots. Look at the screenshots: overlaps, clipped labels, wrapped nav, crushed tables.
2. **Use it for real**: sort a table, set and clear a filter, click a network node and a Pick button, hover a diagram step and tap one at 390px (its What/Why box opens). No console errors.
3. **One fact, one value, one view**: no dataset shown twice (a diagram plus a bar list of the same calls). The lede, next steps, stats, cards, tables and graph caption give the same answer for the same person or item, and every count matches what is shown (badge numbers, "N of M", captions).
4. **Detector**: when the impeccable skill is installed, run its `detect --json <page.html>` and fix contrast, text-size and cramped-padding findings. Inlined libraries and base64 images do not trigger it.
5. **Copy**: no em dashes anywhere; names in proper case; no jargon-only labels; no raw file paths or Copy buttons for files (files are plain links).
6. **Size**: the HTML stays compact (a few hundred KB at most, mostly photos); any library over a few KB loads from a pinned CDN instead of being inlined.

## Known gotchas

- **Chrome for Testing asks for the macOS keychain** ("wants to use your confidential information stored in Chromium Safe Storage") when a script launches it without `--use-mock-keychain`. Always pass it: `chromium.launch({ args: ["--use-mock-keychain"] })`, and add it to any custom `spawn` of the binary.
- **Extracting the template's style or scripts with a regex** can match the words `<style>` or `<script>` inside the template's own comment and produce a broken page with no CSS or JS. Anchor on `<style>\n:root` and on line-start `<script>\n`.
- **Grid matrices with `align-items:center`** make empty cells collapse and borders zig-zag; the template uses `stretch` plus flex-centered cells.
- **Cytoscape node photos over `file://`** fail with a CORS error unless the node style sets `background-image-crossorigin: "null"`; `<img>` tags are not affected. `check-report.mjs` prints the error.
- **Clicking a canvas in Playwright** needs it scrolled into view first; clicks outside the viewport land on nothing.
- **Biome/Ultracite formatting** strips a space after an inline tag (`<b>X</b> text` becomes `<b>X</b>text`). Where a space must follow `</b>`, `</a>`, `</small>`, `</tspan>`, write `&nbsp;`.
- **Report vs product style**: never repaint a product mockup in the report palette or force it light or dark.
