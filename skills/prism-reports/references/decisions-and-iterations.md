# Decision pages and iterations

## Decision pages

Whenever the user must pick, approve or answer anything, render `templates/decision-page.html`, even for one yes/no and even when they did not ask for HTML. The user answers by clicking, never by typing in the terminal what the page could collect.

- **Header**: the main question as h1 ("Which X should we ship?"), the recommendation in one sentence with the reason, a meta line with the round number, date and what happens after the picks.
- **Your call** (the CTA block): the questions to answer as `ol.next`, each linked to its section, the recommendation as the muted line.
- **Questions**: every `.opts[data-q="<question>"]` is one question; the page can hold several (pick a design, approve a plan, choose a name). Add `data-multi` when several picks are allowed (which screens to keep). Yes/no and approvals use the same cards without previews (`data-key="Yes" data-name="ship Friday"`). The template script adds a note box under each question.
- **Options** (`article.opt[data-key][data-name]` inside `.opts`): 2-4 side by side (one column on phones). Design options have a letter and a short name, a one-line description, a preview, 1-3 pros and cons (`.pc` with `li` / `li.con`), and a Pick button. When there is a recommendation, that option carries a `Recommended` chip. Pros and cons only when known; never invent them to fill a card.
- **Copy results** (`button.copy-all`, last item in `nav.toc`): pinned right in the sticky top bar, shows `answered/total`, and copies one block to paste back in the chat. Answers and notes are remembered per page.

  ```
  Answers from "<h1>" (/abs/path/page.html)
  1. <question>: B (<name>). Note: <note>
  2. <question>: Yes (ship Friday)
  3. <question>: no answer
  ```
- **Previews show the real thing**: the actual page section with each variant's CSS applied, a screenshot, or a mockup in the product's own style. Same content in every option so only the variable differs.
- **Compare**: a short sortable table of only the criteria that decide it, with SVG icons.
- Give the user the page link and say: click your answers, then Copy results and paste it here. When they paste, apply every answer, then update the page: the next round on top, or a "Decided" state.

## Iterations: the latest is always on top

Any page with rounds or versions (design rounds, a report updated after feedback, a decision that went through several picks):

- The latest round is the first section after the CTA, with an "Latest" chip (or "Decided") and a meta line saying what changed since the previous round.
- Earlier rounds go under "Earlier rounds", newest first, each collapsed in `<details>` with a summary line: `Round N · date · what we learned and why it moved on`. Earlier options keep their previews (screenshots are fine for the record) but have no Pick buttons; only the latest round can be picked.
- The nav lists rounds newest first; the newest link has `.latest`.
- A decided page keeps the CTA as a "Decision" block quoting the user's words, and shows what shipped live as round N.
- The index sorts pages oldest first; inside a page, newest first.
