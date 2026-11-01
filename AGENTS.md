# prism-reports

Minimal, decision-first HTML reports, dashboards and decision pages. Full playbook: [`skills/prism-reports/SKILL.md`](skills/prism-reports/SKILL.md). The always-on ruleset a session gets at start: [`hooks/always.md`](hooks/always.md).

Short version:

0. Everything human-facing is an HTML page, asked for or not; agent-facing files (plans agents execute, memory, CLAUDE.md, skills, READMEs) stay markdown.
1. Every page starts from a template in [`templates/`](templates/): `daylight-report.html` (default), `midnight-report.html` (dark, only when asked), `decision-page.html` (whenever the user must pick or approve).
2. Decision first: question h1, one-sentence answer, a titled "Next steps" block with an ink border and no color, at most 4 hued stat cards, evidence, appendix.
3. Latest iteration on top; earlier rounds collapse below, newest first.
4. Pages live in the repo's `docs/` folder by section (`docs/reports/`, `docs/design/`, `docs/decisions/`). Every folder of pages gets an index (`scripts/reports-index.py`), and a docs folder with several indexes gets an index of indexes (`--hub`). The handover links the page, its index and the hub.
5. Check before handover: render at 1440px and 390px (`scripts/check-report.mjs`), click the interactive parts, make every view agree, no em dashes. Compact: libraries from a pinned CDN, never inlined.

Developing this repo: `sh tests/activate.test.sh`; enable the version guard once with `git config core.hooksPath .githooks` (plugin installs are cached by version, so content changes need a version bump).
