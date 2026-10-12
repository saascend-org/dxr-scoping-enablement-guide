#!/usr/bin/env python3
"""Generates index.html for the scoping enablement guide.

Edit content.py, then run this. NEVER edit index.html by hand - it is regenerated.
Brand tokens come from the DXR Cyber kit via the partner-portal implementation:
white canvas, Instrument Sans, #1d1d1b headings, lime as a fill with #3b7a00 as its
text-safe partner on white, pill controls, 26px cards.
"""
import base64, html, pathlib, re, sys, content

def esc(s): return html.escape(str(s), quote=False)

CSS = """
:root{
  --lime:#a6ff33; --green:#4dde53; --cyan-t:#00808a;
  --ink:#1d1d1b; --head:#1d1d1b; --text:#2b303a; --muted:#5d626c; --dim:#8a8e96;
  --accent:#3b7a00; --line:rgba(43,48,58,.12); --line2:rgba(43,48,58,.22);
  --s1:rgba(43,48,58,.045); --r:26px; --r2:14px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:var(--text);
  font-family:"Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
.bar{display:flex;align-items:center;gap:18px;padding:20px 40px;border-bottom:1px solid var(--line);
  position:sticky;top:0;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);z-index:10}
.bar img{width:132px;height:auto;display:block}
.bar .tag{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);
  font-weight:600;border-left:1px solid var(--line2);padding-left:14px}
.wrap{max-width:880px;margin:0 auto;padding:0 24px 100px}
.rule{border-top:3px solid var(--lime);width:54px;margin:48px 0 18px}
h1{font-size:42px;line-height:1.08;letter-spacing:-.02em;color:var(--head);margin:0 0 10px;font-weight:700}
.sub{font-size:19px;color:var(--muted);margin:0 0 28px}
h2{font-size:26px;letter-spacing:-.015em;color:var(--head);margin:0 0 14px;font-weight:700}
h3{font-size:18px;color:var(--head);margin:0 0 8px;font-weight:600}
p{margin:0 0 14px}
a{color:var(--accent)}
.lead{font-size:17px}
.stages{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:26px 0 8px}
.stage{border:1px solid var(--line);border-radius:var(--r2);padding:14px 16px;background:#fff}
.stage b{display:block;font-size:14px;color:var(--head);margin-bottom:4px}
.stage span{font-size:13.5px;color:var(--muted);line-height:1.45}
.step{border-top:1px solid var(--line);padding-top:34px;margin-top:40px}
.step-head{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}
.num{flex:none;width:32px;height:32px;border-radius:50%;background:var(--ink);color:var(--lime);
  display:grid;place-items:center;font-weight:700;font-size:15px;align-self:flex-start}
figure{margin:22px 0 10px}
figure img{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:var(--r2);
  box-shadow:0 18px 50px rgba(29,29,27,.10)}
figcaption{font-size:13px;color:var(--dim);margin-top:9px}
.note{background:var(--s1);border-radius:var(--r2);padding:14px 18px;font-size:15px;
  color:var(--text);margin:18px 0 0;border-left:3px solid var(--lime)}
.note b{color:var(--head)}
.faq{border-top:1px solid var(--line);padding-top:18px;margin-top:18px}
.faq h3{margin-bottom:6px}
.faq p{color:var(--muted);margin:0}
.warn{background:#fdfbe7;border-radius:var(--r2);padding:22px 26px;margin-top:22px;
  border-left:3px solid #c9a800}
.warn h2{font-size:20px;margin-bottom:12px}
.warn p{color:#5b4f00}
footer{border-top:1px solid var(--line);margin-top:60px;padding-top:22px;
  font-size:13px;color:var(--dim)}
@media (max-width:640px){
  .bar{padding:16px 20px}.wrap{padding:0 18px 70px}h1{font-size:32px}.sub{font-size:17px}
}
"""

def step_html(s):
    # No loading="lazy" on the figures: the gated build injects the whole page via
    # document.write() with the screenshots already inlined as data URIs. Lazy images never
    # fire their observer on that path and render blank, and there is nothing to defer anyway.
    img = ""
    if s["img"]:
        img = (f'<figure><img src="assets/img/{s["img"]}" alt="{esc(s["alt"])}">'
               f'<figcaption>{esc(s["alt"])}</figcaption></figure>')
    note = f'<div class="note">{s["note"]}</div>' if s.get("note") else ""
    return f"""<section class="step">
  <div class="step-head"><div class="num">{s['n']}</div><h2>{esc(s['title'])}</h2></div>
  <p>{s['body']}</p>
  {img}
  {note}
</section>"""

doc = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(content.TITLE)} — DXR Cyber</title>
<meta name="description" content="{esc(content.SUBTITLE)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛡️</text></svg>">
<style>{CSS}</style>
</head>
<body>
<header class="bar">
  <img src="assets/img/dxr-cyber-logo.png" alt="DXR Cyber">
  <div class="tag">Enablement</div>
</header>
<main class="wrap">
  <div class="rule"></div>
  <h1>{esc(content.TITLE)}</h1>
  <p class="sub">{esc(content.SUBTITLE)}</p>
  <p class="lead">{content.INTRO}</p>

  <div class="rule"></div>
  <h2>The five stages</h2>
  <p>Every scoping request moves through these. The stage is on the record, so you can see where a
     client has got to without emailing to ask.</p>
  <div class="stages">
    {''.join(f'<div class="stage"><b>{esc(n)}</b><span>{esc(d)}</span></div>' for n, d in content.STAGES)}
  </div>

  {''.join(step_html(s) for s in content.STEPS)}

  <div class="rule"></div>
  <h2>Questions people ask</h2>
  {''.join(f'<div class="faq"><h3>{esc(q)}</h3><p>{esc(a)}</p></div>' for q, a in content.FAQ)}

  <div class="warn">
    <h2>What is not finished</h2>
    <p>{content.NOT_READY}</p>
  </div>

  <footer>{esc(content.FOOTER)}</footer>
</main>
</body>
</html>
"""
# Usage:
#   python3 build.py                              -> index.html, images referenced from assets/img
#   python3 build.py build/index.plain.html       -> same, for the encryptor
#   python3 build.py build/index.plain.html --inline
#       -> screenshots base64-inlined, so the encrypted payload is the ONLY place they exist.
#          The published site must never serve them as files: they show real DXR config.
out = sys.argv[1] if len(sys.argv) > 1 else 'index.html'

if '--inline' in sys.argv:
    def inline(m):
        p = pathlib.Path(m.group(1))
        if p.name == 'dxr-cyber-logo.png':      # the gate page needs the logo as a real file
            return m.group(0)
        return 'src="data:image/png;base64,' + base64.b64encode(p.read_bytes()).decode() + '"'
    doc, n = re.subn(r'src="(assets/img/[^"]+\.png)"', inline, doc)
    print(f"inlined {n} screenshots")

pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
open(out, 'w').write(doc)
print(f"{out} written: {len(doc):,} chars, {len(content.STEPS)} steps, {len(content.FAQ)} FAQs")
