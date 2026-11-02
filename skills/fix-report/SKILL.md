---
name: fix-report
description: Bring an existing prism page up to the current rules in place - refresh its template style and scripts, then fix what the rules now require (files as links, diagram-design diagrams with hover help, decision pages with Copy results) and re-run the checks. Use when the user says fix, upgrade, tighten or clean up a report, dashboard or decision page, or points at an older page.
argument-hint: "[page.html | folder | file:// URL] [extra fixes]"
---

# fix-report

Fix one page in place, or every page in a folder. Same file, same URL, same facts. Change only what breaks the current rules.

**Input:** `$ARGUMENTS`

- First word: the target, as a path, a `file://` URL, or a folder (every `.html` in it except `index.html`).
- Anything after it: extra fixes the user wants on top of the rules ("make the Gantt bigger"), applied in step 4.
- No target: the page this conversation is about; else the newest page under the repo's `docs/`. Say which page you picked before editing it.

1. **Load the rules.** Load the `prism-reports` skill with the Skill tool and read the page. Name its template: decision page when it asks the user to pick or approve, midnight when it is dark, else daylight.
2. **Generated page? Fix the generator.** If a script next to the page writes it (`gen.py`, `build.mjs`...), make every change below in the script and re-run it. Never hand-edit output that the next run overwrites.
3. **Refresh the template parts.** Replace the page's template CSS (from `<style>\n:root` to where the page's own rules start) and its template `<script>` blocks with the current template's. Keep the page's own CSS and scripts unless the template now covers them (path Copy buttons, the old single "Copy my pick" bar, hand-made tooltips).
4. **Fix against the musts**, only where the page breaks them, then apply the user's extra fixes:
   - Decision first: question h1, one-sentence answer, titled Next steps, at most 4 stats.
   - Files: raw paths, path boxes and Copy buttons become `a.file-link` on the label.
   - Diagrams: step pills, hand-drawn SVG flows and ASCII art become a diagram-design diagram, inline, in the page's CSS variables. Every step, node and bar gets `data-tip` ("What: ..." and "Why: ..."); `?` popovers become `data-tip`.
   - Choices: anything the user must pick, approve or answer becomes decision-page questions with Copy results in the sticky bar.
   - Iterations latest on top, back link to the index, libraries from a pinned CDN, no em dashes.
5. **Keep the rest.** Don't reword, reorder or restyle what already passes, and never change a number or a fact unless it was wrong.
6. **Check and hand over.** Run the checks in the `prism-reports` skill (render at 1440px and 390px, hover and tap a diagram step, click every Pick), re-run the index script, then hand over the page link with one line per fix.
