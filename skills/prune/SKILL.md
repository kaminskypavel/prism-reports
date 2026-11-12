---
name: prune
description: Review, refresh and squash a prism page with many rounds - bring it up to the current rules (template, checks), then shorten it to its current answers, the older rounds summed up in one closed "Where we landed". With several pages that are rounds of one topic, merge them first. Use when the user says prune, squash, collapse or clean up the rounds of a report, dashboard or decision page.
argument-hint: "[page.html | folder] [extra fixes]"
---

# prune

Shortcut for `fix-report` with `prune` (and `merge` when given several pages of one topic).

**Input:** `$ARGUMENTS`

Follow `${CLAUDE_PLUGIN_ROOT}/skills/fix-report/SKILL.md` with these arguments plus `prune`:

1. **Target**: as in fix-report (none: the page this conversation is about, else the newest page under `docs/`). Say which page you picked.
2. **Several pages**: only rounds of one topic merge (fix-report "Merge"); pages on different topics stay separate, say so.
3. **Refresh**: fix-report steps 1 to 6 (template, musts).
4. **Squash**: fix-report "Prune": newest round whole, older rounds become one line each in a closed "Where we landed", one truth, answered questions become Decided cards.
5. **Review and hand over**: fix-report step 7 (checks at 1440px and 390px, index, links).
