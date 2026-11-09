#!/usr/bin/env node
// Render a report at 1440px and 390px: prints scrollWidth (must equal the viewport), page and console errors, word-budget misses,
// and writes full-page screenshots. Run from a folder where @playwright/test (or playwright) resolves.
// Usage: node check-report.mjs <page.html> [out-dir]
import { createRequire } from "node:module";
import { resolve, basename, dirname } from "node:path";
import { mkdirSync } from "node:fs";
import { tmpdir } from "node:os";

const [file, outArg] = process.argv.slice(2);
if (!file) { console.error("usage: node check-report.mjs <page.html> [out-dir]"); process.exit(2); }
const require = createRequire(resolve(process.cwd(), "noop.js"));
let chromium;
for (const mod of ["@playwright/test", "playwright"]) { try { ({ chromium } = require(mod)); break; } catch {} }
if (!chromium) { console.error("Playwright not found here. cd into a project that has @playwright/test, or npm i -g playwright."); process.exit(2); }

const out = outArg ? resolve(outArg) : resolve(tmpdir(), "daylight-check");
mkdirSync(out, { recursive: true });
const url = `file://${resolve(file)}`;
// --use-mock-keychain: Chrome for Testing otherwise asks for the macOS keychain on every launch.
const browser = await chromium.launch({ args: ["--use-mock-keychain"] });
let failed = false;
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, isMobile: w < 500, hasTouch: w < 500 });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await page.goto(url);
  await page.waitForTimeout(400);
  const sw = await page.evaluate(() => document.documentElement.scrollWidth);
  // Goldfish budget on prism pages (they have a .cta): exactly one One thing, and short lines above the fold.
  if (w > 500) errors.push(...await page.evaluate(() => {
    if (!document.querySelector(".cta")) return [];
    const words = (el) => el.textContent.split(/\s+/).filter((x) => /[\p{L}\p{N}]/u.test(x)).length;
    const own = (sel) => [...document.querySelectorAll(sel)].filter((el) => !el.closest(".preview")); // previews show the product, not the page
    const n = own(".cta .one").length;
    const out = n === 1 ? [] : [`budget: the .cta needs exactly one p.one (the One thing), found ${n}`];
    for (const [sel, cap] of [[".one", 15], [".lede", 25], [".next li", 14], [".thesis", 20]])
      for (const el of own(sel)) if (words(el) > cap) out.push(`budget: ${sel} has ${words(el)} words, cap ${cap}: "${el.textContent.trim().slice(0, 70)}"`);
    // An option's visual sits in its own card: a figure captioned with an option's name, outside the cards, splits the pick from what it picks.
    for (const g of document.querySelectorAll(".opts[data-q]")) {
      const names = new Set([...g.querySelectorAll(".opt")].flatMap((o) => [o.dataset.key, o.dataset.name, o.querySelector(".opt-h b")?.textContent]).filter(Boolean).map((t) => t.trim().toLowerCase()));
      for (const f of (g.closest("section") || document).querySelectorAll("figure")) {
        const c = f.querySelector("figcaption")?.textContent.trim();
        if (c && !f.closest(".opt") && names.has(c.toLowerCase())) out.push(`split: "${c}" is shown outside its option card in "${g.dataset.q}"; move it into that card's .preview`);
      }
    }
    return out;
  }));
  const name = basename(file, ".html") === "index" ? basename(dirname(resolve(file))) : basename(file, ".html"); // folder pages: name after the folder
  const shot = resolve(out, `${name}-${w}.png`);
  await page.screenshot({ path: shot, fullPage: true });
  const ok = sw <= w && errors.length === 0;
  failed ||= !ok;
  console.log(`${ok ? "ok  " : "FAIL"} ${w}px scrollWidth=${sw} errors=${errors.length} ${shot}`);
  for (const e of errors) console.log(`     ${e}`);
  await page.close();
}
await browser.close();
process.exit(failed ? 1 : 0);
