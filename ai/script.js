const canvas=document.getElementById('light');
const gl=canvas.getContext('webgl',{alpha:false,antialias:false,powerPreference:'low-power',preserveDrawingBuffer:false});
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let reading=false;
let paused=reduced.matches,raf=0,lastFrame=0,elapsed=18,viewportWidth=0,viewportHeight=0;
const pointer={x:.48,y:.57,targetX:.48,targetY:.57};
let active=0,activeTarget=0;
const sceneIds={akademi:1,egitim:2,kurum:3,veri:4,yaklasim:5};
let sceneFrom=0,sceneTo=0,sceneMix=1,transitioning=false;
const vertexSource=`attribute vec2 a_position;void main(){gl_Position=vec4(a_position,0.,1.);}`;
const fragmentSource=`precision highp float;
uniform vec2 u_resolution;uniform float u_time;uniform vec2 u_pointer;uniform float u_active;
uniform float u_sceneFrom;uniform float u_sceneTo;uniform float u_sceneMix;
float haze(float distance,float width){return exp(-distance*distance/width);}
// Forms are relief in one continuous material, never line-art placed over it.
float softFold(float y,float center,float width){return exp(-pow((y-center)/width,2.));}
float sceneSurface(vec2 p,float t,float scene){
  float a=p.x*1.25+.48*sin(p.y*1.3-t*.16);
  float b=p.y*1.55+.5*sin(p.x*1.1+t*.12);
  float bed=.16*sin(a)+.12*cos(b)+.05*sin(a+b);
  if(scene<.5){
    // Two soft presences approach, exchange a small deformation, then share a fold.
    float breathe=sin(t*.34);
    float waist=exp(-p.x*p.x*.7);
    float contact=-.65+.09*breathe;
    float left=contact+.65*sin(p.x*1.02)+.16*sin(p.x*2.1-t*.13)*(1.-waist);
    float right=contact-.65*sin(p.x*1.02)+.08*sin(p.x*3.+t*.13)*(1.-waist);
    float broad=softFold(p.y,left,.42)*(1.-smoothstep(-.25,1.4,p.x));
    float fine=softFold(p.y,right,.28)*smoothstep(-1.4,.25,p.x);
    float echo=softFold(p.y,right+.26*(1.-waist),.14)*smoothstep(-.6,1.3,p.x);
    // The response is reciprocal: each presence takes on the other's curvature.
    float shared=softFold(p.y-contact-.16*sin(p.x*1.8+t*.12),.0,.48)*waist;
    return bed*.65+.52*broad+.43*fine+.11*echo+.17*shared;
  }
  if(scene<1.5){
    // Research: an off-axis lens gathering light into a deep, quiet focal pool.
    vec2 q=p-vec2(-.75,-.25);
    float r=length(q*vec2(.78,1.06));
    float lens=softFold(r,1.13+.07*sin(atan(q.y,q.x)*2.),.37);
    return bed*.45+.62*lens-.25*exp(-r*r*1.6)+.13*cos(r*2.1);
  }
  if(scene<2.5){
    // Learning: successive folds unfurl from a small source, growing wider and softer.
    vec2 q=p-vec2(-1.25,-1.45);
    float r=length(q*vec2(.83,1.));
    float bend=.09*sin(atan(q.y,q.x)*3.+t*.1);
    return bed*.3+.43*softFold(r+bend,1.,.27)+.36*softFold(r+bend,1.95,.4)+.26*softFold(r+bend,3.15,.6);
  }
  if(scene<3.5){
    // Teams: three separate streams naturally braid and broaden into one current.
    float converge=1.-smoothstep(-2.1,1.65,p.x);
    float flow=p.y-.18*p.x-.28*sin(p.x*.85+t*.08);
    float spread=.88*converge;
    return bed*.35+.35*softFold(flow,spread,.28)+.4*softFold(flow,0.,.36)+.35*softFold(flow,-spread,.28);
  }
  if(scene<4.5){
    // Data: granular variation becomes a smooth, coherent contour, without a chart.
    float clarity=smoothstep(-2.,1.7,p.x);
    float variation=p.y+.24*sin(p.x*2.+p.y*2.3)+.1*sin(p.y*7.);
    float ordered=mix(variation,p.y+.14*p.x,clarity);
    float ridges=.25*sin(ordered*3.3)+.12*cos(ordered*1.6);
    float grains=.035*sin(p.x*12.+sin(p.y*8.))*cos(p.y*11.);
    return bed*.2+ridges+grains*(1.-clarity);
  }
  // The researcher: a broad atmospheric crescent with distant, diffuse depth.
  vec2 q=(p-vec2(.45,-1.6))*vec2(.72,1.);
  float radius=length(q);
  return bed*.2+.52*softFold(radius,2.12,.55)-.12*exp(-radius*radius*.4);
}
float sceneLight(vec2 p,float t,float scene){
  if(scene<.5){
    float contact=-.65+.09*sin(t*.34);
    return exp(-p.x*p.x*1.2-pow((p.y-contact)*1.5,2.))*.21;
  }
  if(scene<1.5){
    vec2 q=(p-vec2(-.75,-.25))*vec2(.78,1.06);
    return exp(-dot(q,q)*.8)*.16;
  }
  if(scene<2.5){
    vec2 q=p-vec2(-1.25,-1.45);
    return exp(-dot(q,q)*.65)*.24;
  }
  if(scene<3.5){
    float flow=p.y-.18*p.x-.28*sin(p.x*.85+t*.08);
    return exp(-pow(flow*1.5,2.))*smoothstep(-1.,2.5,p.x)*.16;
  }
  if(scene<4.5){
    float clouds=sin(p.x*3.+p.y*1.2)*cos(p.y*3.1-p.x*.7);
    return (.5+.5*clouds)*.06*(1.-smoothstep(-2.,1.5,p.x));
  }
  vec2 q=(p-vec2(.45,-1.6))*vec2(.72,1.);
  return exp(-pow((length(q)-2.5)*1.7,2.))*.15;
}
float thematicLight(vec2 p,float t){
  if(u_sceneMix>.999)return sceneLight(p,t,u_sceneTo);
  return mix(sceneLight(p,t,u_sceneFrom),sceneLight(p,t,u_sceneTo),smoothstep(0.,1.,u_sceneMix));
}
float surface(vec2 p,float t){
  if(u_sceneMix>.999)return sceneSurface(p,t,u_sceneTo);
  return mix(sceneSurface(p,t,u_sceneFrom),sceneSurface(p,t,u_sceneTo),smoothstep(0.,1.,u_sceneMix));
}
void main(){
  vec2 uv=gl_FragCoord.xy/u_resolution;
  float aspect=u_resolution.x/u_resolution.y;
  vec2 p=(uv-.5)*vec2(aspect,1.)*3.4;
  float t=u_time*.17;
  float h=surface(p,t);
  float eps=.008;
  vec2 grad=vec2(surface(p+vec2(eps,0.),t)-h,surface(p+vec2(0.,eps),t)-h)/eps;
  vec3 normal=normalize(vec3(-grad*.74,1.));
  vec2 lamp=(u_pointer-.5)*vec2(aspect,1.)*1.5;
  vec3 light=normalize(vec3(lamp+vec2(-.4,.65),1.8));
  float diffuse=dot(normal,light)*.5+.5;
  float gloss=pow(max(dot(reflect(-light,normal),vec3(0.,0.,1.)),0.),26.);
  float broad=pow(max(dot(normal,normalize(vec3(.5,-.1,1.))),0.),8.);
  float line=pow(.5+.5*sin(h*5.+p.x*.3),9.);
  vec3 shadow=vec3(.52,.64,.60);
  vec3 pearl=vec3(.90,.93,.86);
  vec3 color=mix(shadow,pearl,smoothstep(.23,.96,diffuse));
  color+=gloss*.11+line*.025+broad*.04;
  float theme=thematicLight(p,t);
  color=mix(color,vec3(.99,.99,.90),clamp(theme,0.,.7));
  float warm=exp(-dot(p-vec2(-.8,.6),p-vec2(-.8,.6))*.35);
  color=mix(color,vec3(.97,.95,.84),warm*.28);
  // A shared, open horizon: brighter where the two currents come together.
  float future=exp(-pow(p.x*.72,2.)-pow((p.y-1.05)*.8,2.));
  color=mix(color,vec3(.97,.97,.89),future*.12);
  float d=length((uv-u_pointer)*vec2(aspect,1.));
  color+=exp(-d*d*3.)*.025*u_active;
  float grain=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453)-.5;
  color+=grain*.008;
  float edge=smoothstep(.35,.78,length((uv-.5)*vec2(1.,.8)));
  color=mix(color,vec3(.88,.92,.87),edge*.46);
  color=mix(color,vec3(.89,.93,.88),.16);
  gl_FragColor=vec4(color,1.);
}`;
let program,uniforms;
function compile(type,source){const shader=gl.createShader(type);gl.shaderSource(shader,source);gl.compileShader(shader);if(!gl.getShaderParameter(shader,gl.COMPILE_STATUS)){gl.deleteShader(shader);return null;}return shader;}
function initialize(){
 if(!gl)return false;
 const vertex=compile(gl.VERTEX_SHADER,vertexSource),fragment=compile(gl.FRAGMENT_SHADER,fragmentSource);if(!vertex||!fragment)return false;
 program=gl.createProgram();gl.attachShader(program,vertex);gl.attachShader(program,fragment);gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))return false;
 gl.useProgram(program);const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
 const position=gl.getAttribLocation(program,'a_position');gl.enableVertexAttribArray(position);gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
 uniforms={resolution:gl.getUniformLocation(program,'u_resolution'),time:gl.getUniformLocation(program,'u_time'),pointer:gl.getUniformLocation(program,'u_pointer'),active:gl.getUniformLocation(program,'u_active'),sceneFrom:gl.getUniformLocation(program,'u_sceneFrom'),sceneTo:gl.getUniformLocation(program,'u_sceneTo'),sceneMix:gl.getUniformLocation(program,'u_sceneMix')};
 return true;
}
const ready=initialize();
if(!ready){canvas.hidden=true;document.getElementById('motion-control').hidden=true;}
function draw(){
 if(!ready)return;
 gl.viewport(0,0,canvas.width,canvas.height);gl.useProgram(program);gl.uniform2f(uniforms.resolution,canvas.width,canvas.height);gl.uniform1f(uniforms.time,elapsed);gl.uniform2f(uniforms.pointer,pointer.x,pointer.y);gl.uniform1f(uniforms.active,active);gl.uniform1f(uniforms.sceneFrom,sceneFrom);gl.uniform1f(uniforms.sceneTo,sceneTo);gl.uniform1f(uniforms.sceneMix,sceneMix);gl.drawArrays(gl.TRIANGLES,0,6);
}
function resize(){
 viewportWidth=innerWidth;viewportHeight=innerHeight;
 const scale=Math.min(devicePixelRatio||1,1.25,1100/viewportWidth);
 canvas.width=Math.round(viewportWidth*scale);canvas.height=Math.round(viewportHeight*scale);draw();
}
function frame(stamp){
 raf=0;if(paused||document.hidden||(reading&&!transitioning))return;
 if(!lastFrame||stamp-lastFrame>=33){const delta=lastFrame?Math.min((stamp-lastFrame)/1000,.1):.033;lastFrame=stamp;elapsed+=reading?0:delta;if(transitioning){sceneMix=Math.min(1,sceneMix+delta/1.5);transitioning=sceneMix<1;}pointer.x+=(pointer.targetX-pointer.x)*.045;pointer.y+=(pointer.targetY-pointer.y)*.045;active+=(activeTarget-active)*.05;draw();}
 raf=requestAnimationFrame(frame);
}
function setScene(id){sceneFrom=sceneMix<.5?sceneFrom:sceneTo;sceneTo=sceneIds[id]||0;sceneMix=paused?1:0;transitioning=sceneMix<1;document.body.dataset.scene=id||'home';}
function syncMotion(){document.body.classList.toggle('motion-paused',paused);if(paused){sceneMix=1;transitioning=false;}document.getElementById('motion-control').textContent=paused?'Harekete izin ver':'Hareketi durdur';document.getElementById('motion-control').setAttribute('aria-pressed',String(paused));if(raf){cancelAnimationFrame(raf);raf=0;}lastFrame=0;if(!paused&&!document.hidden&&(!reading||transitioning)&&ready)raf=requestAnimationFrame(frame);else draw();}
window.addEventListener('resize',resize);
document.addEventListener('pointermove',event=>{if(reduced.matches||paused||reading)return;pointer.targetX=event.clientX/viewportWidth;pointer.targetY=1-event.clientY/viewportHeight;activeTarget=1;},{passive:true});
document.addEventListener('pointerleave',()=>activeTarget=0);
document.getElementById('motion-control').addEventListener('click',()=>{paused=!paused;syncMotion();});
reduced.addEventListener('change',()=>{paused=reduced.matches;syncMotion();});document.addEventListener('visibilitychange',syncMotion);
canvas.addEventListener('webglcontextlost',event=>{event.preventDefault();if(raf)cancelAnimationFrame(raf);raf=0;canvas.hidden=true;});canvas.addEventListener('webglcontextrestored',()=>location.reload());
resize();syncMotion();

const room=document.getElementById('reading-room'),readingContent=document.getElementById('reading-content');
function draftLinks(root){root.querySelectorAll('[data-program]').forEach(link=>{const programme=link.dataset.program;const body=`Merhaba Arif Bey,\r\n\r\n${programme} eğitimi hakkında konuşmak isterim.\r\n\r\nKurum: \r\nKatılımcı profili ve yaklaşık sayısı: \r\nÖğrenmek istediğimiz konu: \r\nDüşündüğümüz tarih ve eğitim biçimi: \r\n\r\nAd soyad: \r\n`;link.href=`mailto:arif.solmaz@istun.edu.tr?subject=${encodeURIComponent(programme+' — Eğitim talebi')}&body=${encodeURIComponent(body)}`;});}
function openRoom(id,updateHash=true){const template=document.getElementById('content-'+id);if(!template)return;readingContent.replaceChildren(template.content.cloneNode(true));draftLinks(readingContent);if(!room.open)room.showModal();reading=true;document.body.classList.add('reading-active');setScene(id);syncMotion();room.scrollTop=0;if(updateHash)history.replaceState(null,'','#'+id);}
function closeRoom(){room.close();}
document.querySelectorAll('[data-open]').forEach(button=>button.addEventListener('click',()=>openRoom(button.dataset.open)));
document.getElementById('close-reading').addEventListener('click',closeRoom);
room.addEventListener('click',event=>{if(event.target===room){const rect=room.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)closeRoom();}});
room.addEventListener('close',()=>{reading=false;document.body.classList.remove('reading-active');setScene('home');syncMotion();readingContent.replaceChildren();history.replaceState(null,'',location.pathname+location.search);});
window.addEventListener('hashchange',()=>{const id=location.hash.slice(1);if(document.getElementById('content-'+id))openRoom(id,false);else if(room.open)room.close();});
draftLinks(document);if(location.hash)openRoom(location.hash.slice(1),false);
