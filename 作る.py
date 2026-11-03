#!/usr/bin/env python3
"""neuron-notes を作る（AI なし）。cards/*.md → index.html と cards/<slug>.html。11-03 Shota 声 4091〜4133。
カードの形：頭に「key: 値」の行、---en と ---ja の後に本文（**太字** と空行の段落だけ）。"""
import html, pathlib, re
ROOT = pathlib.Path(__file__).parent
CSS = """*{box-sizing:border-box}body{margin:0;background:#f7f5f0;color:#14181f;font-family:"Noto Sans JP","Noto Sans CJK JP",system-ui,sans-serif;line-height:1.7}
a{color:#2f7d6b}.wrap{max-width:880px;margin:0 auto;padding:48px 20px}.k{font-size:14px;color:#2f7d6b;font-weight:700;letter-spacing:.12em}
h1{font-size:44px;line-height:1.15;margin:8px 0 12px}.lead{color:#4b5563;font-size:18px}.card{display:block;background:#fff;border-radius:20px;padding:20px;margin:22px 0;box-shadow:0 10px 30px #0001;text-decoration:none;color:inherit}
.card img,.fig{width:100%;border-radius:14px;display:block}.card h2{font-size:22px;margin:14px 0 2px}.meta{color:#8a8f98;font-size:14px}
.lang{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:24px}@media(max-width:720px){.lang{grid-template-columns:1fr}h1{font-size:32px}}
footer{color:#8a8f98;font-size:13px;margin-top:48px}"""
PAGE = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t}</title><meta name="description" content="{d}"><style>{css}</style></head><body><div class="wrap">{b}<footer>neuron-notes — short cards on how real neurons work, for people who build AI. By Shota (zdna0x). Sources are linked on every card.</footer></div></body></html>'

def md(s):
    out = []
    for para in [p.strip() for p in s.strip().split("\n\n") if p.strip()]:
        t = html.escape(para)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        out.append(f"<p>{t}</p>")
    return "\n".join(out)

def load(p):
    head, rest = p.read_text().split("---en", 1)
    en, ja = rest.split("---ja", 1)
    meta = dict(l.split(": ", 1) for l in head.strip().splitlines() if ": " in l)
    return meta, en, ja

cards = [load(p) for p in sorted((ROOT / "cards").glob("*.md"))]
items = []
for m, en, ja in cards:
    body = (f'<div class="k"><a href="../index.html">NEURON-NOTES</a> · {m["date"]}</div><h1>{html.escape(m["title_en"])}</h1>'
            f'<div class="lead">{html.escape(m["title_ja"])}</div><img class="fig" src="../{m["image_en"]}" alt="{html.escape(m["title_en"])}">'
            f'<div class="lang"><div lang="en">{md(en)}</div><div lang="ja">{md(ja)}<img class="fig" src="../{m["image_ja"]}" alt="{html.escape(m["title_ja"])}"></div></div>'
            f'<p class="meta">Source: <a href="{m["source_url"]}">{html.escape(m["source"])}</a></p>')
    (ROOT / "cards" / f'{m["slug"]}.html').write_text(PAGE.format(t=html.escape(m["title_en"]) + " — neuron-notes", d=html.escape(m["title_en"]), css=CSS, b=body))
    items.append(f'<a class="card" href="cards/{m["slug"]}.html"><img src="{m["image_en"]}" alt="{html.escape(m["title_en"])}"><h2>{html.escape(m["title_en"])}</h2><div class="meta">{m["date"]} · {html.escape(m["title_ja"])}</div></a>')
idx = ('<div class="k">NEURON-NOTES</div><h1>How real neurons work,<br>one card at a time.</h1>'
       '<p class="lead">Short cards for people who build AI: conclusion, meaning, and what it means for AI. 本物のニューロンの仕組みを、一枚ずつ。</p>' + "\n".join(reversed(items)))
(ROOT / "index.html").write_text(PAGE.format(t="neuron-notes", d="How real neurons work, one card at a time.", css=CSS, b=idx))
print(f"{len(cards)} 枚で作った")
