---
name: prism-reports
description: Build HTML reports, dashboards, research pages, design reviews, mockup galleries and decision pages in the Daylight style - minimal, decision first, from one template, with sortable tables, Cytoscape networks, an index of every report, and render checks before handover. Use whenever the deliverable is an HTML page the user will open, or the user must pick or approve between options.
---

# prism-reports

One family of HTML pages for a reader with a short attention span: the answer first, the next step second, evidence below, nothing decorative. Minimal, easy to read, informative and structured.

Paths below are relative to this skill's base directory (the Skill tool prints it): the plugin root is two levels up, so templates are in `../../templates/` and scripts in `../../scripts/`. The SessionStart hook also prints them as absolute paths.

## When

- **Everything human-facing is a page**, asked for or not: anything the user reads to understand, compare, decide or approve (reports, dashboards, research, comparisons, status recaps, design reviews, mockup galleries).
- The user has to pick or approve between options (designs, names, plans, vendors, copy): build a decision page (`templates/decision-page.html`).
- Agent-facing files stay markdown so agents can grep them: plans and specs agents execute, agent-to-agent reports, CLAUDE.md, memory, skills, READMEs. When one needs the user's review or approval, also render an HTML view of it. Chat replies stay chat.

## Workflow

1. **Pick the page type.** Report (`daylight-report.html`), dark report only when asked (`midnight-report.html`), decision page (`decision-page.html`).
2. **Build one data object first.** Every number, verdict, path and label the page shows comes from it. The lede, the next steps, the stats, cards, tables and charts all read from that object, so two views can never disagree.
3. **Copy the template.** Keep its style block and all its script blocks; replace the demo content; delete components you don't use. Don't extract the style or scripts with a regex that can match the words inside the template's own comments; anchor on `<style>\n:root` and line-start `<script>`.
4. **Lay it out decision first** (see [references/style.md](references/style.md)): question h1, one-sentence answer, the titled "Next steps" block, up to 4 stats, sticky nav, evidence sections, appendix.
5. **Show, don't tell.** Every point that can be a chart becomes a chart: range bars, stacked bars, treemaps, ranked lists, verdict cards, matrices with SVG icons, step paths. Networks use Cytoscape ([references/networks.md](references/networks.md)). Every flow, process, timeline, Gantt, sequence, state or architecture is drawn with the `diagram-design` skill (a dependency of this plugin), never by hand ([references/style.md](references/style.md#diagrams)).
6. **Iterations and choices.** Latest round on top, earlier rounds collapsed below; choices get a decision page ([references/decisions-and-iterations.md](references/decisions-and-iterations.md)).
7. **File and index it.** Save it in the repo's `docs/` section (`docs/reports/`, `docs/design/`, `docs/decisions/`, or a section the repo already has) as `YYYY-MM-DD-topic.html`; run the index script on that section and the hub on `docs/` ([references/index.md](references/index.md)).
8. **Check it** ([references/checks.md](references/checks.md)): render at 1440px and 390px, click the interactive parts, confirm every view agrees, run the impeccable detector, no em dashes.
9. **Hand over** with markdown links that have a 🔗 label and a full file:// URL: the page, its index, and the hub when there is one.

## Musts

- Decision first: the answer and the next step are visible without scrolling.
- Minimal: light paper page, white surfaces with 1px borders, ink text, color only where it means something (good, caution, risk) or to tell stat cards and chart series apart. No gradient tiles, no white text on light fills, no colored left borders, no emoji or Unicode glyphs as icons.
- The call to action is a titled block with a stronger ink border, never colored.
- Tables sort; filters only where the reader will slice; wide tables scroll inside their panel on phones.
- Latest iteration on top. Anything the user must pick, approve or answer renders as a decision page: click to answer, Copy results in the sticky top bar.
- Compact: one HTML file; libraries from a pinned CDN (`cdn.jsdelivr.net/npm/<pkg>@<x.y.z>`), never inlined; images as small downscaled data URIs or files next to the page; no external fonts.
- Every page is in an index, and the handover links the index too.
- Text never below 12px; contrast 4.5:1 for text; no em dashes anywhere.
- A report never restyles the product it shows: mockups and screenshots keep the product's own look inside the report's panels.

## References

| File | What's in it |
|---|---|
| [references/style.md](references/style.md) | Layout order, tokens, typography, components, tables |
| [references/networks.md](references/networks.md) | Cytoscape intro/relationship networks: layout, click behavior, mobile |
| [references/decisions-and-iterations.md](references/decisions-and-iterations.md) | Decision pages, Pick flow, rounds with the latest on top |
| [references/index.md](references/index.md) | Report index, design index, hub of indexes, metadata |
| [references/checks.md](references/checks.md) | Render and interaction checks, detector, consistency, known gotchas |
