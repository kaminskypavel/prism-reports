# Where pages live, indexes, hub

## Location

Every page goes in the current repository's `docs/` folder, in the section that fits:

| Section | What goes there | Index title |
|---|---|---|
| `docs/reports/` | reports, research, dashboards, comparisons, status recaps | default |
| `docs/design/` | design reviews, mockups, prototypes, decision pages that pick a design | `--title Designs --fixed` |
| `docs/decisions/` | decision pages for anything else: names, vendors, plans, approaches | `--title Decisions --fixed` |

- Reuse a section the repo already has (`docs/wireframes/`, `docs/marketing/`, `docs/research/`) instead of inventing a new one; add a new section only when nothing fits.
- Name files `YYYY-MM-DD-topic.html` (the date the page was first made; later rounds update the same file, latest on top).
- Outside a git repo, ask once where to put it; never scatter pages on the Desktop or in temp folders.
- Assets a page needs (screenshots, photos) go next to it in a folder named after the page, or inline as small data URIs.

## Indexes

Every folder of HTML pages has an `index.html` listing every page with name, date and time, and topic, oldest first (several pages a day keep the order they were made in). Every page has a back link to it at the top. The handover always links the index too.

- Give each page `<meta name="report-topic" content="...">` (reuse a topic the folder's index already uses; add a new one only when none fits) and `<meta name="report-date" content="YYYY-MM-DD HH:MM">` with the time it was made. Without a time, the script takes the `YYYY-MM-DD-` name prefix plus the file creation time and writes it back as the meta tag.
- After writing or moving any page: `python3 <plugin>/scripts/reports-index.py <reports-dir>`. It rebuilds `index.html` (oldest first, topic filter pills) and adds the back link to any page without one. Safe to rerun.
- Design folders (mockups, prototypes, design rounds, decision pages): `python3 <plugin>/scripts/reports-index.py <design-dir> --title Designs --fixed`. `--fixed` pins the back link to the bottom-left corner so a mockup's own header stays untouched. Pages built from a prism template ignore it: their back link always sits first in the content column, lined up with the page like the index's own link.
- Never mark a page the user opens `report-index: skip`; every human-facing page (galleries, viewers, storyboards, listening pages) must be reachable from an index and the hub. Only fragments embedded in another page get `<meta name="report-index" content="skip">`.
- A page that has to live deeper than the index reaches (a tool's own output folder) gets a dated redirect stub in the section folder, so the index lists it.
- **Index of indexes**: a docs folder with two or more indexes (reports, designs, wireframes, marketing...) gets a hub: `python3 <plugin>/scripts/reports-index.py <docs-dir> --hub`. It writes `<docs-dir>/index.html` with one tile per index found up to 3 levels down, with item count and latest date. From then on every normal run below the hub adds an "All docs" link and refreshes the hub, so a new index shows up on its own.
- Handover: the page, its index, and the hub when the project has one, each as `[🔗 Name](file:///absolute/path)` on its own line.
