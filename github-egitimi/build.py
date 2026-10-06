"""Build the static lecture and its speaker notes from ders.json (stdlib only)."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def esc(value):
    return html.escape(str(value), quote=True)


def inline(value):
    value = esc(value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)


def clock(seconds):
    return f'{int(seconds)//60:02}:{int(seconds)%60:02}'


def source_links(slide):
    return ''.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>' for s in slide.get('sources', []))


def bullets(slide):
    if not slide.get('bullets'):
        return ''
    tag = 'ol' if slide.get('layout') == 'steps' else 'ul'
    return f'<{tag} class="big-list">' + ''.join(f'<li>{inline(b)}</li>' for b in slide['bullets']) + f'</{tag}>'


def codebox(code):
    lines = []
    for line in code.splitlines():
        cls = 'added' if line.startswith('+') else 'removed' if line.startswith('-') else ''
        lines.append(f'<span class="{cls}">{esc(line)}</span>')
    return '<pre class="codebox"><code>' + '\n'.join(lines) + '</code></pre>'


def render_slide(slide, index, main_count, timing):
    appendix = slide.get('appendix', False)
    number = f'Ek {index-main_count+1} / {44-main_count}' if appendix else f'{index+1} / {main_count}'
    title_tag = 'h1' if index == 0 else 'h2'
    theme = slide.get('theme', 'paper')
    layout = slide.get('layout', 'text')
    heading = f'<p class="eyebrow">{esc(slide.get("eyebrow", ""))}</p><{title_tag}>{esc(slide["title"])}</{title_tag}>'
    lead = f'<p class="lead">{inline(slide["lead"])}</p>' if slide.get('lead') else ''
    if layout == 'cover':
        content = lead + ( '<p class="byline">Arif Solmaz<br>İSTÜN Mekatronik Mühendisliği</p>' if index == 0 else bullets(slide))
        if slide.get('diagram'):
            content += f'<img class="diagram" src="{esc(slide["diagram"])}" alt="Git dalı ve ana akış">'
    elif slide.get('asset'):
        asset = slide['asset']
        poster = f'assets/posters/{Path(asset["src"]).stem}.png'
        content = lead + f'<img src="{esc(poster)}" data-animation="{esc(asset["src"])}" data-poster="{esc(poster)}" alt="{esc(asset["alt"])}" width="1920" height="1080">'
    elif slide.get('diagram'):
        content = lead + f'<img class="diagram" src="{esc(slide["diagram"])}" alt="{esc(slide.get("diagramAlt",slide["title"]))}">' + bullets(slide)
    elif slide.get('code'):
        side = bullets(slide)
        if slide.get('columns'):
            side += ''.join(f'<div class="column"><h3>{esc(c["heading"])}</h3><p>{inline(c["body"])}</p></div>' for c in slide['columns'])
        content = lead + (f'<div class="code-layout">{codebox(slide["code"])}<div>{side}</div></div>' if side else codebox(slide['code']))
    elif slide.get('columns'):
        columns = slide['columns']
        content = lead + f'<div class="columns {"three" if len(columns)==3 else ""}">' + ''.join(f'<div class="column"><h3>{esc(c["heading"])}</h3><p>{inline(c["body"])}</p></div>' for c in columns) + '</div>' + bullets(slide)
    else:
        content = lead + bullets(slide)
    if slide.get('caption'):
        content += f'<p class="caption">{inline(slide["caption"])}</p>'
    if slide.get('visibleSources'):
        content += f'<div class="slide-links">{source_links(slide)}</div>'
    speech = f'{timing}\n\n{slide["notes"]}'
    return f'''<section id="{esc(slide['id'])}" class="{theme} {layout}{' appendix' if appendix else ''}" aria-hidden="true">
{heading}<div class="content">{content}</div>
<footer class="slide-footer"><span>Git ve GitHub</span><span>{esc(number)}</span></footer>
<aside><div class="speech">{esc(speech)}</div><div class="sources">{source_links(slide)}</div></aside>
</section>'''


def main():
    data = json.loads((ROOT / 'ders.json').read_text())
    slides = data['slides']
    main_count = data['mainCount']
    assert len(slides) == 44 and main_count == 32
    assert sum(s['duration'] for s in slides[:main_count]) == 2700
    assert len({s['id'] for s in slides}) == len(slides)
    cumulative = 0
    rendered = []
    note_sections = []
    markdown = [f'# {data["title"]}', '', '32 ana slayt, 12 ek slayt. Ana anlatım ve sorular toplam 45 dakika.', '', 'Canlı gösterim, sınıf içi uygulama ve zorunlu ödev yoktur. Ek slaytlar ana anlatım süresinin dışındadır.', '']
    for i, slide in enumerate(slides):
        if i < main_count:
            timing = f'{clock(cumulative)}–{clock(cumulative+slide["duration"])} · {slide["duration"]} saniye'
            cumulative += slide['duration']
            label = str(i+1)
        else:
            timing = 'Ek slayt · ana anlatım süresinin dışında'
            label = f'Ek {i-main_count+1}'
        rendered.append(render_slide(slide,i,main_count,timing))
        note_sections.append(f'<section id="not-{i+1}"><p class="time">{esc(timing)}</p><h2>{label}. {esc(slide["title"])}</h2><p>{esc(slide["notes"]).replace(chr(10),"<br>")}</p><div class="sources">{source_links(slide)}</div><a class="back" href="index.html#{i+1}">Slaytı aç</a></section>')
        markdown.extend([f'## {label}. {slide["title"]}', '', timing, '', slide['notes'], '', 'Kaynaklar:', ''])
        markdown.extend([f'- [{s["title"]}]({s["url"]})' for s in slide.get('sources',[])])
        markdown.append('')
    document = f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(data['title'])}</title><meta name="description" content="Mekatronik öğrencileri için Git ve GitHub: 32 ana slayt ve 12 ek, 45 dakikalık anlatım, konuşmacı notları.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600..800&family=IBM+Plex+Sans:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/lecture.css"></head><body data-main-count="{main_count}">
<div id="ui-progress" aria-hidden="true"></div><main id="ui-viewport" aria-label="Birleşik Git ve GitHub sunumu"><div id="ui-stage">{''.join(rendered)}</div></main>
<div id="ui-notes" role="region" aria-label="Konuşmacı notları" hidden><h3 id="ui-notes-title"></h3><div id="ui-notes-body"></div><div id="ui-notes-sources"></div></div>
<div id="ui-overview" role="dialog" aria-modal="true" aria-label="Tüm slaytlar" hidden><div class="overview-top"><h2>Tüm slaytlar</h2><button id="ui-close-ov">Sunuma dön</button></div><h3>Ana anlatım · 32 slayt · 45 dakika</h3><div class="overview-grid" id="ui-main-grid"></div><h3>Ekler · 12 slayt</h3><div class="overview-grid" id="ui-extra-grid"></div></div>
<nav id="ui-bar" aria-label="Sunum gezinmesi"><button id="ui-prev" aria-label="Önceki slayt">←</button><span id="ui-count" aria-live="polite"></span><button id="ui-next" aria-label="Sonraki slayt">→</button><button id="ui-btn-ov">Genel bakış</button><button id="ui-btn-notes" aria-pressed="false">Notlar</button><button id="ui-appendix">Ek slaytlar</button><button id="ui-btn-replay">Animasyonu yinele</button><button id="ui-btn-fs">Tam ekran</button><button id="ui-btn-print">Yazdır</button><a href="konusmaci-notlari.html" target="_blank" rel="noopener">Not belgesi</a><a href="canli-ders/materyal.html">Materyal</a><span id="ui-help">← → gezin · N notlar · O genel bakış</span></nav>
<script src="assets/lecture.js"></script></body></html>'''
    (ROOT/'index.html').write_text(document)
    note_document = f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Konuşmacı notları · Git ve GitHub</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f1ea;color:#141b2b;font:19px/1.7 Arial,sans-serif}}main{{max-width:900px;margin:auto;padding:56px 28px}}h1{{font-size:44px;line-height:1.15}}h2{{font-size:28px;line-height:1.25}}a{{color:#a43f20}}section{{padding:38px 0;border-bottom:1px solid #cfc7ba;break-inside:avoid}}.time{{font-size:15px;color:#626d7d}}.sources{{display:flex;flex-direction:column;font-size:14px;gap:5px}}.back{{display:inline-block;margin-top:14px;font-size:14px}}nav{{display:flex;gap:24px;flex-wrap:wrap}}@media print{{body{{background:white;font-size:13pt}}main{{padding:0;max-width:none}}nav,.back{{display:none}}section{{padding:20px 0}}}}@page{{size:A4;margin:18mm}}
</style></head><body><main><nav><a href="index.html">Sunuma dön</a><a href="egitmen-rehberi.md" download>Notları indir</a></nav><h1>{esc(data['title'])}</h1><p>Konuşmacı notları · 32 ana slayt ve 12 ek</p><p>Ana anlatım ve sorular için süre: 45 dakika. Ek slaytlar soru ve ayrıntılı başvuru içindir.</p>{''.join(note_sections)}</main></body></html>'''
    (ROOT/'konusmaci-notlari.html').write_text(note_document)
    (ROOT/'egitmen-rehberi.md').write_text('\n'.join(markdown))
    print(f'Built {len(slides)} slides, {main_count} main, {cumulative}s. Notes: {sum(len(s["notes"].split()) for s in slides)} words.')


if __name__ == '__main__':
    main()
