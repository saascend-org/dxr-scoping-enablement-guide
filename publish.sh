#!/bin/bash
# Rebuild the password-gated scoping guide and push it to GitHub Pages.
# Prompts for the password so it never lands in a file, the repo or shell history.
set -euo pipefail
cd "$(dirname "$0")"
read -rsp "Guide password: " PW; echo
[ -n "$PW" ] || { echo "No password entered - nothing published."; exit 1; }
python3 build.py build/index.plain.html --inline
printf %s "$PW" | node build/encrypt.js -
unset PW
git add index.html assets/img/dxr-cyber-logo.png .gitignore README.md publish.sh build.py build/encrypt.js
git commit -m "Publish scoping enablement guide $(date +%Y-%m-%d)" || echo "(no changes to commit)"
git push origin main
echo "Live in about a minute."
