---
name: fix-report
description: Bring an existing prism page up to the current rules in place - refresh its template style and scripts, then fix what the rules now require (files as links, diagram-design diagrams with hover help, picks with Send results) and re-run the checks. Also merges pages that are rounds of one topic into one page with a tab per round, and prunes a page with many rounds down to its current answers. Use when the user says fix, upgrade, tighten, clean up, merge or prune a report, dashboard or decision page, or points at an older page.
argument-hint: "[page.html | folder | all] [force | merge | prune] [extra fixes]"
---

# fix-report

Fix one page in place, or every page in a folder. Same file, same URL, same facts. Change only what breaks the current rules.

**Input:** `$ARGUMENTS`

- **Target**, the first word:
  - a page path or `file://` URL: that page.
  - a folder: every page in it.
  - `all` (or `--all`): every page under the repo's `docs/`, every section. Indexes and the hub are rebuilt by the index script, not fixed by hand.
  - none: the page this conversation is about; else the newest page under `docs/`. Never every page. Say which page you picked before editing it.
- **`force`** (or `--force`), anywhere: redo the whole page on the current template, not only what breaks a rule. Re-lay out every section decision first, rebuild every diagram with diagram-design, tighten every line. Facts, numbers and links still stay.
- **`merge`**, anywhere, with two or more pages that are rounds of one topic: join them into one page, a tab per round (see Merge below), then fix that page. Pages on different topics never merge; link them both ways instead.
- **`prune`**, anywhere: shorten a page with many rounds to its current answers (see Prune below), then fix it.
- **Anything else**: extra fixes the user wants on top of the rules ("make the Gantt bigger"), applied in step 4.
- **Several pages**: list them first, one line each, then fix them one at a time.
- **Safety**: before the first edit, copy every file this run will write that git does not track or that has uncommitted changes (the page, its generator, and the `index.html` and hub the index script rewrites) to a temp folder, and say where.

1. **Load the rules from this plugin version.** Read `${CLAUDE_PLUGIN_ROOT}/skills/prism-reports/SKILL.md` and the references it links (not an older cached copy), then the page. Templates are in `${CLAUDE_PLUGIN_ROOT}/templates/`, scripts in `${CLAUDE_PLUGIN_ROOT}/scripts/`.
2. **Pick the template.** Decision page when the page asks the user to pick, approve or answer anything (a pick inside a report's One thing counts: the decision template is the report template plus Pick cards and Send results). Midnight when the page is dark. Else daylight.
3. **Generated page? Fix the generator.** If a script next to the page writes it (`gen.py`, `build.mjs`...), make every change in the script and re-run it; never hand-edit output the next run overwrites. Make it read the newest installed template, not a pinned version (`.../prism-reports/0.3.4/templates/...`). Anchor on `<style>\n:root` and the first line-start `<script>`, never on a template demo section. Switching templates changes the back-link label and placeholders: set them again (step 4).
4. **Refresh the template parts.** Skip when a generator already reads the newest template. Otherwise replace the template CSS (the `<style>` that starts with `:root`, up to the first rule the template does not have) and the template `<script>` blocks with the current template's. Keep the page's own CSS (later rules or separate `<style>` blocks) and scripts unless the template now covers them (path Copy buttons, the old "Copy my pick" bar, hand-made tooltips).
5. **Fix against the musts**, only where the page breaks them, then apply the user's extra fixes:
   - Decision first, goldfish short: question h1, one-sentence answer (25 words max), the One thing block (`p.one-h` + one `p.one` of 15 words max with its words in `<mark>` + 0-3 steps of 14 words max; an old `.cta-h` "Next steps" or "Your call" title becomes it), at most 4 stats. Trim words until `check-report.mjs` passes the budget; never drop a fact the reader needs to act, move it lower.
   - Metadata: `<title>`, `report-topic` and `report-date` are real values, never the template's `Topic` or `YYYY-MM-DD HH:MM`. The back link points at its index (`../index.html` when the page is a folder's `index.html`) and is labelled with that index's name.
   - Files: raw paths, path boxes and Copy buttons become `a.file-link` on the label, including a generator named in the meta line.
   - Diagrams: step pills, ad-hoc SVG shapes, ASCII art, and bar lists whose bars follow each other in time or add up to a total (range bars used as a timeline or a projection) become a diagram-design diagram (Gantt, waterfall, swimlane...), inline, in the page's CSS variables. A generated SVG that follows a diagram-design type reference passes. Measured data stays: never drop real bars or rows to fit a type's size limits; keep the type's styling instead. One dataset, one view: when a diagram shows the same data as an older chart, bar list or table, delete the old one and move any detail only it had into the diagram's tips.
   - Hover help: every step, node, bar and row gets `data-tip` ("What: ..." and "Why: ..."); `?` popovers become `data-tip`. Axis lines, moment markers and legends need none.
   - Choices: every pending pick, approval or open question becomes a decision-page question with Send results in the sticky bar. In a report, put it in a "Your pick" section right after the nav and link it from its step in the One thing block. Add a `Recommended` chip and pros and cons only when the page already states them; never invent them.
   - Links: every link that leaves the page opens in a new tab (comes with the current template script).
   - Technical tables at the end (runs, logs, raw data) sit in a closed `<details>` with a row count in the summary.
   - Rounds: from round 2 on, each round is a tab (`nav.rounds` + `div.round`, see the prism-reports decisions reference). Rounds listed in `nav.toc` with earlier ones in `<details>` under "Earlier rounds" become tabs: each earlier round's body moves into its own `div.round`, ids prefixed.
   - Order: rounds, versions and change-log tables newest first. Libraries from a pinned CDN, no em dashes.
6. **Keep the rest** (skipped with `force`). Don't reword, reorder or restyle what already passes, and never change a number or a fact unless it was wrong. Flag stale or contradictory data to the user instead of fixing it.
7. **Check and hand over.** Run every check in the prism-reports `references/checks.md` (render at 1440px and 390px, use every interactive part: hover and tap a diagram step, click every Pick and Send results, sort a table; one fact one value; the impeccable detector; copy; size). Re-run the index script, then serve the page: `python3 <prism root>/scripts/collect-answers.py <page.html>` as a background command (it opens one tab that reloads itself on every change; Send results ends it and its output holds the answers, pasted images as paths), and link its `http://127.0.0.1:<port>/` URL first. With several pages, open their index once instead (`python3 -m webbrowser -t "file://<abs path>"`). Then hand over the page, its index and the hub as links, with one line per fix and one per thing left unfixed.

## Merge: rounds of one topic that landed as separate pages

Only pages on the same topic (round 1 of a domain pick in one file, round 2 in another). Different topics stay separate pages; if asked to merge them, say so and link them both ways instead.

1. **Plan it.** The merged page keeps the oldest page's file name and folder, so its links stay. One round per page, newest first; only the newest page's open questions stay open. Two pages with open questions: stop and ask which is current.
2. **Build it** on the current template: its style and scripts, then the back link, `nav.rounds` with one link per round, and one `div.round` (`id="round-N"`) per page holding that page's body (everything inside `.wrap` but the back link). Each page's own CSS (rules its template does not have) moves to one extra `<style>` after the template's.
3. **Keep ids unique.** Prefix every id inside a round with the round id, and rewrite what points at it: `href="#x"`, `url(#x)`, `for`, `aria-*`. Links to the other merged pages become round jumps (`#round-1`, `#round-1-compare`); relative links from a page that came from another folder get re-rooted.
4. **Retire the old files.** Remove them (Safety above backs up any that git does not hold as they are), point every link to them in the repo at the merged page and round, and re-run the indexes: the index lists each round under the page.
5. **Check every round**: open `page.html#round-N` at 1440px and 390px, no `#` link without a target, no console errors. Flag facts a newer round overruled in an older one; prune fixes those.

## Prune: a page with many rounds down to its current answers

Asked for, prune may change facts; nothing else in this skill does.

- **Keep the newest round whole.** The older round tabs go, and the page drops `nav.rounds` and its `div.round` wrapper (one round, no tabs). Their story becomes one closed `<details>` "Where we landed" at the end: one line per round (what it found, why it moved on), newest first. Their bodies go; git keeps them. A round that only led to a dead end is one line.
- **One truth.** A lede, One thing or stat that a newer round overruled is rewritten to the current answer.
- **Answered questions** become Decided cards: no `data-q`, no Pick buttons, the pick in the user's words.
