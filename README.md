# DXR Cyber — Scoping Requests enablement guide

Enablement guide for XYP-SCOPE-001, the scoping request process in Salesforce.

## The published file is encrypted

`index.html` in this repo is a **password gate**, not the guide. The readable page is
AES-256-GCM ciphertext inside it, under a PBKDF2-SHA256 (600k iteration) key derived from the
password. The screenshots are base64-inlined into that payload, so a host serving this repo never
has the guide or the screenshots in the clear.

**The password is not in this repo and must never be committed.** `publish.sh` prompts for it so
it stays out of files and shell history. Ask whoever published last.

## Editing

```bash
python3 build.py          # -> index.html, PLAINTEXT, for local reading only
./publish.sh              # rebuild, re-encrypt, commit, push
```

Edit `content.py`. **Never edit `index.html`** — it is regenerated, and a stray edit destroys the
gate. `encrypt.js` keeps one `.bak` of whatever it overwrites, because a test run with a throwaway
password would otherwise lock the live site behind a string nobody knows.

Preview locally with the `scoping-guide` config in `../.claude/launch.json` (port 8793). Serve it
over http rather than opening the file directly — `crypto.subtle` needs a secure context.

## Screenshots

`assets/img/` is captured from `Xypher_Sandbox_FC` by `../playwright/capture-scoping-modal.js`
(Request Scoping modal) and headless Chrome with a 70s `--virtual-time-budget` for the record
pages; at 35s those capture the chrome with an empty body.

**They are git-ignored except the logo.** They show the demo record
`Northvale Manufacturing (Scoping Demo)`, not a real client — but they also show real DXR Cyber
configuration: stage names, MEDDPICC qualification guidance, custom tabs. They belong inside the
encrypted payload and nowhere else.

The figures carry no `loading="lazy"`. The gated page is injected with `document.write()`, and
lazy images never fire their observer on that path — they silently render blank.
