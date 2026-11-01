# prism-reports: always on

**Everything human-facing is an HTML page**, even when the user did not ask for one: anything the user reads to understand, compare, decide or approve (reports, dashboards, research, comparisons, status recaps, design reviews, mockup galleries, option picks). It follows the `prism-reports` skill: load it with the Skill tool before writing the page; it holds the style, the components and the checks.

Agent-facing files stay markdown so agents can grep them: plans and specs that agents execute, agent-to-agent reports, CLAUDE.md, memory, skills, READMEs. When one of those needs the user's review or approval, also render an HTML view of it. Chat replies stay chat.

Musts, every time:

1. Start from a template, never from scratch: `{{ROOT}}/templates/daylight-report.html` (light, the default), `{{ROOT}}/templates/midnight-report.html` (dark, only when asked), `{{ROOT}}/templates/decision-page.html` (whenever the user must choose or approve).
2. Decision first: the question as h1, the answer in one sentence, a titled "Next steps" block (ink border, no color), at most 4 stats, then evidence, then an appendix.
3. Iterations: when a page has rounds or versions, the latest is always on top; earlier ones collapse below under "Earlier rounds", newest first.
4. Choices: whenever the user has to pick, approve or answer anything (one question or several), render a decision page: every question is answered by clicking (options side by side, a recommendation, Pick buttons, an optional note), and a Copy results button in the sticky top bar copies all answers at once to paste back in the terminal. Never ask them to type answers the page could collect.
5. Location: every page goes in the current repo's `docs/` folder, in its section: `docs/reports/` (reports, research, dashboards, comparisons, status recaps), `docs/design/` (design reviews, mockups, prototypes, design picks), `docs/decisions/` (other picks: names, vendors, plans). Reuse a section the repo already has (`docs/wireframes/`, `docs/marketing/`...). Name files `YYYY-MM-DD-topic.html`. Outside a git repo, ask once where to put it.
6. Index: every folder of reports gets an `index.html`, and a docs folder with two or more indexes gets an index of indexes. After writing any page run `python3 {{ROOT}}/scripts/reports-index.py <folder>` (designs: `--title Designs --fixed`; decisions: `--title Decisions --fixed`). With two or more sections, refresh the hub: `python3 {{ROOT}}/scripts/reports-index.py <repo>/docs --hub`.
7. Hand over with links: the page, its index, and the hub when there is one, each as a markdown link with a 🔗 label and the full file:// URL. Never only a path.
8. Check before handing over: render at 1440px and 390px (`node {{ROOT}}/scripts/check-report.mjs <page.html>`), click the interactive parts, make every view agree on the same facts, and run the impeccable detector when it is installed. No em dashes.
9. Compact: a page is one HTML file. Libraries (Cytoscape, chart or table packages) load from a pinned CDN (`https://cdn.jsdelivr.net/npm/<pkg>@<x.y.z>/...`), never inlined. Images as small data URIs (downscaled JPEG) or as files next to the page.
10. Files are links: every local file the page names is a plain `<a>` with a relative href, on the label itself ("Full quality"), not on an extra file-name line. Never a raw path, a path box or a Copy button.
