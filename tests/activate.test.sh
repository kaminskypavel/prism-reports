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
