# Decision pages and iterations

## Decision pages

Whenever the user must pick, approve or answer anything, render `templates/decision-page.html`, even for one yes/no and even when they did not ask for HTML. The user answers by clicking, never by typing in the terminal what the page could collect.

- **Header**: the main question as h1 ("Which X should we ship?"), the recommendation in one sentence with the reason, a meta line with the round number, date and what happens after the picks.
- **One thing** (the CTA block): `p.one` says how many questions to answer and to send them ("Answer 2 questions, then <span class="verb">Send results</span> (top right)."; the script renames `.verb` to Copy results when the page is opened as a file); the questions follow as `ol.next`, each linked to its section, with "X recommended" as the muted words.
- **Questions**: every `.opts[data-q="<question>"]` is one question; the page can hold several (pick a design, approve a plan, choose a name). Add `data-multi` when several picks are allowed (which screens to keep). Yes/no and approvals use the same cards without previews (`data-key="Yes" data-name="ship Friday"`). The template script adds a note box under each question (it grows as you type), a **Select all / Deselect all** bar with the count above every `data-multi` question, and a **Next question** button under each note that jumps to the next question. After the last question it adds a general note, **Anything else?**, whose button sends (or copies) the results. On screens 1180px and wider a **question sidebar** (`nav.wiz`) is docked down the left edge from the start, the page beside it: every question as a step with its answer, the one on screen in bold, click to jump. **Focus**: once the reader reaches the questions, every question but the one on screen dims (no blur), and the cards not picked in an answered question dim. A card whose chip reads `Recommended` gets a green frame and a solid chip, and the results button is green (tinted until every question is answered, then solid, with a send icon when served). Nothing to write for any of these. The button fills once its question has an answer.
- **Options** (`article.opt[data-key][data-name]` inside `.opts`): 2-4 side by side (one column on phones). Design options have a letter and a short name, a one-line description, a preview, 1-3 pros and cons (`.pc` with `li` / `li.con`), and a Pick button. When there is a recommendation, that option carries a `Recommended` chip. Pros and cons only when known; never invent them to fill a card.
- **Send results** (`button.copy-all`, last item in `nav.toc`): pinned right in the sticky top bar, shows `answered/total`. Served by `scripts/collect-answers.py`, one click posts the answers to the server and closes the tab; the server prints them and exits. A **Copy** button sits right before it, for a copy of the same block. Opened as a file it reads **Copy results** and copies one block to paste back in the chat. Answers and notes are remembered per page. After a copy, a **Close tab** button springs in right next to it in the top bar (Motion from the pinned CDN, loaded on the first pick; plain when offline or with reduced motion): it closes the tab when the browser allows it (a page opened from the terminal is allowed) and otherwise names the shortcut. Keep the script as it is.

  ```
  Answers from "<h1>" (/abs/path/page.html)
  1. <question>: B (<name>). Note: <note>
  2. <question>: Yes (ship Friday)
  3. <question>: no answer
  General note: <note>
  ```
- **Previews show the real thing**: the actual page section with each variant's CSS applied, a screenshot, or a mockup in the product's own style. Same content in every option so only the variable differs.
- **Compare**: a short sortable table of only the criteria that decide it, with SVG icons.
- Hand it over live: run `python3 <plugin>/scripts/collect-answers.py <page.html>` as a background command (it opens the page in the browser and prints its `http://127.0.0.1:<port>/` URL on stderr; it waits up to 4 hours, `--timeout` to change). Hand over that URL with the page's index and hub links, and say: click your answers, then Send results. When the command exits, its stdout is the block above, from the user's own clicks: apply every answer, then update the page: the next round on top, or a "Decided" state. Without background commands, hand over the file link and ask for Copy results pasted back.

## Iterations: the latest is always on top

Any page with rounds or versions (design rounds, a report updated after feedback, a decision that went through several picks):

- The latest round is the first section after the CTA, with an "Latest" chip (or "Decided") and a meta line saying what changed since the previous round.
- Earlier rounds go under "Earlier rounds", newest first, each collapsed in `<details>` with a summary line: `Round N · date · what we learned and why it moved on`. Earlier options keep their previews (screenshots are fine for the record) but have no Pick buttons; only the latest round can be picked.
- The nav lists rounds newest first; the newest link has `.latest`.
- A decided page keeps the CTA, its one thing now the decision in the user's words, and shows what shipped live as round N.
- The index sorts pages oldest first; inside a page, newest first.
