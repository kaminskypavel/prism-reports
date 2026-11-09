#!/bin/sh
# Checks the SessionStart hook: it prints the ruleset with real paths, quietly.
# Run: sh tests/activate.test.sh
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
fail() { echo "FAIL: $1" >&2; exit 1; }
run() { CLAUDE_PLUGIN_ROOT="$root" sh "$root/hooks/prism-activate.sh"; }

out=$(run)
[ -n "$out" ] || fail "hook printed nothing"
[ -z "$(run 2>&1 >/dev/null)" ] || fail "hook wrote to stderr"
echo "$out" | grep -q "{{ROOT}}" && fail "placeholder left unreplaced"
for f in templates/daylight-report.html templates/midnight-report.html templates/decision-page.html scripts/reports-index.py scripts/check-report.mjs; do
  echo "$out" | grep -q "$root/$f" || [ "$f" = templates/midnight-report.html ] || [ "$f" = scripts/check-report.mjs ] || fail "ruleset does not point at $f"
  [ -f "$root/$f" ] || fail "missing $f"
done
grep -q "latest is always on top" "$root/hooks/always.md" || fail "iteration rule missing"
grep -q "index of indexes" "$root/hooks/always.md" || fail "hub rule missing"
grep -q "Files are links" "$root/hooks/always.md" || fail "file link rule missing"
grep -q "Copy results" "$root/hooks/always.md" || fail "copy results rule missing"
grep -q "diagram-design" "$root/hooks/always.md" || fail "diagram rule missing"
grep -q '"name": "diagram-design"' "$root/.claude-plugin/marketplace.json" || fail "diagram-design dependency missing"
[ -f "$root/skills/fix-report/SKILL.md" ] || fail "fix-report skill missing"
for t in daylight-report midnight-report decision-page; do grep -q 'a.target = "_blank"' "$root/templates/$t.html" || fail "$t links do not open in a new tab"; done
for t in daylight-report midnight-report decision-page; do grep -q "data-tip" "$root/templates/$t.html" || fail "$t has no hover help"; done
grep -q "copy-all" "$root/templates/decision-page.html" || fail "decision page has no Copy results button"
grep -q "close-tab" "$root/templates/decision-page.html" || fail "decision page has no Close tab button"
grep -q "done-toast" "$root/templates/decision-page.html" && fail "decision page still has the old Close tab toast"
grep -q "One thing" "$root/hooks/always.md" || fail "one thing rule missing"
for t in daylight-report midnight-report decision-page; do grep -q '<p class="one"><mark>' "$root/templates/$t.html" || fail "$t has no highlighted One thing"; done
grep -q "next-q" "$root/templates/decision-page.html" || fail "decision page has no Next question button"
grep -q "collect-answers.py" "$root/hooks/always.md" || fail "send results rule missing"
grep -q "python3 -m webbrowser" "$root/hooks/always.md" || fail "open-in-browser rule missing"
grep -q "/__prism" "$root/templates/decision-page.html" || fail "decision page cannot send results"
grep -q "copy-one" "$root/templates/decision-page.html" || fail "decision page has no Copy next to Send results"
grep -q "data-rows" "$root/templates/decision-page.html" || fail "decision page has no row picks"
grep -q "row picks" "$root/hooks/always.md" || fail "row picks rule missing"
python3 "$root/scripts/collect-answers.py" -h >/dev/null || fail "collect-answers.py broken"
for t in daylight-report midnight-report decision-page; do grep -q "history.replaceState" "$root/templates/$t.html" || fail "$t in-page jumps add history (blocks Close tab)"; done
for t in daylight-report midnight-report decision-page; do awk '/<div class="wrap">/{getline n; if (n !~ /report-back/) exit 1; exit 0}' "$root/templates/$t.html" || fail "$t back link is outside the content column"; done
grep -q "budget:" "$root/scripts/check-report.mjs" || fail "check-report has no word budget"
grep -q "split:" "$root/scripts/check-report.mjs" || fail "check-report does not catch previews split from their options"
for t in daylight-report midnight-report decision-page; do grep -q "Facelift motion" "$root/templates/$t.html" || fail "$t has no facelift motion script"; done

# without CLAUDE_PLUGIN_ROOT it resolves its own install folder
out2=$(sh "$root/hooks/prism-activate.sh")
echo "$out2" | grep -q "$root/templates/daylight-report.html" || fail "fallback root not resolved"

# a missing ruleset exits quietly instead of failing the session
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/hooks"; cp "$root/hooks/prism-activate.sh" "$tmp/hooks/"
[ -z "$(CLAUDE_PLUGIN_ROOT="$tmp" sh "$tmp/hooks/prism-activate.sh" 2>&1)" ] || fail "missing ruleset should print nothing"

# no em dashes in anything the agent reads
dash=$(printf "\342\200\224")
! grep -rl "$dash" "$root/hooks" "$root/skills" "$root/templates" "$root/AGENTS.md" >/dev/null 2>&1 || fail "em dash found"
echo "ok"
