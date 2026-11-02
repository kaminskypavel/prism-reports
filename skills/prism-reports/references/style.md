# Style: layout, look, components

## Layout: decision first

1. **Header**: the question as h1, then the answer in one sentence that names the thing or person to act on (`.lede`), then one muted meta line (date, sources, method, cost).
2. **Next steps** (`.cta` > `.cta-h` + `ol.next`): the call to action. Title "Next steps" with "Do these in order"; 1-3 numbered asks, each naming who or what and through whom, with one muted line on why. Marked by a stronger border (1.5px ink) and its title, never by color: ink step numbers, no tints. Research-only pages with nothing to do may title it "What this means", still 1-3 lines. On a decision page the block is "Your call": each question to answer, linked to its section, with the recommendation as the muted line; the Copy results button sits in the sticky nav.
3. **Stats** (`.stats` / `.stat`): at most 4 small cards inside one white frame, ink numbers, each card on its own faint hue so they read apart: slate, teal, blue, amber by position, or by meaning with `.good` (teal), `.warn` (amber), `.bad` (pink). Each links to its section. The first stat is the decision's key number. Cost and run metadata go in the meta line, never in a stat. Skip the strip when the answer is a person or a choice, not a number.
4. **Sticky nav** (`nav.toc`): one scrolling row with every section plus Appendix; the template script marks the section in view. Round links carry `.latest` on the newest.
5. **Evidence sections**: question-style h2, an optional status chip, a one-line thesis, then panels. Order by what the reader needs to act, not by how the research went.
6. **Appendix** (`<details>`): funnels, method, sources, caveats, secondary matrices, run files. Nothing the reader needs to act lives only here.

## Look

- Page `#F3F3F0`; surfaces `#FFFFFF` with a 1px `#E2E2DC` border, radius 12 (border or shadow, never both); soft fills `#F7F7F4`.
- Ink `#141414`, muted `#5C5C56`, faint `#8A8A84` (never for text on soft fills: 3.2:1), lines `#E2E2DC`, tracks `#ECECE8`. One accent, blue `#2440E8`, for focus rings, the "latest" marker and the rare highlighted link.
- System font stack, `font-variant-numeric: tabular-nums`. h1 36px / -.025em, h2 24px / -.02em, body 15px / 1.55, captions 13px. Nothing below 12px.
- Semantic color as text, dots, thin bars and light tints, never as white-on-saturated fills: good teal `#0F766E` on `#E6F3F1`, caution amber `#B45309` on `#FBF1E4`, risk pink `#BE185D` on `#FBE9F1`, dead/closed a `#E11D48` outline.
- Stat hues (`--tint-*`): slate, teal, blue, amber, pink, cyan at 6-7% alpha.
- Categorical series for charts (`--c1..--c7`: blue, teal, amber, pink, violet, cyan, slate), dark enough for white labels. Use them to tell series apart, not to decorate. Violet is flagged by the impeccable detector as an "AI palette"; prefer cyan when a fifth hue is not needed.
- Browser surfaces themed: `::selection`, `:focus-visible` (2px accent outline), thin scrollbars, underline offset 3px; `prefers-reduced-motion` turns off smooth scrolling.
- Midnight (dark, opt-in only): page `#000`, surfaces `#121212` with a 1px `#2E2E2E` border, ink white, muted `#B3B3B3`, accent `#A78BFA`; semantic colors as light text on dark tints.
- Compact: libraries from a pinned CDN, never inlined. Photos are downscaled to about 160px and saved once in a folder next to the page (`<page-name>/<photo>.jpg`), referenced by relative path from cards, tables and networks; never embed the same photo as a data URI in several places.
- Never: gradient tiles, rainbow rows, white text on light or mid-tone fills, colored left borders above 1px, decorative shadows, emoji or Unicode ✓ ✕ as icons, eyebrow labels above headings.

## Components (all in the templates)

- `.cta`, `.cta-h`, `ol.next`: the call to action. `.stats` / `.stat`: hued stat cards.
- `.chip` with `.good` `.warn` `.bad` `.accent` (`.plain` drops the dot): status next to an h2 or in a table cell.
- `.who`: avatar (photo data URI or initials) + name + role, for people in cards and table cells.
- `.panel`, `.cols` (2-up), `.ph` panel label, `.cap` caption, `.note` soft callout.
- Charts: `.rb` range/value bars (independent values on one scale only; bars that follow each other in time or add up to a total are a diagram-design Gantt or waterfall), `.stack` stacked bar, `.tm` treemap, `.grid` tinted verdict cards (`.good` `.warn` `.bad` `.dead`), `.path` + `.step` only for a 2 to 4 step people chain, `.nums` numbered cards.
- `.mx` verdict matrix with `.ic` SVG icons (check, cross, question in the template demo). Before any matrix, one line saying what the columns mean; empty cells where "no" is not news.
- People to act on first: 3-5 cards. Everyone else: a table.
- Every repo, project, plugin or app named in a page is a link (GitHub URL, site, or file:// for a local repo), in body text, cards, tables and the appendix, not only in a sources list.
- Every local file a page names (a render, video, image, export, doc) is a plain `<a>` link: href relative to the page (`renders/promo.mp4`), and the link is the label the reader already sees ("Full quality", "Small file for sending"), not an extra line with the file name under it, so right-click > Copy Link works on the label itself. Size or format as muted text after it. Use the template's `a.file-link` (accent blue, bold). Example: `<a class="file-link" href="renders/promo.mp4">Full quality</a> <span class="cap">49 MB</span>`. Never a path in a code box, never Path/Link rows, never Copy buttons for files. Absolute paths appear nowhere on the page; the link already carries them.

## Diagrams

- Every flow, process, timeline, Gantt, sequence, state, tree or architecture is made with the `diagram-design` skill: pick the type there and follow its type reference and layout rules. Never hand-roll step pills or ad-hoc SVG.
- One dataset, one view: never show the same data as a diagram and again as bars, a list or a table. The diagram's `data-tip` carries the detail.
- Embed its SVG inline in a `.panel` of the page, not as a separate file. The page is the skin: do not run diagram-design's onboarding or edit its `style-guide.md`; map its roles to the page's CSS variables so the diagram follows Daylight and Midnight alike.

  | diagram-design role | Page variable |
  |---|---|
  | `paper`, `paper-2` | `var(--surface)`, `var(--soft)` |
  | `ink`, `ink-strong` | `var(--ink)` |
  | `muted`, `soft` | `var(--mute)` |
  | `rule`, `rule-solid` | `var(--line)`, `var(--faint)` |
  | `accent`, `accent-tint`, `link` | `var(--accent)`, `var(--accent-tint)`, `var(--accent)` |
  | `series-1` to `series-5` | `var(--c1)` to `var(--c5)` |
  | font | `var(--font)` |

- **Hover help**: every step, node, bar and row worth explaining carries `data-tip`, two lines: `What: <what happens>` and `Why: <why it is there>` (newline as `&#10;`). The template script opens it on hover, keyboard focus or tap, inside SVG too. Put it on the node's `<g>`, not on its text.

## Tables

- Every `<table>` gets click-to-sort headers (keyboard too) and a horizontal scroller on narrow screens; tables with 4+ columns get a minimum width so they scroll instead of crushing cells.
- `data-filter` on a `<table>` adds a filter box, a Clear button and a row count; use it only when the table has about 15+ rows or the reader will slice it. `<th data-facet>` marks the columns worth a dropdown (low-cardinality clean values like status or tier, never free text). The dropdown keeps the column name in the selected value.
- `data-sort` on a cell gives the sort value when the text won't sort right ("2013-16", "now"). `<table data-plain>` opts out of sorting.
