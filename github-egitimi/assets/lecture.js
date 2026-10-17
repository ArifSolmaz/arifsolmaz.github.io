(() => {
  'use strict';
  const stage=document.getElementById('ui-stage');
  const slides=Array.from(stage.children);
  const mainCount=Number(document.body.dataset.mainCount);
  const viewport=document.getElementById('ui-viewport');
  const count=document.getElementById('ui-count');
  const previous=document.getElementById('ui-prev');
  const next=document.getElementById('ui-next');
  const notes=document.getElementById('ui-notes');
  const overview=document.getElementById('ui-overview');
  const appendixButton=document.getElementById('ui-appendix');
  const language=document.body.dataset.lang||document.documentElement.lang||'tr';
  const ui=language==='en'?{appendix:'Appendix',main:'Main lecture',extras:'Appendix slides',title:'Git and GitHub'}:{appendix:'Ek',main:'Ana anlatım',extras:'Ek slaytlar',title:'Git ve GitHub'};
  const languageLink=document.querySelector('[data-language-link]');
  const languageBase=languageLink?.getAttribute('href').split('#')[0];
  const notesDocument=document.getElementById('ui-notes-document');
  const notesBase=document.body.dataset.notesBase||notesDocument?.getAttribute('href').split('#')[0];
  const appendixLabel=i=>`${ui.appendix} ${i-mainCount+1}`;
  const loaded=new Map();
  let index=0, lastMain=0, returnFocus=null;
  const appendix=()=>index>=mainCount;
  function fit(){
    const scale=Math.min(viewport.clientWidth/1920,viewport.clientHeight/1080);
    stage.style.transform=`scale(${scale})`;
    stage.style.margin=`${-(1080-1080*scale)/2}px ${-(1920-1920*scale)/2}px`;
    document.querySelectorAll('.thumb-preview').forEach(t=>{t.firstElementChild.style.transform=`scale(${t.clientWidth/1920})`;});
  }
  async function playAnimation(slide){
    const img=slide.querySelector('img[data-animation]');
    if(!img)return;
    if(document.body.classList.contains('editing')||matchMedia('(prefers-reduced-motion: reduce)').matches){img.src=img.dataset.poster;return;}
    const path=img.dataset.animation;
    if(location.protocol==='file:'){img.src=path;return;}
    try{
      if(!loaded.has(path))loaded.set(path,fetch(path).then(r=>{if(!r.ok)throw Error('Unavailable');return r.blob();}));
      const blob=await loaded.get(path);
      if(!slide.classList.contains('active'))return;
      if(img.dataset.blobUrl)URL.revokeObjectURL(img.dataset.blobUrl);
      const url=URL.createObjectURL(blob);img.dataset.blobUrl=url;img.src=url;
    }catch{img.src=img.dataset.poster;}
  }
  function show(target,push=false){
    const value=Number(target);index=Number.isFinite(value)?Math.max(0,Math.min(slides.length-1,value)):0;
    if(!appendix())lastMain=index;
    slides.forEach((s,i)=>{s.classList.toggle('active',i===index);s.setAttribute('aria-hidden',String(i!==index));});
    document.body.dataset.mode=appendix()?'appendix':'main';
    const start=appendix()?mainCount:0,end=appendix()?slides.length:mainCount;
    count.textContent=appendix()?`${appendixLabel(index)} / ${slides.length-mainCount}`:`${index+1} / ${mainCount}`;
    count.title=slides[index].querySelector('h1,h2').textContent;
    previous.disabled=index===start;next.disabled=index===end-1;
    document.getElementById('ui-btn-replay').disabled=!slides[index].querySelector('img[data-animation]');
    appendixButton.textContent=appendix()?ui.main:ui.extras;
    document.getElementById('ui-progress').style.width=`${(index-start+1)/(end-start)*100}%`;
    const speech=slides[index].querySelector('aside');
    document.getElementById('ui-notes-title').textContent=`${appendix()?appendixLabel(index):index+1}. ${count.title}`;
    document.getElementById('ui-notes-body').textContent=speech?.querySelector('.speech')?.textContent||'';
    document.getElementById('ui-notes-sources').replaceChildren(...Array.from(speech?.querySelectorAll('a')||[],a=>a.cloneNode(true)));
    document.querySelectorAll('.thumb').forEach((t,i)=>{t.classList.toggle('current',i===index);if(i===index)t.setAttribute('aria-current','true');else t.removeAttribute('aria-current');});
    const hash=`#${index+1}`;
    if(location.hash!==hash)history[push?'pushState':'replaceState'](null,'',hash);
    document.title=count.title.trim()===ui.title?ui.title:`${count.title} · ${ui.title}`;
    if(languageLink)languageLink.setAttribute('href',`${languageBase}#${encodeURIComponent(slides[index].id)}`);
    if(notesDocument)notesDocument.setAttribute('href',`${notesBase}#not-${index+1}`);
    playAnimation(slides[index]);
    document.dispatchEvent(new CustomEvent('lecture:slidechange',{detail:{index,slideId:slides[index].id}}));
  }
  function fromHash(){
    let hash=location.hash.slice(1);
    try{hash=decodeURIComponent(hash);}catch{return 0;}
    if(hash==='ekler'||hash==='appendix')return mainCount;
    if(/^\d+$/.test(hash))return Number(hash)-1;
    const found=slides.findIndex(s=>s.id===hash);return found<0?0:found;
  }
  function move(delta){
    const start=appendix()?mainCount:0,end=appendix()?slides.length:mainCount;
    show(Math.max(start,Math.min(end-1,index+delta)),true);
  }
  function setOverview(open){
    if(open){returnFocus=document.activeElement;overview.hidden=false;fit();const current=overview.querySelector('.thumb.current');current?.focus();current?.scrollIntoView({block:'center'});}
    else{overview.hidden=true;returnFocus?.focus();}
  }
  function toggleNotes(){notes.hidden=!notes.hidden;document.getElementById('ui-btn-notes').setAttribute('aria-pressed',String(!notes.hidden));}
  function buildOverview(){
    document.getElementById('ui-main-grid').replaceChildren();
    document.getElementById('ui-extra-grid').replaceChildren();
    slides.forEach((s,i)=>{
      const button=document.createElement('button');button.className='thumb';button.type='button';
      const title=s.querySelector('h1,h2').textContent;button.setAttribute('aria-label',`${i<mainCount?i+1:appendixLabel(i)}. ${title}`);
      const preview=document.createElement('div');preview.className='thumb-preview';preview.setAttribute('aria-hidden','true');
      const mini=document.createElement('div');mini.className='mini';const clone=s.cloneNode(true);clone.removeAttribute('id');clone.removeAttribute('aria-hidden');clone.classList.remove('active');clone.querySelector('aside')?.remove();
      clone.querySelectorAll('[id]').forEach(e=>e.removeAttribute('id'));
      clone.querySelectorAll('a').forEach(a=>a.removeAttribute('href'));
      clone.querySelectorAll('img[data-animation]').forEach(img=>{img.src=img.dataset.poster;img.removeAttribute('data-animation');});
      mini.append(clone);preview.append(mini);const label=document.createElement('div');label.className='thumb-label';const number=document.createElement('b');number.textContent=i<mainCount?`${i+1}.`:`${appendixLabel(i)}.`;label.append(number,document.createTextNode(title));
      button.append(preview,label);button.onclick=()=>{show(i,true);setOverview(false);};
      document.getElementById(i<mainCount?'ui-main-grid':'ui-extra-grid').append(button);
    });
  }
  previous.onclick=()=>move(-1);next.onclick=()=>move(1);
  appendixButton.onclick=()=>show(appendix()?lastMain:mainCount,true);
  document.getElementById('ui-btn-ov').onclick=()=>setOverview(true);
  document.getElementById('ui-close-ov').onclick=()=>setOverview(false);
  document.getElementById('ui-btn-notes').onclick=toggleNotes;
  document.getElementById('ui-btn-replay').onclick=()=>playAnimation(slides[index]);
  document.getElementById('ui-btn-fs').onclick=()=>{if(document.fullscreenElement)document.exitFullscreen?.();else document.documentElement.requestFullscreen?.();};
  document.getElementById('ui-btn-print').onclick=()=>window.print();
  window.addEventListener('hashchange',()=>show(fromHash()));
  window.addEventListener('popstate',()=>show(fromHash()));
  window.addEventListener('resize',fit);
  document.addEventListener('lecture:refresh',e=>{buildOverview();fit();show(e.detail?.index??index);});
  window.addEventListener('beforeprint',()=>{slides.forEach(s=>{const img=s.querySelector('img[data-animation]');if(img)img.src=img.dataset.poster;});});
  window.addEventListener('afterprint',()=>playAnimation(slides[index]));
  document.addEventListener('keydown',e=>{
    if(e.metaKey||e.ctrlKey||e.altKey||e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
    const k=e.key.toLowerCase();
    if(k===' '&&e.target.closest('button,a'))return;
    if(!overview.hidden){
      if(k==='escape'||k==='o'){setOverview(false);e.preventDefault();}
      else if(k==='tab'){
        const buttons=Array.from(overview.querySelectorAll('button'));
        const first=buttons[0],last=buttons[buttons.length-1];
        if(e.shiftKey&&document.activeElement===first){last.focus();e.preventDefault();}
        else if(!e.shiftKey&&document.activeElement===last){first.focus();e.preventDefault();}
      }
      return;
    }
    if(['arrowright','arrowdown','pagedown',' '].includes(k)){move(1);e.preventDefault();}
    else if(['arrowleft','arrowup','pageup'].includes(k)){move(-1);e.preventDefault();}
    else if(k==='home'){show(appendix()?mainCount:0,true);e.preventDefault();}
    else if(k==='end'){show(appendix()?slides.length-1:mainCount-1,true);e.preventDefault();}
    else if(k==='n')toggleNotes();else if(k==='o')setOverview(true);
    else if(k==='escape'){notes.hidden=true;document.getElementById('ui-btn-notes').setAttribute('aria-pressed','false');}
    else if(k==='f')document.getElementById('ui-btn-fs').click();
    else if(k==='p')window.print();else if(k==='r')playAnimation(slides[index]);
  });
  let touch=null;stage.addEventListener('touchstart',e=>{touch={x:e.touches[0].clientX,y:e.touches[0].clientY};},{passive:true});
  stage.addEventListener('touchend',e=>{if(!touch)return;const dx=e.changedTouches[0].clientX-touch.x,dy=e.changedTouches[0].clientY-touch.y;touch=null;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))move(dx<0?1:-1);},{passive:true});
  buildOverview();fit();show(fromHash());
})();
