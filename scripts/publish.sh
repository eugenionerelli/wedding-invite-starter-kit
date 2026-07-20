#!/usr/bin/env bash
#
# Publishes whatever is currently on disk, no matter which tool you used
# to change it (local editor, Webstudio, or by hand).
#
#   ./scripts/publish.sh "Updated the schedule"
#
# Nothing magic: shows what changed, asks for confirmation, then
# commit + push. The site updates on its own in about a minute.

set -euo pipefail

if [ -t 1 ]; then
  R=$'\e[31m'; V=$'\e[32m'; G=$'\e[33m'; B=$'\e[1m'; N=$'\e[0m'
else
  R=""; V=""; G=""; B=""; N=""
fi
ok(){ printf "%s✓%s %s\n" "$V" "$N" "$1"; }
err(){ printf "%s✗ %s%s\n" "$R" "$1" "$N" >&2; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MESSAGE="${1:-}"
if [ -z "$MESSAGE" ]; then
  err "Needs a message: ./scripts/publish.sh \"what you changed\""
  exit 1
fi

if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing to publish: the live site is already up to date."
  exit 0
fi

echo "Changes to publish:"
git status --short
echo
read -r -p "Proceed? [y/N] " answer || answer=""
case "$answer" in
  y|Y|yes|Yes|YES) ;;
  *) echo "Cancelled."; exit 0 ;;
esac

git add -A
git commit -q -m "$MESSAGE"
git push -q origin main

ok "Published. Live in about a minute."

# Best-effort: work out the GitHub Pages URL from the git remote, so this
# keeps working correctly whatever you rename the repo or account to.
REMOTE="$(git remote get-url origin 2>/dev/null || true)"
if [[ "$REMOTE" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
  echo "    https://${BASH_REMATCH[1]}.github.io/${BASH_REMATCH[2]}/"
fi
