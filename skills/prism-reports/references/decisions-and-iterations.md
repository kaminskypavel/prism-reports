# Decision pages and iterations

## Decision pages

Whenever the user must pick between options or approve a design, render `templates/decision-page.html`, even for two options and even when they did not ask for HTML. It is the "pick one" family member of the report.

- **Header**: the question as h1 ("Which X should we ship?"), the recommendation in one sentence with the reason, a meta line with the round number, date and what happens after the pick.
- **Your call** (the CTA block): an optional note box and a Copy button. Picking an option copies one line, `Decision "<h1>": option B (<name>). Note: <note>`, for the user to paste back in the chat, and remembers the pick per page.
- **Options** (`.opts` > `article.opt[data-key][data-name]`): 2-4 side by side (one column on phones). Each has a letter and a short name, a one-line description, a preview, 1-3 pros and cons (`.pc` with `li` / `li.con`), and a Pick button. One option carries a `Recommended` chip.
- **Previews show the real thing**: the actual page section with each variant's CSS applied, a screenshot, or a mockup in the product's own style. Same content in every option so only the variable differs.
- **Compare**: a short sortable table of only the criteria that decide it, with SVG icons.
- Give the user the page link and say what they'll paste back. When they answer, apply the pick, then update the page: the next round on top, or a "Decided" state.

## Iterations: the latest is always on top

Any page with rounds or versions (design rounds, a report updated after feedback, a decision that went through several picks):

- The latest round is the first section after the CTA, with an "Latest" chip (or "Decided") and a meta line saying what changed since the previous round.
- Earlier rounds go under "Earlier rounds", newest first, each collapsed in `<details>` with a summary line: `Round N · date · what we learned and why it moved on`. Earlier options keep their previews (screenshots are fine for the record) but have no Pick buttons; only the latest round can be picked.
- The nav lists rounds newest first; the newest link has `.latest`.
- A decided page keeps the CTA as a "Decision" block quoting the user's words, and shows what shipped live as round N.
- The index sorts pages oldest first; inside a page, newest first.
