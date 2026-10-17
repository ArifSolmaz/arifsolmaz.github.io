"""Build the Turkish/English lecture and speaker notes (stdlib only)."""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UI = {
    'tr': {
        'footer': 'Git ve GitHub', 'appendix': 'Ek', 'seconds': 'saniye',
        'appendix_timing': 'Ek slayt · ana anlatım süresinin dışında',
        'byline': 'İSTÜN Mekatronik Mühendisliği', 'cover_alt': 'Git dalı ve ana akış',
        'description': 'Git ve GitHub neden kullanılır? Çalışma felsefesi, gerçek kullanım, kazanımlar ve maliyetler: {main_count} ana slayt ve {extra_count} ek, {minutes} dakikalık anlatım.',
        'lecture_label': 'Git ve GitHub çalışma felsefesi sunumu', 'notes': 'Konuşmacı notları',
        'all_slides': 'Tüm slaytlar', 'return': 'Sunuma dön',
        'main_heading': 'Ana anlatım · {main_count} slayt · {minutes} dakika', 'extra_heading': 'Ekler · {extra_count} slayt',
        'navigation': 'Sunum gezinmesi', 'previous': 'Önceki slayt', 'next': 'Sonraki slayt',
        'edit': 'Düzenle', 'overview': 'Genel bakış', 'notes_button': 'Notlar', 'appendix_button': 'Ek slaytlar',
        'replay': 'Animasyonu yinele', 'fullscreen': 'Tam ekran', 'print': 'Yazdır',
        'notes_document': 'Not belgesi', 'materials': 'Materyal', 'pdf': 'PDF indir',
        'help': '← → gezin · N notlar · O genel bakış', 'open_slide': 'Slaytı aç',
        'sources': 'Kaynaklar', 'download_notes': 'Notları indir',
        'code_notes': 'Kodun anlamı', 'notes_subtitle': 'Konuşmacı notları · {main_count} ana slayt ve {extra_count} ek',
        'notes_intro': 'Ana anlatım ve sorular için süre: 45 dakika. Ek slaytlar soru ve ayrıntılı başvuru içindir.',
        'markdown_intro': '{main_count} ana slayt, {extra_count} ek slayt. Ana anlatım ve sorular toplam {minutes} dakika.',
        'markdown_scope': 'Canlı gösterim, sınıf içi uygulama ve zorunlu ödev yoktur. Ek slaytlar ana anlatım süresinin dışındadır.',
        'language_label': 'Switch to English',
    },
    'en': {
        'footer': 'Git and GitHub', 'appendix': 'Appendix', 'seconds': 'seconds',
        'appendix_timing': 'Appendix slide · outside the main lecture time',
        'byline': 'İSTÜN Mechatronics Engineering', 'cover_alt': 'Git branch and main workflow',
        'description': 'Why use Git and GitHub? Their working philosophy, real uses, benefits and costs: {main_count} main slides, {extra_count} appendix slides and a {minutes}-minute lecture.',
        'lecture_label': 'Git and GitHub working philosophy presentation', 'notes': 'Speaker notes',
        'all_slides': 'All slides', 'return': 'Return to presentation',
        'main_heading': 'Main lecture · {main_count} slides · {minutes} minutes', 'extra_heading': 'Appendix · {extra_count} slides',
        'navigation': 'Presentation navigation', 'previous': 'Previous slide', 'next': 'Next slide',
        'edit': 'Edit', 'overview': 'Overview', 'notes_button': 'Notes', 'appendix_button': 'Appendix slides',
        'replay': 'Replay animation', 'fullscreen': 'Fullscreen', 'print': 'Print',
        'notes_document': 'Notes document', 'materials': 'Materials', 'pdf': 'Download PDF',
        'help': '← → navigate · N notes · O overview', 'open_slide': 'Open slide',
        'sources': 'Sources', 'download_notes': 'Download notes',
        'code_notes': 'What the code means', 'notes_subtitle': 'Speaker notes · {main_count} main slides and {extra_count} appendix slides',
        'notes_intro': 'The main lecture and questions take 45 minutes. Appendix slides are available for questions and detailed reference.',
        'markdown_intro': '{main_count} main slides and {extra_count} appendix slides. The main lecture and questions take {minutes} minutes.',
        'markdown_scope': 'No live demonstration, in-class exercise or required homework. Appendix slides are outside the main lecture time.',
        'language_label': 'Switch to Turkish',
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def inline(value):
    value = esc(value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', value)


def clock(seconds):
    return f'{int(seconds)//60:02}:{int(seconds)%60:02}'


def embedded_json(data):
    """Keep JSON unchanged while preventing script-tag and line-separator parsing."""
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', r'\u003c').replace('\u2028', r'\u2028').replace('\u2029', r'\u2029')


def resource(value, prefix):
    """JSON paths are relative to the lecture root; EN pages are one level down."""
    value = str(value)
    if value.startswith(('/', '#')) or re.match(r'^[a-z][a-z0-9+.-]*:', value, re.I):
        return value
    return prefix + value


def source_links(slide):
    return ''.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a>' for s in slide.get('sources', []))


def bullets(slide):
    if not slide.get('bullets'):
        return ''
    tag = 'ol' if slide.get('layout') == 'steps' else 'ul'
    return f'<{tag} class="big-list">' + ''.join(f'<li data-edit-field="bullets" data-edit-index="{i}">{inline(b)}</li>' for i, b in enumerate(slide['bullets'])) + f'</{tag}>'


def code_lines(code):
    return re.split(r'\r?\n', code)


def codebox(code):
    lines = []
    for line in code_lines(code):
        cls = 'added' if line.startswith('+') else 'removed' if line.startswith('-') else ''
        lines.append(f'<span class="{cls}">{esc(line)}</span>')
    return '<pre class="codebox" data-edit-field="code"><code>' + '\n'.join(lines) + '</code></pre>'


def column_content(columns):
    return ''.join(f'<div class="column"><h3 data-edit-field="columns" data-edit-index="{i}" data-edit-part="heading">{esc(c["heading"])}</h3><p data-edit-field="columns" data-edit-index="{i}" data-edit-part="body">{inline(c["body"])}</p></div>' for i, c in enumerate(columns))


def code_notes(slide, editable=True):
    if not slide.get('codeNotes'):
        return ''
    items = []
    for i, note in enumerate(slide['codeNotes']):
        fields = f' data-edit-field="codeNotes" data-edit-index="{i}"' if editable else ''
        items.append(f'<li{fields}>{inline(note)}</li>')
    return '<ul class="code-notes">' + ''.join(items) + '</ul>'


def render_slide(slide, index, main_count, total_count, timing, lang, prefix):
    ui = UI[lang]
    appendix = slide.get('appendix', False)
    number = f'{ui["appendix"]} {index-main_count+1} / {total_count-main_count}' if appendix else f'{index+1} / {main_count}'
    title_tag = 'h1' if index == 0 else 'h2'
    theme = slide.get('theme', 'paper')
    layout = slide.get('layout', 'text')
    heading = f'<p class="eyebrow" data-edit-field="eyebrow">{esc(slide.get("eyebrow", ""))}</p><{title_tag} data-edit-field="title">{esc(slide["title"])}</{title_tag}>'
    lead = f'<p class="lead" data-edit-field="lead">{inline(slide["lead"])}</p>' if slide.get('lead') else ''
    if layout == 'cover':
        content = lead + (f'<p class="byline">Arif Solmaz<br>{esc(ui["byline"])}</p>' if index == 0 else bullets(slide))
        if slide.get('diagram'):
            content += f'<img class="diagram" src="{esc(resource(slide["diagram"],prefix))}" alt="{esc(slide.get("diagramAlt",ui["cover_alt"]))}">'
    elif slide.get('asset'):
        asset = slide['asset']
        poster = resource(f'assets/posters/{Path(asset["src"]).stem}.png', prefix)
        animation = resource(asset['src'], prefix)
        content = lead + f'<img src="{esc(poster)}" data-animation="{esc(animation)}" data-poster="{esc(poster)}" alt="{esc(asset["alt"])}" width="1920" height="1080">'
    elif slide.get('diagram'):
        content = lead + f'<img class="diagram" src="{esc(resource(slide["diagram"],prefix))}" alt="{esc(slide.get("diagramAlt",slide["title"]))}">' + bullets(slide)
    elif slide.get('code'):
        side = code_notes(slide) + bullets(slide)
        if slide.get('columns'):
            side += column_content(slide['columns'])
        explained = ' explained ' + ('side' if len(code_lines(slide['code'])) > 7 else 'stacked') if slide.get('codeNotes') else ''
        content = lead + (f'<div class="code-layout{explained}">{codebox(slide["code"])}<div class="code-support">{side}</div></div>' if side else codebox(slide['code']))
    elif slide.get('columns'):
        columns = slide['columns']
        content = lead + f'<div class="columns {"three" if len(columns)==3 else ""}">' + column_content(columns) + '</div>' + bullets(slide)
    else:
        content = lead + bullets(slide)
    if not slide.get('code') or slide.get('asset') or slide.get('diagram') or layout == 'cover':
        content += code_notes(slide)
    if slide.get('caption'):
        content += f'<p class="caption" data-edit-field="caption">{inline(slide["caption"])}</p>'
    if slide.get('visibleSources'):
        content += f'<div class="slide-links">{source_links(slide)}</div>'
    speech = f'{timing}\n\n{slide["notes"]}'
    reference_class = ' cheatsheet' if appendix and index == total_count-1 and layout == 'code' else ''
    cover_class = ' story-cover' if index == 0 and layout == 'cover' else ''
    sources_class = ' with-sources' if slide.get('visibleSources') else ''
    explanation_class = ' has-code-notes' if slide.get('codeNotes') else ''
    diagram_class = ' diagram-explained' if slide.get('diagram') and slide.get('codeNotes') and layout != 'cover' else ''
    return f'''<section id="{esc(slide['id'])}" class="{theme} {layout}{' appendix' if appendix else ''}{reference_class}{cover_class}{sources_class}{explanation_class}{diagram_class}" data-timing="{esc(timing)}" aria-hidden="true">
{heading}<div class="content">{content}</div>
<footer class="slide-footer"><span>{esc(ui['footer'])}</span><span>{esc(number)}</span></footer>
<aside><div class="speech">{esc(speech)}</div><div class="sources">{source_links(slide)}</div></aside>
</section>'''


def build(lang):
    source = ROOT / ('ders.json' if lang == 'tr' else 'lesson-en.json')
    data = json.loads(source.read_text())
    slides = data['slides']
    main_count = data['mainCount']
    assert isinstance(slides, list) and slides
    assert isinstance(main_count, int) and not isinstance(main_count, bool) and 0 < main_count <= len(slides)
    assert all(isinstance(s['duration'], int) and not isinstance(s['duration'], bool) and 0 <= s['duration'] <= (600 if i < main_count else 0) for i, s in enumerate(slides))
    assert sum(s['duration'] for s in slides[:main_count]) == 2700
    assert slides[main_count-1]['duration'] == 180, 'Keep three minutes for questions.'
    assert len({str(s['id']) for s in slides}) == len(slides)
    assert all(bool(s.get('appendix')) == (i >= main_count) for i, s in enumerate(slides))
    assert all('codeNotes' not in s or isinstance(s['codeNotes'], list) and len(s['codeNotes']) <= 100 and all(isinstance(note, str) and len(note) <= 10000 for note in s['codeNotes']) for s in slides)
    ui = {key: value.format(main_count=main_count, extra_count=len(slides)-main_count, minutes=sum(s['duration'] for s in slides[:main_count])//60) for key, value in UI[lang].items()}
    if lang == 'en':
        original = json.loads((ROOT / 'ders.json').read_text())
        assert main_count == original['mainCount'], 'Language links require matching lecture sections.'
        assert [s['id'] for s in slides] == [s['id'] for s in original['slides']], 'Language links require matching slide IDs.'
    prefix = '' if lang == 'tr' else '../'
    destination = ROOT if lang == 'tr' else ROOT / 'en'
    destination.mkdir(exist_ok=True)
    other_deck = 'en/' if lang == 'tr' else '../'
    other_notes = 'en/konusmaci-notlari.html' if lang == 'tr' else '../konusmaci-notlari.html'
    other_lang = 'EN' if lang == 'tr' else 'TR'
    material = resource('canli-ders/materyal.html', prefix) + ('#en' if lang == 'en' else '')
    pdf = resource(f'pdf/git-github-{lang}.pdf', prefix)
    cumulative = 0
    rendered = []
    note_sections = []
    markdown = [f'# {data["title"]}', '', ui['markdown_intro'], '', ui['markdown_scope'], '']
    for i, slide in enumerate(slides):
        if i < main_count:
            timing = f'{clock(cumulative)}–{clock(cumulative+slide["duration"])} · {slide["duration"]} {ui["seconds"]}'
            cumulative += slide['duration']
            label = str(i+1)
        else:
            timing = ui['appendix_timing']
            label = f'{ui["appendix"]} {i-main_count+1}'
        rendered.append(render_slide(slide, i, main_count, len(slides), timing, lang, prefix))
        annotations = f'<h3>{esc(ui["code_notes"])}</h3>{code_notes(slide, editable=False)}' if slide.get('codeNotes') else ''
        note_sections.append(f'<section id="not-{i+1}"><p class="time">{esc(timing)}</p><h2>{label}. {esc(slide["title"])}</h2><p>{esc(slide["notes"]).replace(chr(10),"<br>")}</p>{annotations}<div class="sources">{source_links(slide)}</div><a class="back" href="index.html#{esc(slide["id"])}">{esc(ui["open_slide"])}</a></section>')
        markdown.extend([f'## {label}. {slide["title"]}', '', timing, '', slide['notes'], ''])
        if slide.get('codeNotes'):
            markdown.extend([ui['code_notes'] + ':', '', *[f'- {note}' for note in slide['codeNotes']], ''])
        markdown.extend([ui['sources'] + ':', ''])
        markdown.extend([f'- [{s["title"]}]({s["url"]})' for s in slide.get('sources', [])])
        markdown.append('')
    document = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(data['title'])}</title><meta name="description" content="{esc(ui['description'])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600..800&family=IBM+Plex+Sans:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/lecture.css"><link rel="stylesheet" href="{prefix}assets/editor.css"></head><body data-lang="{lang}" data-prefix="{prefix}" data-main-count="{main_count}" data-storage-key="git-github-editor-felsefe-v4:{lang}">
<div id="ui-progress" aria-hidden="true"></div><main id="ui-viewport" aria-label="{esc(ui['lecture_label'])}"><div id="ui-stage">{''.join(rendered)}</div></main>
<div id="ui-notes" role="region" aria-label="{esc(ui['notes'])}" hidden><h3 id="ui-notes-title"></h3><div id="ui-notes-body"></div><div id="ui-notes-sources"></div></div>
<div id="ui-overview" role="dialog" aria-modal="true" aria-label="{esc(ui['all_slides'])}" hidden><div class="overview-top"><h2>{esc(ui['all_slides'])}</h2><button id="ui-close-ov">{esc(ui['return'])}</button></div><h3>{esc(ui['main_heading'])}</h3><div class="overview-grid" id="ui-main-grid"></div><h3>{esc(ui['extra_heading'])}</h3><div class="overview-grid" id="ui-extra-grid"></div></div>
<nav id="ui-bar" aria-label="{esc(ui['navigation'])}"><button id="ui-prev" aria-label="{esc(ui['previous'])}">←</button><span id="ui-count" aria-live="polite"></span><button id="ui-next" aria-label="{esc(ui['next'])}">→</button><button id="ui-btn-edit" aria-pressed="false">{esc(ui['edit'])}</button><button id="ui-btn-ov">{esc(ui['overview'])}</button><button id="ui-btn-notes" aria-pressed="false">{esc(ui['notes_button'])}</button><button id="ui-appendix">{esc(ui['appendix_button'])}</button><button id="ui-btn-replay">{esc(ui['replay'])}</button><button id="ui-btn-fs">{esc(ui['fullscreen'])}</button><button id="ui-btn-print">{esc(ui['print'])}</button><a id="ui-notes-document" href="konusmaci-notlari.html" target="_blank" rel="noopener">{esc(ui['notes_document'])}</a><a href="{material}">{esc(ui['materials'])}</a><a href="{pdf}" download>{esc(ui['pdf'])}</a><a data-language-link href="{other_deck}" aria-label="{esc(ui['language_label'])}" hreflang="{'en' if lang == 'tr' else 'tr'}">{other_lang}</a><span id="ui-help">{esc(ui['help'])}</span></nav>
<script id="lecture-data" type="application/json">{embedded_json(data)}</script>
<script src="{prefix}assets/lecture.js"></script><script src="{prefix}assets/editor.js"></script></body></html>'''
    (destination / 'index.html').write_text(document)
    note_document = f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(ui['notes'])} · {esc(ui['footer'])}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f4f1ea;color:#141b2b;font:19px/1.7 Arial,sans-serif}}main{{max-width:900px;margin:auto;padding:56px 28px}}h1{{font-size:44px;line-height:1.15}}h2{{font-size:28px;line-height:1.25}}a{{color:#a43f20}}section{{padding:38px 0;border-bottom:1px solid #cfc7ba;break-inside:avoid}}.time{{font-size:15px;color:#626d7d}}.sources{{display:flex;flex-direction:column;font-size:14px;gap:5px}}.back{{display:inline-block;margin-top:14px;font-size:14px}}nav{{display:flex;gap:24px;flex-wrap:wrap}}@media print{{body{{background:white;font-size:13pt}}main{{padding:0;max-width:none}}nav,.back{{display:none}}section{{padding:20px 0}}}}@page{{size:A4;margin:18mm}}
</style></head><body><main><nav><a href="index.html">{esc(ui['return'])}</a><a href="egitmen-rehberi.md" download>{esc(ui['download_notes'])}</a><a href="{pdf}" download>{esc(ui['pdf'])}</a><a id="notes-language-link" href="{other_notes}" hreflang="{'en' if lang == 'tr' else 'tr'}" aria-label="{esc(ui['language_label'])}">{other_lang}</a></nav><h1>{esc(data['title'])}</h1><p>{esc(ui['notes_subtitle'])}</p><p>{esc(ui['notes_intro'])}</p>{''.join(note_sections)}</main><script>(()=>{{const link=document.getElementById('notes-language-link'),base=link.getAttribute('href');const update=()=>link.setAttribute('href',base+location.hash);window.addEventListener('hashchange',update);update();}})();</script></body></html>'''
    (destination / 'konusmaci-notlari.html').write_text(note_document)
    (destination / 'egitmen-rehberi.md').write_text('\n'.join(markdown))
    print(f'Built {lang}: {len(slides)} slides, {main_count} main, {cumulative}s. Notes: {sum(len(s["notes"].split()) for s in slides)} words.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=['tr', 'en', 'all'], default='all')
    args = parser.parse_args()
    for lang in ['tr', 'en'] if args.language == 'all' else [args.language]:
        if lang == 'en' and args.language == 'all' and not (ROOT / 'lesson-en.json').exists():
            print('English source lesson-en.json is not available yet; built Turkish only.')
            continue
        build(lang)


if __name__ == '__main__':
    main()
