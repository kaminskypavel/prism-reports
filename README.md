<p align="center"><img src="assets/banner.jpg" alt="prism-reports: colored noise goes into a glass prism and comes out as one clear white beam" width="100%"></p>

<h1 align="center">prism-reports</h1>

A Claude Code plugin. Everything an agent shows you becomes one minimal HTML page: the answer first, the next step second, the evidence below.

## Install

```sh
claude plugin marketplace add kaminskypavel/prism-reports
claude plugin install prism-reports@prism-reports
```

## What changes

A `SessionStart` hook loads these rules into every session:

- Anything you read to understand, compare, decide or approve is an HTML page. Files agents read stay markdown.
- Each page answers first, then shows a titled Next steps block, at most 4 stats, the evidence, and an appendix.
- Pages live in the repo's `docs/reports/`, `docs/design/` or `docs/decisions/`. Each folder gets an index, and `docs/` gets an index of indexes.
- When you have to choose, you get a decision page with Pick buttons. With several rounds, the latest is on top.
- Every page is rendered at desktop and phone width and checked before you see it.

## Files

| Path | What |
|---|---|
| `hooks/always.md` | The rules loaded every session |
| `skills/prism-reports/` | The full playbook, loaded when a page is built |
| `templates/` | `daylight-report.html`, `midnight-report.html`, `decision-page.html` |
| `scripts/reports-index.py` | Builds the indexes |
| `scripts/check-report.mjs` | Renders a page at 1440px and 390px |

MIT
