#!/usr/bin/env node
// Render a report at 1440px and 390px: prints scrollWidth (must equal the viewport), page and console errors,
// and writes full-page screenshots. Run from a folder where @playwright/test (or playwright) resolves.
// Usage: node check-report.mjs <page.html> [out-dir]
import { createRequire } from "node:module";
import { resolve, basename } from "node:path";
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
  const shot = resolve(out, `${basename(file, ".html")}-${w}.png`);
  await page.screenshot({ path: shot, fullPage: true });
  const ok = sw <= w && errors.length === 0;
  failed ||= !ok;
  console.log(`${ok ? "ok  " : "FAIL"} ${w}px scrollWidth=${sw} errors=${errors.length} ${shot}`);
  for (const e of errors) console.log(`     ${e}`);
  await page.close();
}
await browser.close();
process.exit(failed ? 1 : 0);
