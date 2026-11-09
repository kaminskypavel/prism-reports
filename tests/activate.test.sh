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
grep -q "zoom-box" "$root/templates/decision-page.html" || fail "decision page images have no full size button"
grep -q '".preview > \[data-w\]"' "$root/templates/decision-page.html" || fail "decision page previews do not fit their card"
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

# Send results with two pasted images: the server saves them to a temp folder and prints their paths
echo "<p>x</p>" > "$tmp/p.html"
python3 - "$root/scripts/collect-answers.py" "$tmp/p.html" <<'PY' || fail "pasted images are not saved"
import json, os, subprocess, sys, urllib.request
p = subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2], "--no-open", "--timeout", "20"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
url = p.stderr.readline().split(": ", 1)[1].strip().rsplit("/", 1)[0] + "/__prism"
png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
import base64, shutil, tempfile
if shutil.which("sips"):  # a TIFF pasted from a clipboard manager comes back as PNG for its thumbnail (macOS)
    d = tempfile.mkdtemp(); open(f"{d}/a.png", "wb").write(base64.b64decode(png))
    subprocess.run(["sips", "-s", "format", "tiff", f"{d}/a.png", "--out", f"{d}/a.tiff"], capture_output=True)
    r = urllib.request.urlopen(urllib.request.Request(url + "/png", open(f"{d}/a.tiff", "rb").read()))
    assert r.status == 200 and r.read(8) == b"\x89PNG\r\n\x1a\n"; shutil.rmtree(d)
body = {"text": "1. Q: A. Note: look [image: paste-1.png] [image: ../up.png]", "images": [{"name": "paste-1.png", "data": png}, {"name": "../up.png", "data": png}]}
urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"}))
out = p.communicate(timeout=10)[0]
paths = [x.split("]")[0] for x in out.split("[image: ")[1:]]
assert len(paths) == 2 and all(os.path.isfile(f) for f in paths), out
assert len({os.path.dirname(f) for f in paths}) == 1 and "prism-notes" in paths[0], out  # ../ stays inside the temp folder
for f in paths: os.remove(f)
PY

# no em dashes in anything the agent reads
dash=$(printf "\342\200\224")
! grep -rl "$dash" "$root/hooks" "$root/skills" "$root/templates" "$root/AGENTS.md" >/dev/null 2>&1 || fail "em dash found"
echo "ok"
