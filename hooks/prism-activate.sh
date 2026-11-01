#!/bin/sh
# prism-reports: SessionStart activation.
# Prints the always-on ruleset with this install's absolute paths. The full
# playbook stays in skills/prism-reports/SKILL.md and loads on demand.
# No dependencies beyond POSIX sh.
set -u

root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
rules="$root/hooks/always.md"
[ -f "$rules" ] || exit 0

# The only substitution is the install root, so paths in the ruleset are real.
sed "s|{{ROOT}}|$root|g" "$rules"
