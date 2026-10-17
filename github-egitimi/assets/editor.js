(() => {
  'use strict';
  const embedded = document.getElementById('lecture-data');
  const stage = document.getElementById('ui-stage');
  const toggle = document.getElementById('ui-btn-edit');
  if (!embedded || !stage || !toggle) return;
  const lang = document.body.dataset.lang || document.documentElement.lang || 'tr';
  const english = lang === 'en';
  const ui = english ? {
    editor: 'Edit presentation', close: 'Close editor', instruction: 'Click text on a slide or change a field on the right.',
    storage: 'Changes are saved in this browser. Download HTML to share them.',
    title: 'Title', eyebrow: 'Section label', lead: 'Introduction', bullets: 'List · one item per line',
    columns: 'Column', heading: 'Heading', body: 'Text', code: 'Code', codeNotes: 'What the code means · one explanation per line', codeNotesHeading: 'What the code means', caption: 'Caption', notes: 'Speaker notes',
    duration: 'Duration · seconds', theme: 'Background', paper: 'Light', dark: 'Dark', coral: 'Orange',
    main: 'Main lecture', appendix: 'Appendix', total: 'Main lecture time', seconds: 'seconds',
    undo: 'Undo', redo: 'Redo', json: 'Download edit file', html: 'Download HTML', import: 'Open edit file',
    notesDownload: 'Download notes', print: 'Print / save PDF', reset: 'Restore original presentation',
    resetHint: 'This browser’s draft will be replaced with the original. Download an edit file or HTML first if you want to keep it.',
    confirmReset: 'Restore original', cancel: 'Cancel', original: 'Original presentation restored.',
    saved: 'Saved in this browser.', loaded: 'Your saved draft has been restored.', imported: 'The edit file has been opened and saved.',
    memory: 'Changes are kept in memory. Browser storage is unavailable or full; download HTML or an edit file to keep them.',
    invalid: 'The edit file could not be opened. Choose an export for this language and this presentation.',
    storageInvalid: 'The saved draft is incompatible. The original presentation is shown; opening a valid edit file will replace that draft.',
    number: 'Enter a whole number from 0 to 600 seconds.', download: 'Download prepared.',
    hints: 'Use **bold** or `code` in paragraphs and list items. Current PDF: Print → Save as PDF.',
    baseline: 'After editing, the notes and PDF buttons use your draft. Download HTML to share the edited presentation.',
    createPdf: 'Create PDF', current: 'Slide', errors: 'Please check the field value.',
    overflow: 'Some text does not fit on this slide. Shorten the text.', currentNotes: 'Open the notes for your edited presentation.',
    listLimit: 'Use at most 100 list items, with at most 10,000 characters per item.',
    deckLimit: 'The presentation has too much text to save in an edit file. Shorten the longest passages.'
  } : {
    editor: 'Sunumu düzenle', close: 'Düzenleyiciyi kapat', instruction: 'Metne tıklayın veya sağdaki alanı değiştirin.',
    storage: 'Değişiklikler bu tarayıcıda kaydedilir. Paylaşmak için HTML indirin.',
    title: 'Başlık', eyebrow: 'Bölüm etiketi', lead: 'Giriş metni', bullets: 'Liste · her satır bir madde',
    columns: 'Sütun', heading: 'Başlık', body: 'Metin', code: 'Kod', codeNotes: 'Kodun anlamı · her satır bir açıklama', codeNotesHeading: 'Kodun anlamı', caption: 'Açıklama', notes: 'Konuşmacı notları',
    duration: 'Süre · saniye', theme: 'Arka plan', paper: 'Açık', dark: 'Koyu', coral: 'Turuncu',
    main: 'Ana anlatım', appendix: 'Ek', total: 'Ana anlatım süresi', seconds: 'saniye',
    undo: 'Geri al', redo: 'Yinele', json: 'Düzenleme dosyasını indir', html: 'HTML indir', import: 'Dosyadan aç',
    notesDownload: 'Notları indir', print: 'Yazdır / PDF kaydet', reset: 'Özgün sunuma geri dön',
    resetHint: 'Bu tarayıcıdaki taslak özgün sunumla değiştirilecek. Saklamak isterseniz önce düzenleme dosyası veya HTML indirin.',
    confirmReset: 'Özgün sunuma dön', cancel: 'Vazgeç', original: 'Özgün sunuma dönüldü.',
    saved: 'Bu tarayıcıda kaydedildi.', loaded: 'Kaydedilmiş taslağınız açıldı.', imported: 'Düzenleme dosyası açıldı ve kaydedildi.',
    memory: 'Değişiklikler bellekte tutuluyor. Tarayıcı depolaması kullanılamıyor veya dolu; saklamak için HTML veya düzenleme dosyası indirin.',
    invalid: 'Düzenleme dosyası açılamadı. Bu dil ve bu sunum için dışa aktarılmış bir dosya seçin.',
    storageInvalid: 'Kaydedilmiş taslak uyumlu değil. Özgün sunum gösteriliyor; geçerli bir düzenleme dosyası açmak taslağı değiştirir.',
    number: '0 ile 600 arasında bir tam saniye değeri girin.', download: 'İndirme hazırlandı.',
    hints: 'Paragraf ve listelerde **kalın** veya `kod` kullanabilirsiniz. Güncel PDF için Yazdır → PDF olarak kaydet.',
    baseline: 'Düzenlemeden sonra not ve PDF düğmeleri taslağınızı kullanır. Düzenlenmiş sunumu paylaşmak için HTML indirin.',
    createPdf: 'PDF oluştur', current: 'Slayt', errors: 'Alan değerini kontrol edin.',
    overflow: 'Bu slayttaki metinler alana sığmıyor. Metni kısaltın.', currentNotes: 'Düzenlenmiş sunumun notlarını açın.',
    listLimit: 'En fazla 100 liste maddesi ve her maddede en fazla 10.000 karakter kullanın.',
    deckLimit: 'Sunumda düzenleme dosyasına sığmayacak kadar metin var. En uzun metinleri kısaltın.'
  };
  const copy = value => JSON.parse(JSON.stringify(value));
  let original;
  try { original = JSON.parse(embedded.textContent); } catch { return; }
  if (!Array.isArray(original.slides) || !original.slides.length || !Number.isInteger(original.mainCount) || original.mainCount < 1 || original.mainCount > original.slides.length || stage.children.length !== original.slides.length) return;
  original = { title: original.title, mainCount: original.mainCount, slides: original.slides };
  const mainCount = original.mainCount, totalSlides = original.slides.length;
  let data = copy(original);
  let index = Math.max(0, Array.from(stage.children).findIndex(s => s.classList.contains('active')));
  let open = false, focusReturn = null, editGroup = null, restoring = false;
  const undo = [], redo = [];
  const storageKey = document.body.dataset.storageKey || `git-github-editor-felsefe-v4:${lang}${document.body.dataset.deckId ? ':' + document.body.dataset.deckId : ''}`;
  const canonicalRoot = 'https://arifsolmaz.github.io/github-egitimi/';
  const canonicalPage = canonicalRoot + (english ? 'en/' : '');
  const prefix = document.body.dataset.prefix || (english ? '../' : '');
  const sectionNodes = Array.from(stage.children);
  const pdfLabels = new Map(Array.from(document.querySelectorAll('a[href*="pdf/git-github-"]'), a => [a, { text: a.textContent, download: a.getAttribute('download') }]));
  const notesLink = document.getElementById('ui-notes-document');
  const originalNotesLabel = notesLink?.textContent;
  const allowedSlideKeys = new Set(['id', 'title', 'eyebrow', 'theme', 'layout', 'lead', 'caption', 'notes', 'duration', 'sources', 'appendix', 'diagram', 'diagramAlt', 'asset', 'bullets', 'columns', 'code', 'codeNotes', 'visibleSources']);
  const textKeys = ['title', 'eyebrow', 'lead', 'caption', 'notes', 'code'];
  const text = (value, maximum = 200000) => typeof value === 'string' && value.length <= maximum;
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  function validateImport(input) {
    if (!object(input) || input.schemaVersion !== 1 || input.language !== lang || input.mainCount !== mainCount || !text(input.title, 2000) || !Array.isArray(input.slides) || input.slides.length !== totalSlides) throw Error('Invalid deck');
    if (new TextEncoder().encode(JSON.stringify(input, null, 2)).length > 4000000) throw Error('Deck size limit');
    if (Object.keys(input).some(k => !['schemaVersion', 'language', 'title', 'mainCount', 'slides'].includes(k))) throw Error('Unknown deck property');
    const result = { title: input.title, mainCount, slides: [] };
    input.slides.forEach((slide, i) => {
      const source = original.slides[i];
      if (!object(slide) || Object.keys(slide).some(k => !allowedSlideKeys.has(k)) || slide.id !== source.id || slide.layout !== source.layout || slide.appendix !== (i >= mainCount)) throw Error('Invalid slide metadata');
      if (!['paper', 'dark', 'coral'].includes(slide.theme) || !Number.isInteger(slide.duration) || slide.duration < 0 || slide.duration > (i < mainCount ? 600 : 0)) throw Error('Invalid slide settings');
      if (!text(slide.title, 2000) || !text(slide.notes)) throw Error('Invalid required text');
      textKeys.forEach(k => { if (slide[k] !== undefined && !text(slide[k], k === 'code' ? 100000 : 200000)) throw Error('Invalid text'); });
      if (slide.bullets !== undefined && (!Array.isArray(slide.bullets) || slide.bullets.length > 100 || slide.bullets.some(v => !text(v, 10000)))) throw Error('Invalid list');
      if (slide.codeNotes !== undefined && (!Array.isArray(slide.codeNotes) || slide.codeNotes.length > 100 || slide.codeNotes.some(v => !text(v, 10000)))) throw Error('Invalid code notes');
      if ((slide.columns?.length || 0) !== (source.columns?.length || 0)) throw Error('Invalid columns');
      if (slide.columns !== undefined && (!Array.isArray(slide.columns) || slide.columns.some(c => !object(c) || Object.keys(c).some(k => !['heading', 'body'].includes(k)) || !text(c.heading, 2000) || !text(c.body, 20000)))) throw Error('Invalid column text');
      if (slide.diagram !== source.diagram || slide.diagramAlt !== source.diagramAlt) throw Error('Asset metadata cannot change');
      if (JSON.stringify(slide.asset) !== JSON.stringify(source.asset)) throw Error('Animation metadata cannot change');
      if (slide.visibleSources !== source.visibleSources) throw Error('Source display cannot change');
      if (!Array.isArray(slide.sources) || slide.sources.length > 100 || slide.sources.some(s => {
        if (!object(s) || Object.keys(s).some(k => !['title', 'url'].includes(k)) || !text(s.title, 2000) || !text(s.url, 4000)) return true;
        try { const url = new URL(s.url); return !['http:', 'https:'].includes(url.protocol); } catch { return true; }
      })) throw Error('Invalid sources');
      const clean = copy(source);
      textKeys.forEach(k => { if (slide[k] !== undefined) clean[k] = slide[k]; else delete clean[k]; });
      ['bullets', 'columns'].forEach(k => { if (slide[k] !== undefined) clean[k] = copy(slide[k]); else delete clean[k]; });
      if (slide.codeNotes !== undefined) clean.codeNotes = copy(slide.codeNotes);
      clean.theme = slide.theme; clean.duration = slide.duration; clean.sources = copy(slide.sources);
      result.slides.push(clean);
    });
    return result;
  }
  function payload(value = data) { return { schemaVersion: 1, language: lang, title: value.title, mainCount: value.mainCount, slides: copy(value.slides) }; }
  function node(tag, className, value) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (value !== undefined) element.textContent = value;
    return element;
  }
  function inline(element, value) {
    // Matches the builder's small formatting vocabulary without interpreting HTML.
    const input = String(value || '');
    const pieces = input.split(/(`[^`]+`)/g);
    pieces.forEach(piece => {
      if (piece.startsWith('`') && piece.endsWith('`') && piece.length > 2) {
        element.append(node('code', '', piece.slice(1, -1))); return;
      }
      const parts = piece.split(/(\*\*[^*]+\*\*)/g);
      parts.forEach(part => element.append(part.startsWith('**') && part.endsWith('**') && part.length > 4 ? node('strong', '', part.slice(2, -2)) : document.createTextNode(part)));
    });
    return element;
  }
  function editable(element, field) { element.dataset.editorField = field; return element; }
  function resource(path) {
    if (document.body.dataset.assetBase) return new URL(path, document.body.dataset.assetBase).href;
    return /^(?:[a-z][a-z0-9+.-]*:|\/|#)/i.test(path) ? path : prefix + path;
  }
  function clock(seconds) { return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`; }
  function timings(value = data) {
    let cumulative = 0;
    return value.slides.map((slide, i) => {
      if (i >= value.mainCount) return english ? 'Appendix slide · outside the main lecture time' : 'Ek slayt · ana anlatım süresinin dışında';
      const start = cumulative; cumulative += slide.duration;
      return `${clock(start)}–${clock(cumulative)} · ${slide.duration} ${ui.seconds}`;
    });
  }
  function sources(slide) {
    const result = document.createDocumentFragment();
    (slide.sources || []).forEach(source => {
      const link = node('a', '', source.title); link.href = source.url; link.target = '_blank'; link.rel = 'noopener'; result.append(link);
    });
    return result;
  }
  function list(slide) {
    if (!slide.bullets?.length) return null;
    const result = editable(node(slide.layout === 'steps' ? 'ol' : 'ul', 'big-list'), 'bullets');
    slide.bullets.forEach(value => result.append(inline(node('li'), value)));
    return result;
  }
  function columns(slide, wrapper = true) {
    const result = wrapper ? node('div', `columns${slide.columns.length === 3 ? ' three' : ''}`) : document.createDocumentFragment();
    slide.columns.forEach((column, i) => {
      const item = node('div', 'column');
      item.append(editable(node('h3', '', column.heading), `columns.${i}.heading`), editable(inline(node('p'), column.body), `columns.${i}.body`));
      result.append(item);
    });
    return result;
  }
  function codebox(value) {
    const result = editable(node('pre', 'codebox'), 'code');
    const code = node('code');
    value.split(/\r?\n/).forEach((line, i) => {
      if (i) code.append(document.createTextNode('\n'));
      code.append(node('span', line.startsWith('+') ? 'added' : line.startsWith('-') ? 'removed' : '', line));
    });
    result.append(code); return result;
  }
  function codeNotes(slide, editing = true) {
    if (!slide.codeNotes?.length) return null;
    const result = node('ul', 'code-notes');
    if (editing) editable(result, 'codeNotes');
    slide.codeNotes.forEach(value => result.append(inline(node('li'), value)));
    return result;
  }
  function renderSlide(i) {
    const slide = data.slides[i], section = sectionNodes[i], active = section.classList.contains('active');
    const wasUrl = section.querySelector('img[data-blob-url]')?.dataset.blobUrl;
    if (wasUrl) URL.revokeObjectURL(wasUrl);
    section.className = `${slide.theme} ${slide.layout}${slide.appendix ? ' appendix' : ''}${slide.appendix && i === totalSlides - 1 && slide.layout === 'code' ? ' cheatsheet' : ''}${i === 0 && slide.layout === 'cover' ? ' story-cover' : ''}${slide.visibleSources ? ' with-sources' : ''}${slide.codeNotes?.length ? ' has-code-notes' : ''}${slide.diagram && slide.codeNotes?.length && slide.layout !== 'cover' ? ' diagram-explained' : ''}${active ? ' active' : ''}`;
    section.id = String(slide.id);
    const heading = editable(node(i === 0 ? 'h1' : 'h2', '', slide.title), 'title');
    const eyebrow = editable(node('p', 'eyebrow', slide.eyebrow || ''), 'eyebrow');
    const content = node('div', 'content');
    if (slide.lead) content.append(editable(inline(node('p', 'lead'), slide.lead), 'lead'));
    const bullets = () => { const element = list(slide); if (element) content.append(element); };
    const diagram = () => { const img = node('img', 'diagram'); img.src = resource(slide.diagram); img.alt = slide.diagramAlt || (i === 0 ? (english ? 'Git branch and main workflow' : 'Git dalı ve ana akış') : slide.title); content.append(img); };
    if (slide.layout === 'cover') {
      if (i === 0) { const byline = node('p', 'byline'); byline.append(document.createTextNode('Arif Solmaz'), node('br'), document.createTextNode(english ? 'İSTÜN Mechatronics Engineering' : 'İSTÜN Mekatronik Mühendisliği')); content.append(byline); }
      else bullets();
      if (slide.diagram) diagram();
    } else if (slide.asset) {
      const image = node('img');
      const stem = slide.asset.src.split('/').pop().replace(/\.[^.]+$/, '');
      image.dataset.animation = resource(slide.asset.src); image.dataset.poster = resource(`assets/posters/${stem}.png`);
      image.src = image.dataset.poster; image.alt = slide.asset.alt; image.width = 1920; image.height = 1080; content.append(image);
    } else if (slide.diagram) { diagram(); bullets(); }
    else if (slide.code) {
      if (slide.bullets?.length || slide.columns?.length || slide.codeNotes?.length) {
        const explained = slide.codeNotes?.length ? ` explained ${slide.code.split(/\r?\n/).length > 7 ? 'side' : 'stacked'}` : '';
        const row = node('div', `code-layout${explained}`), side = node('div', 'code-support'), items = list(slide), annotations = codeNotes(slide);
        if (annotations) side.append(annotations);
        if (items) side.append(items);
        if (slide.columns?.length) side.append(columns(slide, false));
        row.append(codebox(slide.code), side); content.append(row);
      } else content.append(codebox(slide.code));
    } else if (slide.columns?.length) { content.append(columns(slide)); bullets(); }
    else bullets();
    if (!slide.code || slide.asset || slide.diagram || slide.layout === 'cover') {
      const annotations = codeNotes(slide); if (annotations) content.append(annotations);
    }
    if (slide.caption) content.append(editable(inline(node('p', 'caption'), slide.caption), 'caption'));
    if (slide.visibleSources) { const links = node('div', 'slide-links'); links.append(sources(slide)); content.append(links); }
    const footer = node('footer', 'slide-footer');
    footer.append(node('span', '', english ? 'Git and GitHub' : 'Git ve GitHub'), node('span', '', i < data.mainCount ? `${i + 1} / ${data.mainCount}` : `${ui.appendix} ${i - data.mainCount + 1} / ${data.slides.length - data.mainCount}`));
    const aside = node('aside');
    const speech = node('div', 'speech'), links = node('div', 'sources'); links.append(sources(slide)); aside.append(speech, links);
    section.replaceChildren(eyebrow, heading, content, footer, aside);
  }
  function updateTimings() {
    const times = timings();
    sectionNodes.forEach((section, i) => { section.querySelector('.speech').textContent = `${times[i]}\n\n${data.slides[i].notes}`; section.dataset.timing = times[i]; });
    const seconds = data.slides.slice(0, data.mainCount).reduce((sum, s) => sum + s.duration, 0);
    total.textContent = `${ui.total}: ${clock(seconds)}`; document.body.dataset.totalDuration = String(seconds);
    const overviewTitle = document.getElementById('ui-main-grid')?.previousElementSibling;
    if (overviewTitle?.tagName === 'H3') overviewTitle.textContent = `${ui.main} · ${data.mainCount} ${english ? 'slides' : 'slayt'} · ${clock(seconds)}`;
  }
  function modified() { return Boolean(document.body.dataset.deckId) || JSON.stringify(data) !== JSON.stringify(original); }
  function updateLabels() {
    const changed = modified(); document.body.dataset.customDraft = String(changed);
    pdfLabels.forEach((originalLink, link) => {
      link.textContent = changed ? ui.createPdf : originalLink.text; link.title = changed ? ui.hints : '';
      if (changed || originalLink.download === null) link.removeAttribute('download'); else link.setAttribute('download', originalLink.download);
    });
    if (notesLink) { notesLink.textContent = originalNotesLabel; notesLink.title = changed ? ui.currentNotes : ''; }
    undoButton.disabled = !undo.length; redoButton.disabled = !redo.length;
  }
  function refresh(all = false) {
    if (all) data.slides.forEach((_, i) => renderSlide(i)); else renderSlide(index);
    updateTimings(); updateLabels();
    document.dispatchEvent(new CustomEvent('lecture:refresh', { detail: { index } }));
    requestAnimationFrame(checkFit);
  }
  function setStatus(message, error = false) { status.textContent = message; status.classList.toggle('error', error); }
  function save(message = ui.saved) {
    try { localStorage.setItem(storageKey, JSON.stringify(payload())); setStatus(message); }
    catch { setStatus(ui.memory, true); }
  }
  function remember() { undo.push(copy(data)); if (undo.length > 50) undo.shift(); redo.length = 0; }
  function updateField(field, value) {
    if (field === 'duration' && (!Number.isInteger(value) || value < 0 || value > 600)) { setStatus(ui.number, true); return; }
    const slide = data.slides[index];
    const path = field.split('.');
    let target = slide;
    while (path.length > 1) target = target[path.shift()];
    const key = path[0];
    const listField = field === 'bullets' || field === 'codeNotes';
    const normalized = listField ? value.split(/\r?\n/).filter(line => line.trim()) : value;
    if (JSON.stringify(target[key]) === JSON.stringify(normalized)) return;
    const candidate = copy(data);
    const candidatePath = field.split('.'); let candidateTarget = candidate.slides[index];
    while (candidatePath.length > 1) candidateTarget = candidateTarget[candidatePath.shift()];
    candidateTarget[candidatePath[0]] = normalized;
    try { validateImport(payload(candidate)); }
    catch (error) { setStatus(error.message === 'Deck size limit' ? ui.deckLimit : listField ? ui.listLimit : ui.errors, true); return; }
    if (!editGroup) { remember(); editGroup = `${index}:${field}`; }
    data = candidate;
    refresh(); save();
  }
  const panel = node('aside'); panel.id = 'lecture-editor'; panel.hidden = true; panel.setAttribute('aria-label', ui.editor);
  const header = node('div', 'editor-header'), heading = node('h2', '', ui.editor);
  const close = node('button', '', '×'); close.type = 'button'; close.setAttribute('aria-label', ui.close);
  header.append(heading, close);
  const instruction = node('p', 'editor-help', ui.instruction);
  const slideLabel = node('p', 'editor-slide-label'); slideLabel.id = 'editor-slide-label';
  const total = node('p', 'editor-total'); total.id = 'editor-total';
  const actions = node('div', 'editor-actions');
  function action(label, handler) { const button = node('button', '', label); button.type = 'button'; button.addEventListener('click', handler); actions.append(button); return button; }
  const undoButton = action(ui.undo, () => historyStep(undo, redo)); undoButton.id = 'editor-undo';
  const redoButton = action(ui.redo, () => historyStep(redo, undo)); redoButton.id = 'editor-redo';
  action(ui.json, () => download(JSON.stringify(payload(), null, 2), 'application/json;charset=utf-8', `git-github-${lang}.json`));
  action(ui.html, exportHtml).dataset.action = 'html';
  action(ui.notesDownload, exportNotes);
  action(ui.print, () => window.print());
  const importInput = node('input'); importInput.type = 'file'; importInput.accept = '.json,application/json'; importInput.hidden = true; importInput.id = 'editor-import-file';
  action(ui.import, () => importInput.click());
  const resetButton = action(ui.reset, () => { resetConfirm.hidden = false; confirmButton.focus(); });
  const resetConfirm = node('div', 'editor-reset-confirm'); resetConfirm.hidden = true;
  resetConfirm.append(node('p', '', ui.resetHint));
  const confirmButton = node('button', '', ui.confirmReset); confirmButton.type = 'button';
  const cancelButton = node('button', '', ui.cancel); cancelButton.type = 'button';
  resetConfirm.append(confirmButton, cancelButton);
  confirmButton.addEventListener('click', () => {
    remember(); data = copy(original); editGroup = null; refresh(true); buildFields(); resetConfirm.hidden = true;
    try { localStorage.removeItem(storageKey); setStatus(ui.original); } catch { setStatus(ui.memory, true); }
    resetButton.focus();
  });
  cancelButton.addEventListener('click', () => { resetConfirm.hidden = true; resetButton.focus(); });
  const fields = node('div', 'editor-fields'); fields.id = 'editor-fields';
  const status = node('p', 'editor-status'); status.id = 'editor-status'; status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
  const fitWarning = node('p', 'editor-fit-warning'); fitWarning.id = 'editor-fit-warning'; fitWarning.hidden = true; fitWarning.setAttribute('role', 'status');
  panel.append(header, instruction, slideLabel, total, actions, importInput, resetConfirm, fitWarning, fields, node('p', 'editor-help', ui.hints), node('p', 'editor-help', ui.baseline), node('p', 'editor-help', ui.storage), status);
  document.body.append(panel);
  toggle.setAttribute('aria-controls', panel.id); toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-pressed', 'false');
  const fieldElements = new Map();
  function field(label, path, value, kind = 'text') {
    const wrapper = node('div', 'editor-field'), labelNode = node('label', '', label);
    const id = `editor-field-${path.replace(/\./g, '-')}`;
    const control = node(kind === 'textarea' ? 'textarea' : kind === 'select' ? 'select' : 'input');
    control.id = id; labelNode.htmlFor = id;
    if (kind === 'select') {
      [['paper', ui.paper], ['dark', ui.dark], ['coral', ui.coral]].forEach(([key, caption]) => { const option = node('option', '', caption); option.value = key; control.append(option); });
    } else if (kind !== 'textarea') control.type = kind;
    if (kind === 'textarea') control.rows = path === 'notes' ? 7 : path === 'code' ? 6 : 3;
    if (kind === 'number') { control.min = '0'; control.max = '600'; control.step = '1'; }
    if (kind === 'textarea' || kind === 'text') {
      control.maxLength = path === 'title' || /\.heading$/.test(path) ? 2000 : path === 'code' ? 100000 : /\.body$/.test(path) ? 20000 : ['bullets', 'codeNotes'].includes(path) ? 1000100 : 200000;
    }
    control.value = value ?? ''; control.dataset.editorPath = path; control.dataset.field = path;
    control.addEventListener('input', () => updateField(path, kind === 'number' ? control.valueAsNumber : control.value));
    control.addEventListener('focus', () => { editGroup = null; });
    control.addEventListener('blur', () => { editGroup = null; });
    wrapper.append(labelNode, control); fields.append(wrapper); fieldElements.set(path, control);
  }
  function buildFields() {
    fields.replaceChildren(); fieldElements.clear(); editGroup = null;
    const slide = data.slides[index];
    slideLabel.textContent = `${index < data.mainCount ? ui.current + ' ' + (index + 1) : ui.appendix + ' ' + (index - data.mainCount + 1)} · ${slide.title}`;
    field(ui.title, 'title', slide.title); field(ui.eyebrow, 'eyebrow', slide.eyebrow || '');
    field(ui.lead, 'lead', slide.lead || '', 'textarea');
    if (!slide.asset && !(slide.layout === 'cover' && index === 0)) field(ui.bullets, 'bullets', (slide.bullets || []).join('\n'), 'textarea');
    (slide.columns || []).forEach((column, i) => { field(`${ui.columns} ${i + 1} · ${ui.heading}`, `columns.${i}.heading`, column.heading); field(`${ui.columns} ${i + 1} · ${ui.body}`, `columns.${i}.body`, column.body, 'textarea'); });
    if ('code' in slide) field(ui.code, 'code', slide.code || '', 'textarea');
    field(ui.codeNotes, 'codeNotes', (slide.codeNotes || []).join('\n'), 'textarea');
    field(ui.caption, 'caption', slide.caption || '', 'textarea');
    field(ui.notes, 'notes', slide.notes, 'textarea');
    if (index < data.mainCount) field(ui.duration, 'duration', slide.duration, 'number');
    field(ui.theme, 'theme', slide.theme, 'select');
  }
  function historyStep(from, to) {
    if (!from.length) return;
    to.push(copy(data)); data = from.pop(); editGroup = null; refresh(true); buildFields(); save();
  }
  function setOpen(value) {
    open = value; panel.hidden = !value; document.body.classList.toggle('editing', value);
    toggle.setAttribute('aria-expanded', String(value)); toggle.setAttribute('aria-pressed', String(value)); editGroup = null;
    if (value) { focusReturn = document.activeElement; buildFields(); close.focus(); }
    else { resetConfirm.hidden = true; focusReturn?.focus(); }
    window.dispatchEvent(new Event('resize'));
    document.dispatchEvent(new CustomEvent('lecture:refresh', { detail: { index } }));
    requestAnimationFrame(checkFit);
  }
  function checkFit() {
    const section = sectionNodes[index], bounds = section.getBoundingClientRect();
    const footer = section.querySelector('footer').getBoundingClientRect();
    const heading = section.querySelector('h1,h2').getBoundingClientRect();
    const scale = bounds.width / 1920;
    const overflow = Array.from(section.querySelectorAll('[data-editor-field],.codebox code,.code-notes li,.content img')).some(element => {
      const box = element.getBoundingClientRect();
      return box.height > 0 && (box.bottom > footer.top - 8 * scale || box.right > bounds.right - 100 * scale || box.left < bounds.left + 100 * scale || (element.closest('.content') && box.top < heading.bottom + 12 * scale));
    });
    fitWarning.hidden = !overflow; fitWarning.textContent = overflow ? ui.overflow : '';
  }
  toggle.addEventListener('click', () => setOpen(!open)); close.addEventListener('click', () => setOpen(false));
  document.addEventListener('lecture:slidechange', event => {
    if (restoring) return;
    const next = Number(event.detail?.index);
    if (!Number.isInteger(next) || next < 0 || next >= data.slides.length || next === index) return;
    index = next; editGroup = null; if (open) buildFields(); requestAnimationFrame(checkFit);
  });
  stage.addEventListener('click', event => {
    if (!open) return;
    const item = event.target.closest('[data-editor-field]');
    if (!item || !item.closest('section.active')) return;
    const control = fieldElements.get(item.dataset.editorField);
    if (control) { event.preventDefault(); control.focus(); control.scrollIntoView({ block: 'nearest' }); }
  });
  document.addEventListener('keydown', event => {
    if (!open || event.key !== 'Escape' || !document.getElementById('ui-overview')?.hidden) return;
    event.preventDefault(); event.stopImmediatePropagation(); setOpen(false);
  }, true);
  panel.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z') {
      event.preventDefault(); historyStep(event.shiftKey ? redo : undo, event.shiftKey ? undo : redo);
    }
  });
  importInput.addEventListener('change', async () => {
    const file = importInput.files?.[0]; importInput.value = ''; if (!file) return;
    try {
      if (file.size > 4000000) throw Error('File too large');
      const incoming = validateImport(JSON.parse(await file.text()));
      remember(); data = incoming; editGroup = null; refresh(true); buildFields(); save(ui.imported);
    } catch { setStatus(ui.invalid, true); }
  });
  function download(content, type, filename) {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const link = node('a'); link.href = url; link.download = filename; document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10000); setStatus(ui.download);
  }
  function exportHtml() {
    const clone = document.documentElement.cloneNode(true), body = clone.querySelector('body');
    clone.querySelector('#lecture-editor')?.remove(); body.classList.remove('editing');
    clone.querySelectorAll('[contenteditable]').forEach(e => e.removeAttribute('contenteditable'));
    clone.querySelectorAll('[data-editor-field]').forEach(e => e.removeAttribute('data-editor-field'));
    clone.querySelector('#ui-btn-edit')?.setAttribute('aria-expanded', 'false');
    clone.querySelector('#ui-btn-edit')?.setAttribute('aria-pressed', 'false');
    clone.querySelector('#ui-notes')?.setAttribute('hidden', ''); clone.querySelector('#ui-overview')?.setAttribute('hidden', '');
    clone.querySelectorAll('.overview-grid').forEach(e => e.replaceChildren());
    clone.querySelectorAll('img[data-animation]').forEach(img => { img.src = img.dataset.poster; img.removeAttribute('data-blob-url'); });
    body.dataset.assetBase = canonicalRoot;
    body.dataset.notesBase = canonicalPage + 'konusmaci-notlari.html';
    const snapshot = globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    body.dataset.deckId = snapshot; body.dataset.storageKey = `git-github-editor-felsefe-v4:${lang}:${snapshot}`;
    clone.querySelector('#lecture-data').textContent = JSON.stringify(payload()).replace(/</g, '\\u003c');
    clone.querySelectorAll('[src],[href],[data-animation],[data-poster]').forEach(element => {
      ['src', 'href', 'data-animation', 'data-poster'].forEach(attribute => {
        const value = element.getAttribute(attribute);
        if (!value || value.startsWith('#') || /^(?:data:|mailto:|tel:)/i.test(value)) return;
        try { element.setAttribute(attribute, new URL(value, canonicalPage).href); } catch { /* Existing metadata is fixed and trusted. */ }
      });
    });
    clone.querySelectorAll('base').forEach(e => e.remove());
    download('<!doctype html>\n' + clone.outerHTML, 'text/html;charset=utf-8', `git-github-${lang}-${english ? 'edited' : 'duzenlenmis'}.html`);
  }
  function exportNotes() {
    download(notesHtml(), 'text/html;charset=utf-8', `git-github-${lang}-${english ? 'notes' : 'notlar'}.html`);
  }
  function notesHtml() {
    const html = document.createElement('html'); html.lang = lang;
    const head = node('head'), charset = node('meta'); charset.setAttribute('charset', 'utf-8');
    const viewport = node('meta'); viewport.name = 'viewport'; viewport.content = 'width=device-width, initial-scale=1';
    const style = node('style', '', 'body{font:18px/1.6 Arial,sans-serif;color:#172033;background:#fff;max-width:960px;margin:40px auto;padding:0 24px}h1{font-size:34px;line-height:1.2}h2{font-size:25px}section{padding:26px 0;border-top:1px solid #d4d8df}.speech{white-space:pre-wrap}.timing{font-size:15px;color:#576174}.sources{display:flex;flex-wrap:wrap;gap:10px 22px;font-size:15px}a{color:#a43f20}@media print{body{margin:0;max-width:none}section{break-inside:avoid}}');
    head.append(charset, viewport, node('title', '', `${data.title} · ${ui.notes}`), style);
    const body = node('body'); body.append(node('h1', '', data.title), node('p', '', `${ui.notes} · ${ui.total}: ${clock(data.slides.slice(0, data.mainCount).reduce((sum, s) => sum + s.duration, 0))}`));
    const times = timings();
    data.slides.forEach((slide, i) => {
      const section = node('section'); section.id = `not-${i + 1}`;
      section.append(node('h2', '', `${i < data.mainCount ? i + 1 : ui.appendix + ' ' + (i - data.mainCount + 1)}. ${slide.title}`), node('p', 'timing', times[i]), node('p', 'speech', slide.notes));
      const annotations = codeNotes(slide, false);
      if (annotations) section.append(node('h3', '', ui.codeNotesHeading), annotations);
      if (slide.sources.length) { const links = node('div', 'sources'); links.append(sources(slide)); section.append(links); }
      body.append(section);
    });
    html.append(head, body); return '<!doctype html>\n' + html.outerHTML;
  }
  pdfLabels.forEach((_, link) => link.addEventListener('click', event => { if (modified()) { event.preventDefault(); window.print(); } }));
  notesLink?.addEventListener('click', event => {
    if (!modified()) return;
    event.preventDefault();
    const url = URL.createObjectURL(new Blob([notesHtml()], { type: 'text/html;charset=utf-8' }));
    window.open(url + `#not-${index + 1}`, '_blank', 'noopener');
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  });
  window.addEventListener('resize', () => requestAnimationFrame(checkFit));
  document.fonts?.ready.then(() => requestAnimationFrame(checkFit));
  // Rendering all slides also installs the preview-to-field click targets.
  let saved;
  try { saved = localStorage.getItem(storageKey); } catch { setStatus(ui.memory, true); }
  if (saved) {
    try { data = validateImport(JSON.parse(saved)); setStatus(ui.loaded); }
    catch { setStatus(ui.storageInvalid, true); }
  }
  restoring = true; refresh(true); restoring = false;
  buildFields();
})();
