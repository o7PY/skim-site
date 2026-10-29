(function(){
'use strict';
var D=window.DATA, $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var SVGNS='http:/'+'/www.w3.org/2000/svg';
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function h(tag,attrs,html){var e=document.createElement(tag);for(var k in (attrs||{})){if(k==='class')e.className=attrs[k];else e.setAttribute(k,attrs[k])}if(html!=null)e.innerHTML=html;return e}
function store(k,v){try{if(v===undefined){return JSON.parse(localStorage.getItem('prep.'+k))}localStorage.setItem('prep.'+k,JSON.stringify(v))}catch(e){return null}}
var GC={ingest:'#60a5fa',ai:'#a78bfa',api:'#2dd4bf',push:'#fb7185',auth:'#fbbf24',deploy:'#94a3b8',data:'#4ade80',web:'#f472b6'};
var TABS=[['start','Start'],['map','Map'],['data','Data'],['api','API & jobs'],['lab','Playgrounds'],['app','App tour'],['internals','How it works'],['decisions','Decisions'],['stories','War stories'],['interview','Interview'],['gloss','Glossary'],['web','Website']];
var main=$('#main'),tabs=$('#tabs');
TABS.forEach(function(t){var b=h('button',{role:'tab','data-t':t[0],'aria-selected':'false'},t[1]);b.onclick=function(){go(t[0])};tabs.appendChild(b);main.appendChild(h('section',{class:'view',id:'v-'+t[0],role:'tabpanel'}))});
var built={};
function go(id,after){
  if(!document.getElementById('v-'+id))id='start';
  $$('.view').forEach(function(v){v.classList.toggle('on',v.id==='v-'+id)});
  $$('#tabs button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.t===id)});
  if(!built[id]){built[id]=1;R[id]($('#v-'+id))}
  if(location.hash!=='#'+id)history.replaceState(null,'','#'+id);
  window.scrollTo(0,0);store('tab',id);if(after)after();
}
var R={};
/* ---------- START ---------- */
R.start=function(el){
  var N=D.numbers;
  el.innerHTML='<div class="hero"><p class="tag">PRIVATE STUDY GUIDE</p><h1>Everything about <span>Skim</span>,<br>in one place you can poke at.</h1><p class="lead">A Microsoft Teams bot, a Python backend on Google Cloud, a Supabase database, AI models, an Android app, and a website. This page explains how each part works, why every big choice was made, and how to talk about it in an interview.</p>'+
  '<div class="row"><button class="btn" data-go="map">Open the live map</button><button class="btn ghost" data-go="interview">Start flashcards</button><button class="btn ghost" data-go="decisions">Browse '+D.decisions.length+' decisions</button></div></div>'+
  '<h2 style="margin-top:34px">The 30-second pitch</h2><div class="card"><p style="font-size:18px;margin:0">'+esc(D.pitch)+'</p></div>'+
  '<h2 style="margin-top:34px">By the numbers</h2><div class="grid g4">'+N.map(function(n){return '<div class="card stat"><b>'+esc(n[0])+'</b><span>'+esc(n[1])+'</span></div>'}).join('')+'</div>'+
  '<h2 style="margin-top:34px">How data flows, in six steps</h2><ol class="how" style="padding:0">'+D.flow.map(function(s){return '<li>'+s+'</li>'}).join('')+'</ol>'+
  '<h2 style="margin-top:34px">The story, phase by phase</h2><div class="tl">'+D.timeline.map(function(t){return '<div class="it"><span class="tag">PHASE '+esc(t.phase)+' &middot; '+esc(t.date)+'</span><h3>'+esc(t.title)+'</h3><p style="margin:.2em 0">'+esc(t.body)+'</p><p class="small" style="margin:0"><b>Outcome:</b> '+esc(t.outcome)+'</p></div>'}).join('')+'</div>'+
  '<h2 style="margin-top:34px">How to use this page</h2><div class="grid g3">'+[['Learn','Map &rarr; Data &rarr; API & jobs &rarr; How it works. Click everything; play the scenarios.'],['Understand why','Decisions and War stories hold the reasoning and the bugs. Star what you want to remember.'],['Rehearse','Playgrounds let you try the rules. Interview has flashcards that remember what you missed.']].map(function(x){return '<div class="card"><h3>'+x[0]+'</h3><p class="small">'+x[1]+'</p></div>'}).join('')+'</div>';
  $$('[data-go]',el).forEach(function(b){b.onclick=function(){go(b.dataset.go)}});
};
/* ---------- MAP ---------- */
var MAPSEL=null;
R.map=function(el){
  el.innerHTML='<h2>The live map</h2><p class="lead">Every box is a real part of the system. Click one for what it does, why it was chosen, and what to say about it. Pick a scenario and press play to watch a request travel.</p>'+
  '<div class="legend" id="leg"></div><div class="scen" id="scen"></div><div class="maplayout"><div><div class="svgwrap"><svg class="map" id="svg" viewBox="0 0 1240 770" role="img" aria-label="Architecture diagram"></svg></div>'+
  '<div class="stepbox" id="stepbox" hidden><div class="row" style="justify-content:space-between"><b id="stt"></b><span class="small" id="stn"></span></div><p id="stx"></p><div class="prog"><i id="stp" style="width:0"></i></div><div class="row" style="margin-top:10px"><button class="btn ghost" id="sprev">&larr; Back</button><button class="btn" id="splay">Play</button><button class="btn ghost" id="snext">Next &rarr;</button><button class="btn ghost" id="sstop">Exit</button></div></div></div>'+
  '<aside class="card panel" id="det" aria-live="polite"></aside></div>';
  var svg=$('#svg'),NS={},ES={},byId={};D.nodes.forEach(function(n){byId[n.id]=n});
  function mk(t,a){var e=document.createElementNS(SVGNS,t);for(var k in a)e.setAttribute(k,a[k]);return e}
  var zones=[['Microsoft',30,25,170,470],['Google Cloud',300,25,420,400],['Dev',790,25,420,95],['Supabase',305,455,500,130],['Expo / Google (push + builds)',800,185,200,570]];
  // light zone frames
  [[30,35,160,470,'MICROSOFT'],[290,35,440,330,'GOOGLE CLOUD'],[310,455,440,130,'SUPABASE'],[800,185,200,570,'PUSH AND BUILDS']].forEach(function(z){svg.appendChild(mk('rect',{x:z[0],y:z[1],width:z[2],height:z[3],rx:18,class:'zone'}));var t=mk('text',{x:z[0]+12,y:z[1]+z[3]-8,class:'zlabel'});t.textContent=z[4];svg.appendChild(t)});
  var defs=mk('defs',{});svg.appendChild(defs);
  var eg=mk('g',{}),ng=mk('g',{}),pg=mk('g',{});svg.appendChild(eg);svg.appendChild(ng);svg.appendChild(pg);
  var W=150,H=56;
  function edgePts(a,b){var ax=a.x,ay=a.y,bx=b.x,by=b.y,dx=bx-ax,dy=by-ay;function clip(cx,cy,ux,uy){var tx=Math.abs(ux)>1e-6?(W/2+6)/Math.abs(ux):1e9,ty=Math.abs(uy)>1e-6?(H/2+6)/Math.abs(uy):1e9,t=Math.min(tx,ty);return [cx+ux*t,cy+uy*t]}return [clip(ax,ay,dx,dy),clip(bx,by,-dx,-dy)]}
  D.edges.forEach(function(e){
    var a=byId[e.a],b=byId[e.b],p=edgePts(a,b),col=GC[e.g]||'#888';
    var g=mk('g',{class:'edge','data-g':e.g,style:'color:'+col});
    var mid=[(p[0][0]+p[1][0])/2,(p[0][1]+p[1][1])/2];
    var d='M'+p[0][0]+','+p[0][1]+' L'+p[1][0]+','+p[1][1];
    var path=mk('path',{d:d,stroke:col,'marker-end':'url(#ar-'+e.g+')'});if(e.dash)path.setAttribute('stroke-dasharray','6 5');
    if(e.both)path.setAttribute('marker-start','url(#as-'+e.g+')');
    g.appendChild(path);
    var tt=mk('text',{x:mid[0],y:mid[1]-5,'text-anchor':'middle'});tt.textContent='';g.appendChild(tt);
    var ti=mk('title',{});ti.textContent=e.label;g.appendChild(ti);
    eg.appendChild(g);ES[e.id]={g:g,path:path,e:e,p:p,lab:tt};
    if(!defs.querySelector('#ar-'+e.g)){
      var m1=mk('marker',{id:'ar-'+e.g,viewBox:'0 0 10 10',refX:9,refY:5,markerWidth:7,markerHeight:7,orient:'auto'});m1.appendChild(mk('path',{d:'M0,0 L10,5 L0,10 z',fill:col}));defs.appendChild(m1);
      var m2=mk('marker',{id:'as-'+e.g,viewBox:'0 0 10 10',refX:1,refY:5,markerWidth:7,markerHeight:7,orient:'auto-start-reverse'});m2.appendChild(mk('path',{d:'M10,0 L0,5 L10,10 z',fill:col}));defs.appendChild(m2);
    }
  });
  D.nodes.forEach(function(n){
    var g=mk('g',{class:'node',tabindex:0,role:'button','aria-label':n.label,transform:'translate('+(n.x-W/2)+','+(n.y-H/2)+')'});
    g.appendChild(mk('rect',{width:W,height:H,rx:14}));
    var ic=mk('text',{x:14,y:36,class:'ic'});ic.textContent=n.icon;g.appendChild(ic);
    var words=n.label.split(' '),l1=n.label,l2='';if(n.label.length>16){var m=Math.ceil(words.length/2);l1=words.slice(0,m).join(' ');l2=words.slice(m).join(' ')}
    var t=mk('text',{x:44,y:l2?24:33});t.textContent=l1;g.appendChild(t);if(l2){var t2=mk('text',{x:44,y:41});t2.textContent=l2;g.appendChild(t2)}
    g.onclick=function(){selNode(n.id)};g.onkeydown=function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();selNode(n.id)}};
    ng.appendChild(g);NS[n.id]=g;
  });
  var leg=$('#leg');var on={};
  Object.keys(D.groups).forEach(function(k){on[k]=true;var b=h('button',{class:'chip on','aria-pressed':'true'},'<span class="dot" style="background:'+GC[k]+'"></span>'+esc(D.groups[k]));b.onclick=function(){on[k]=!on[k];b.classList.toggle('on',on[k]);b.setAttribute('aria-pressed',on[k]);Object.keys(ES).forEach(function(id){if(ES[id].e.g===k)ES[id].g.classList.toggle('hid',!on[k])})};leg.appendChild(b)});
  function clearLit(){Object.keys(NS).forEach(function(i){NS[i].classList.remove('lit','dim')});Object.keys(ES).forEach(function(i){ES[i].g.classList.remove('lit','dim');ES[i].lab.textContent=''})}
  function selNode(id){
    MAPSEL=id;Object.keys(NS).forEach(function(i){NS[i].classList.toggle('sel',i===id)});
    var n=byId[id],rel=D.edges.filter(function(e){return e.a===id||e.b===id});
    $('#det').innerHTML='<h3><span style="font-size:26px">'+n.icon+'</span>'+esc(n.label)+'</h3><span class="tag">'+esc(n.zone)+'</span> <span class="tag">'+esc(n.kind)+'</span>'+
     '<h4>What it is</h4><p>'+esc(n.what)+'</p><h4>Why it was chosen</h4><p>'+esc(n.why)+'</p><h4>Connections</h4><p>'+esc(n.links)+'</p><ul>'+rel.map(function(e){var o=e.a===id?e.b:e.a;return '<li>'+(e.a===id?'&rarr; ':'&larr; ')+'<b>'+esc(byId[o].label)+'</b> <span class="small">'+esc(e.label)+'</span></li>'}).join('')+'</ul>'+
     '<h4>Gotchas</h4><ul>'+n.gotchas.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul><h4>Say this in an interview</h4><ul>'+n.talk.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul><h4>Decisions</h4><div>'+n.dec.map(function(x){return '<button class="chip" data-dec="'+esc(x)+'">'+esc(x)+'</button>'}).join('')+'</div>';
    $$('[data-dec]',$('#det')).forEach(function(b){b.onclick=function(){openDecision(b.dataset.dec)}});
    // highlight neighbourhood
    if(!SC){clearLit();var near={};near[id]=1;rel.forEach(function(e){near[e.a]=near[e.b]=1;ES[e.id].g.classList.add('lit');ES[e.id].lab.textContent=e.label});Object.keys(NS).forEach(function(i){if(!near[i])NS[i].classList.add('dim');else NS[i].classList.add('lit')});Object.keys(ES).forEach(function(i){if(!ES[i].g.classList.contains('lit'))ES[i].g.classList.add('dim')})}
  }
  $('#det').innerHTML='<h3>Pick a box</h3><p class="small">Click any component for its role, reasons, gotchas and talking points. Or choose a scenario above and press Play.</p>';
  svg.addEventListener('click',function(ev){if(ev.target===svg&&!SC){clearLit();MAPSEL=null;$$('.node.sel').forEach(function(n){n.classList.remove('sel')})}});
  /* scenarios */
  var SC=null,si=0,timer=null,raf=null;
  var sc=$('#scen');D.scenarios.forEach(function(s){var b=h('button',{},'<b>'+s.icon+' '+esc(s.title)+'</b><small>'+esc(s.blurb)+'</small>');b.onclick=function(){startScen(s,b)};sc.appendChild(b)});
  function startScen(s,b){stopAnim();SC=s;si=0;$$('button',sc).forEach(function(x){x.classList.toggle('on',x===b)});$('#stepbox').hidden=false;showStep();$('#stepbox').scrollIntoView({block:'nearest',behavior:RM?'auto':'smooth'})}
  function endScen(){stopAnim();SC=null;$$('#scen button').forEach(function(x){x.classList.remove('on')});$('#stepbox').hidden=true;clearLit();if(MAPSEL)selNode(MAPSEL)}
  function stopAnim(){clearTimeout(timer);timer=null;cancelAnimationFrame(raf);while(pg.firstChild)pg.removeChild(pg.firstChild);$('#splay')&&($('#splay').textContent='Play')}
  function showStep(){
    var st=SC.steps[si];clearLit();
    Object.keys(NS).forEach(function(i){NS[i].classList.add('dim')});Object.keys(ES).forEach(function(i){ES[i].g.classList.add('dim')});
    st.nodes.forEach(function(i){NS[i].classList.remove('dim');NS[i].classList.add('lit')});
    st.edges.forEach(function(i){ES[i].g.classList.remove('dim');ES[i].g.classList.add('lit');ES[i].lab.textContent=ES[i].e.label;ES[i].g.classList.remove('hid')});
    $('#stt').textContent=SC.icon+' '+SC.title;$('#stn').textContent='Step '+(si+1)+' of '+SC.steps.length;$('#stx').textContent=st.t;$('#stp').style.width=((si+1)/SC.steps.length*100)+'%';
    $('#sprev').disabled=si===0;$('#snext').disabled=si===SC.steps.length-1;
    pulse(st.edges);
  }
  function pulse(ids){
    cancelAnimationFrame(raf);while(pg.firstChild)pg.removeChild(pg.firstChild);if(RM||!ids.length)return;
    var ps=ids.map(function(i){var e=ES[i],c=mk('circle',{r:6,class:'pkt'});pg.appendChild(c);return {c:c,e:e}});var t0=performance.now();
    (function tick(now){var t=((now-t0)%1600)/1600;ps.forEach(function(p){var a=p.e.p[0],b=p.e.p[1],k=p.e.e.both?(t<.5?t*2:2-t*2):t;p.c.setAttribute('cx',a[0]+(b[0]-a[0])*k);p.c.setAttribute('cy',a[1]+(b[1]-a[1])*k)});raf=requestAnimationFrame(tick)})(t0);
  }
  $('#sprev').onclick=function(){if(si>0){si--;showStep()}};$('#snext').onclick=function(){if(si<SC.steps.length-1){si++;showStep()}};$('#sstop').onclick=endScen;
  $('#splay').onclick=function(){
    if(timer){clearTimeout(timer);timer=null;$('#splay').textContent='Play';return}
    $('#splay').textContent='Pause';if(si>=SC.steps.length-1){si=0;showStep()}
    (function adv(){timer=setTimeout(function(){if(si<SC.steps.length-1){si++;showStep();adv()}else{timer=null;$('#splay').textContent='Play'}},4200)})();
  };
};
/* ---------- DATA ---------- */
R.data=function(el){
  var T=D.tables,refBy={};T.forEach(function(t){t.fks.forEach(function(f){(refBy[f.to]=refBy[f.to]||[]).push(t.name)})});
  el.innerHTML='<h2>The data model</h2><p class="lead">'+T.length+' tables, read straight from the migrations. Every one has row level security on with no policies, so only the backend can touch them. Click a table; click a blue chip to follow a foreign key.</p><div class="tbls"><div><input type="search" id="tq" placeholder="Filter tables..." aria-label="Filter tables"><div class="tlist" id="tl" style="margin-top:8px"></div></div><div class="card" id="td"></div></div>';
  var tl=$('#tl');
  function list(q){tl.innerHTML='';T.filter(function(t){return !q||t.name.indexOf(q)>-1}).forEach(function(t){var b=h('button',{'data-n':t.name},esc(t.name));b.onclick=function(){show(t.name)};tl.appendChild(b)})}
  function show(n){
    var t=T.filter(function(x){return x.name===n})[0];if(!t)return;$$('button',tl).forEach(function(b){b.classList.toggle('on',b.dataset.n===n)});
    var note=D.tablenotes[n]||'';
    $('#td').innerHTML='<h3 class="mono">'+esc(t.name)+'</h3><span class="tag">'+esc(t.mig)+'</span>'+(note?'<p>'+esc(note)+'</p>':'')+
      '<table><tr><th>column</th><th>type</th><th>notes</th></tr>'+t.cols.map(function(c){return '<tr><td class="mono'+(c.pk?' pk':'')+'">'+esc(c.n)+'</td><td class="mono">'+esc(c.type)+'</td><td>'+(c.pk?'<span class="tag">PK</span> ':'')+(c.nn?'<span class="tag">NOT NULL</span> ':'')+(c.fk?'<button class="chip fk" data-fk="'+esc(c.fk)+'">&rarr; '+esc(c.fk)+'</button>':'')+'</td></tr>'}).join('')+'</table>'+
      '<h4 style="margin-top:14px">Referenced by</h4><div>'+((refBy[n]||[]).map(function(x){return '<button class="chip fk" data-fk="'+esc(x)+'">'+esc(x)+'</button>'}).join('')||'<span class="small">nothing</span>')+'</div>';
    $$('[data-fk]',$('#td')).forEach(function(b){b.onclick=function(){show(b.dataset.fk)}});
  }
  $('#tq').oninput=function(){list(this.value.toLowerCase())};list('');show(T[0].name);
  var by={};T.forEach(function(t){(by[t.mig]=by[t.mig]||[]).push(t.name)});
  el.insertAdjacentHTML('beforeend','<h2 style="margin-top:30px">Which migration made what</h2><div class="grid g3">'+Object.keys(by).sort().map(function(m){return '<div class="card"><b class="mono">'+esc(m)+'</b><p class="small" style="margin:.4em 0 0">'+by[m].map(function(x){return '<code>'+esc(x)+'</code>'}).join(', ')+'</p></div>'}).join('')+'</div>');
};
/* ---------- API ---------- */
R.api=function(el){
  el.innerHTML='<h2>API and background jobs</h2><p class="lead">Everything under <code>/api/v1</code> needs a valid user token (any path, even an unknown one, returns 401 without it). The jobs below run in this order on every heartbeat.</p><div class="row"><input type="search" id="aq" placeholder="Filter routes..." style="max-width:320px" aria-label="Filter routes"></div><div class="card" style="margin-top:10px;overflow:auto"><table id="rt"></table></div>'+
  '<h2 style="margin-top:30px">The run-all chain</h2><div class="row"><button class="btn" id="jplay">Run the chain</button><span class="small">Every 15 minutes a Scheduler call walks these jobs, each with a time budget and a resumable cursor.</span></div><ol class="jobs" id="jl" style="padding:0"></ol>';
  var rt=$('#rt');function draw(q){rt.innerHTML='<tr><th>method</th><th>path</th><th>what it does</th></tr>'+D.routes.filter(function(r){return !q||(r.m+r.p+r.d).toLowerCase().indexOf(q)>-1}).map(function(r){return '<tr><td><span class="m '+r.m+'">'+r.m+'</span></td><td class="mono">'+esc(r.p)+'</td><td>'+esc(r.d)+'</td></tr>'}).join('')}
  draw('');$('#aq').oninput=function(){draw(this.value.toLowerCase())};
  var jl=$('#jl');D.jobs.forEach(function(j){jl.appendChild(h('li',{},'<b>'+esc(j[0])+'</b><span>'+esc(j[1])+'</span>'))});
  var timer=null;$('#jplay').onclick=function(){var it=$$('li',jl),i=0;clearInterval(timer);it.forEach(function(x){x.classList.remove('run')});timer=setInterval(function(){it.forEach(function(x){x.classList.remove('run')});if(i>=it.length){clearInterval(timer);return}it[i].classList.add('run');it[i].scrollIntoView({block:'nearest'});i++},RM?150:700)};
};
/* ---------- PLAYGROUNDS ---------- */
function redact(s){var map={},cnt={};function sub(kind,v){var k=kind+'|'+v;if(!map[k]){cnt[kind]=(cnt[kind]||0)+1;map[k]='['+kind+'_'+cnt[kind]+']'}return map[k]}
  var out=s.replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g,function(m){return sub('EMAIL',m)}).replace(/(\+?\d[\d\s-]{8,}\d)/g,function(m){return sub('PHONE',m)}).replace(/\b\d{2}[A-Za-z]{2,4}\d{3,6}\b/g,function(m){return sub('ROLL',m)}).replace(/\b(Prof\.?|Dr\.?|Mr\.?|Ms\.?|Mrs\.?)\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)?/g,function(m){return sub('PERSON',m)});
  return {out:out,map:map}}
function pad2(n){return (n<10?'0':'')+n}
function fmt(d){return d.toLocaleDateString('en-GB',{weekday:'short',day:'numeric',month:'short'})+' '+pad2(d.getHours())+':'+pad2(d.getMinutes())}
R.lab=function(el){
  el.innerHTML='<h2>Playgrounds</h2><p class="lead">The rules that matter are small enough to run in your browser. Each one is a JavaScript port of what the real code does. Try to break them.</p><div class="grid g2 pg" id="pgs"></div>';
  var g=$('#pgs');
  function box(title,why,body){var c=h('div',{class:'card'},'<h3>'+title+'</h3><p class="small">'+why+'</p>'+body);g.appendChild(c);return c}
  /* 1 redactor */
  var c1=box('1. Redaction','Before any text reaches a model, emails, phones, roll numbers and titled names become placeholders. The mapping lives only in memory for one request.','<label for="r_in">Message</label><textarea id="r_in">Quiz 1 moved. Mail Prof. Rao at rao'+'@'+'example.edu or call +91 98765 43210. Roll 22AB1234 please confirm.</textarea><div class="out" id="r_out"></div><label>Restored in the answer</label><div class="out" id="r_back"></div>');
  function r1(){var r=redact($('#r_in',c1).value);$('#r_out',c1).textContent=r.out;var back=r.out;Object.keys(r.map).forEach(function(k){back=back.split(r.map[k]).join(k.split('|')[1])});$('#r_back',c1).textContent=back}
  $('#r_in',c1).oninput=r1;r1();
  /* 2 swipe */
  var c2=box('2. Swipe rules','Drag the card. Left = dismiss, right = open, up = ask. The direction locks to one axis after 10 px. Distance or a flick decides.','<div class="pad" id="pad"><div class="zl"></div><div class="zl zr"></div><div class="zl zu"></div><div class="c" id="pc">card</div></div><div class="out" id="p_out">Drag the card.</div>');
  (function(){var pad=$('#pad',c2),pc=$('#pc',c2),out=$('#p_out',c2),sx,sy,t0,lock=null,drag=false,W=360,Hh=640;
    function res(dx,dy,dt){var ax=Math.abs(dx),ay=Math.abs(dy);if(!lock)return 'Under 10 px: no axis chosen yet.';
      var v=Math.max(ax,ay)/Math.max(dt,1)*1000;
      if(lock==='x'){var far=ax>=0.35*W,flick=v>800&&ax>24;return (far||flick)?(dx<0?'DISMISS (left)':'OPEN (right)')+' - '+(far?'distance over 35% of width':'flick '+Math.round(v)+' px/s'):'Springs back: '+Math.round(ax/W*100)+'% of width, needs 35% or a flick above 800 px/s.'}
      var up=dy<0,far2=up&&ay>=0.25*Hh,flick2=up&&v>800&&ay>24;return (far2||flick2)?'ASK (up) - '+(far2?'over 25% of height':'upward flick'):'Springs back. Needs an upward drag of 25% of height, or a flick.'}
    pad.onpointerdown=function(e){drag=true;lock=null;sx=e.clientX;sy=e.clientY;t0=performance.now();pad.setPointerCapture(e.pointerId);pc.style.transition='none'};
    pad.onpointermove=function(e){if(!drag)return;var dx=e.clientX-sx,dy=e.clientY-sy;if(!lock&&Math.max(Math.abs(dx),Math.abs(dy))>=10)lock=Math.abs(dx)>=Math.abs(dy)?'x':'y';var mx=lock==='y'?0:dx,my=lock==='x'?0:dy;pc.style.transform='translate('+mx+'px,'+my+'px) rotate('+Math.max(-8,Math.min(8,mx/20))+'deg)';out.textContent='axis: '+(lock||'-')+'   dx '+Math.round(dx)+'  dy '+Math.round(dy)+'\n'+res(dx,dy,performance.now()-t0)};
    function end(e){if(!drag)return;drag=false;pc.style.transition=RM?'none':'transform .25s ease';pc.style.transform='';out.textContent=out.textContent+'\n(released)'}
    pad.onpointerup=end;pad.onpointercancel=end})();
  /* 3 citations */
  var c3=box('3. Citation post-check','The model returns cited numbers. The server drops any that are not in the context, empties them on a refusal, and trims to 120 words.','<label>Context entries available</label><input type="number" id="c_n" value="4" min="0" max="8"><label>Model says cited</label><input type="text" id="c_c" value="1, 2, 7"><label>Answer text</label><textarea id="c_t">Quiz 1 is on Mon 2 Nov at 10:00 [1] in LHC 104 [2]. See also [7].</textarea><label><input type="checkbox" id="c_r" style="width:auto"> refused = true</label><div class="out" id="c_out"></div>');
  function r3(){var n=+$('#c_n',c3).value,cited=$('#c_c',c3).value.split(/[ ,]+/).filter(Boolean).map(Number),ref=$('#c_r',c3).checked,t=$('#c_t',c3).value,drop=[],keep=[];cited.forEach(function(x){(x>=1&&x<=n?keep:drop).push(x)});if(ref)keep=[];
    t=t.replace(/\[(\d+)\]/g,function(m,d){return (+d>=1&&+d<=n&&!ref)?m:''}).replace(/\s{2,}/g,' ');var w=t.trim().split(/\s+/);var trimmed=w.length>120;if(trimmed)t=w.slice(0,120).join(' ')+'...';
    $('#c_out',c3).textContent='kept citations: ['+keep.join(', ')+']\ndropped (not in context): ['+drop.join(', ')+']\n'+(n===0?'NO CONTEXT: the model is never called; the answer is "couldn\'t find it".\n':'')+'answer: '+t+(trimmed?'\n(trimmed to 120 words)':'')}
  $$('input,textarea',c3).forEach(function(i){i.oninput=r3;i.onchange=r3});r3();
  /* 4 timing */
  var now0=new Date();var iso=function(d){return d.getFullYear()+'-'+pad2(d.getMonth()+1)+'-'+pad2(d.getDate())+'T'+pad2(d.getHours())+':'+pad2(d.getMinutes())};
  var c4=box('4. "What day is it?" markers','The chat once refused "when is the next quiz?" because the model did not know today\'s date. Now code adds ALREADY PASSED / today / tomorrow / in N days to every event line.','<label>Today (IST)</label><input type="datetime-local" id="t_now" value="'+iso(now0)+'"><label>Event starts</label><input type="datetime-local" id="t_ev" value="'+iso(new Date(now0.getTime()+3*864e5))+'"><div class="out" id="t_out"></div>');
  function r4(){var n=new Date($('#t_now',c4).value),e=new Date($('#t_ev',c4).value);if(isNaN(n)||isNaN(e))return;var d0=new Date(n.getFullYear(),n.getMonth(),n.getDate()),d1=new Date(e.getFullYear(),e.getMonth(),e.getDate()),days=Math.round((d1-d0)/864e5),m;
    if(e<n&&days===0)m='ALREADY PASSED (earlier today)';else if(days<0)m='ALREADY PASSED ('+(-days)+' day'+(days===-1?'':'s')+' ago)';else if(days===0)m='today';else if(days===1)m='tomorrow';else m='in '+days+' days';
    $('#t_out',c4).textContent='<today>'+fmt(n).split(' ').slice(0,3).join(' ')+'</today>\nQuiz 1 | '+fmt(e)+' | '+m}
  $$('input',c4).forEach(function(i){i.oninput=r4});r4();
  /* 5 reminders */
  var c5=box('5. Reminders follow the event','Reminders store intent, never clock times. Day-before = 20:00. Same-day = 5 hours before, but not earlier than 07:00, and dropped if it is not before the start. Move the event and watch them move.','<label>Event starts</label><input type="datetime-local" id="m_ev" value="'+iso(new Date(new Date(now0.getFullYear(),now0.getMonth(),now0.getDate()+5,10,0)))+'"><label><input type="checkbox" id="m_c" style="width:auto"> event cancelled</label><div class="out" id="m_out"></div>');
  function r5(){var e=new Date($('#m_ev',c5).value);if(isNaN(e))return;if($('#m_c',c5).checked){$('#m_out',c5).textContent='Event is cancelled: both reminders are silenced.\nUncancel it and they come back.';return}
    var day=new Date(e.getFullYear(),e.getMonth(),e.getDate()-1,20,0),seven=new Date(e.getFullYear(),e.getMonth(),e.getDate(),7,0),five=new Date(e.getTime()-5*36e5),same=five<seven?seven:five;
    $('#m_out',c5).textContent='day before : '+fmt(day)+'\nsame day   : '+(same<e?fmt(same):'dropped (would not be before the start)')+(five<seven?'  [clamped to 07:00]':'')}
  $$('input',c5).forEach(function(i){i.oninput=r5;i.onchange=r5});r5();
  /* 6 quiet hours */
  var c6=box('6. Quiet hours','A push that would land in quiet hours waits until they end. Default window 23:00 to 07:00.','<label>Alert becomes due at</label><input type="time" id="q_t" value="23:40"><label>Quiet from</label><input type="time" id="q_a" value="23:00"><label>Quiet until</label><input type="time" id="q_b" value="07:00"><div class="out" id="q_out"></div>');
  function mins(v){var p=v.split(':');return +p[0]*60+ +p[1]}
  function r6(){var t=mins($('#q_t',c6).value),a=mins($('#q_a',c6).value),b=mins($('#q_b',c6).value),inq=a>b?(t>=a||t<b):(t>=a&&t<b);$('#q_out',c6).textContent=inq?'In quiet hours: deferred, the row waits (not_before = '+$('#q_b',c6).value+'). Sent after the window ends.':'Outside quiet hours: sent on the next run.'}
  $$('input',c6).forEach(function(i){i.oninput=r6});r6();
  /* 7 date rules */
  var c7=box('7. Why the model never does dates','The model reports what the message says; code computes the date in IST. A deadline with no time defaults to 23:59 (marked as defaulted). A reschedule with no new time keeps no old time.','<label>Message says</label><select id="d_k"><option value="d">Deadline: "due Friday"</option><option value="m">Moved: "moved to Saturday, same time"</option><option value="n">Moved: "moved to Saturday" (no time)</option></select><label>Posted on</label><input type="datetime-local" id="d_p" value="'+iso(new Date(now0.getFullYear(),now0.getMonth(),now0.getDate(),9,0))+'"><div class="out" id="d_out"></div>');
  function nextDow(d,dow){var x=new Date(d.getFullYear(),d.getMonth(),d.getDate());var add=(dow-x.getDay()+7)%7;if(add===0)add=7;x.setDate(x.getDate()+add);return x}
  function r7(){var p=new Date($('#d_p',c7).value),k=$('#d_k',c7).value;if(isNaN(p))return;var o;if(k==='d'){var f=nextDow(p,5);o='weekday=Friday -> '+fmt(new Date(f.getFullYear(),f.getMonth(),f.getDate(),23,59))+'\ntime defaulted: true (23:59)'}else if(k==='m'){var s=nextDow(p,6);o='weekday=Saturday, time=same -> copy the matched event\'s time\nnew date: '+s.toDateString()+'\nexplicit change language: "moved" -> allowed'}else{var s2=nextDow(p,6);o='weekday=Saturday, time unknown\nnew date: '+s2.toDateString()+'\nold time is DROPPED, never invented -> shown as date only'}
    $('#d_out',c7).textContent=o}
  $$('input,select',c7).forEach(function(i){i.oninput=r7;i.onchange=r7});r7();
};
/* ---------- APP TOUR ---------- */
R.app=function(el){
  var dark=(document.documentElement.dataset.theme!=='light');
  el.innerHTML='<h2>The app, screen by screen</h2><p class="lead">Real screenshots, with the code that powers each screen. Android only, Expo SDK 58.</p><div class="row" id="atabs"></div><div class="tour" style="margin-top:16px"><div class="phone"><img id="aimg" alt="" width="295" height="640"></div><div class="card" id="atxt"></div></div>';
  function show(i){var t=D.tour[i],th=document.documentElement.dataset.theme==='light'?'light':'dark';$$('#atabs button').forEach(function(b,j){b.classList.toggle('on',j===i)});
    var src=t.img.indexOf('notification')===0?t.img+'-590.webp':t.img+'-'+th+'-590.webp';var im=$('#aimg');im.src='../assets/shots/'+src;im.alt=t.title;
    $('#atxt').innerHTML='<h3>'+esc(t.title)+'</h3><p>'+esc(t.text)+'</p><h4 class="small" style="margin-bottom:4px">CODE</h4>'+t.code.map(function(c){return '<code class="chip">'+esc(c)+'</code>'}).join('')+'<h4 class="small" style="margin:14px 0 4px">TRY THIS</h4><p class="small">'+esc(t.q)+'</p>'}
  D.tour.forEach(function(t,i){var b=h('button',{class:'chip'},esc(t.title));b.onclick=function(){show(i)};$('#atabs').appendChild(b)});show(0);
  var o=new MutationObserver(function(){var a=$$('#atabs button.on')[0];if(a)a.click()});o.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
};
/* ---------- INTERNALS ---------- */
R.internals=function(el){
  var areas=['All'].concat(D.mech.map(function(m){return m.area}).filter(function(v,i,a){return a.indexOf(v)===i}));
  el.innerHTML='<h2>How it works inside</h2><p class="lead">The mechanisms you will be asked about, in plain steps, with the files to open.</p><div class="row" id="mf"></div><div class="grid g2" id="mg" style="margin-top:12px"></div>';
  function draw(a){$('#mg').innerHTML=D.mech.filter(function(m){return a==='All'||m.area===a}).map(function(m){return '<div class="card"><span class="tag">'+esc(m.area)+'</span><h3 style="margin-top:6px">'+esc(m.title)+'</h3><ul>'+m.body.map(function(b){return '<li>'+esc(b)+'</li>'}).join('')+'</ul><p style="margin:6px 0 0">'+m.files.map(function(f){return '<code class="chip">'+esc(f)+'</code>'}).join('')+'</p></div>'}).join('')}
  areas.forEach(function(a,i){var b=h('button',{class:'chip'+(i?'':' on')},esc(a));b.onclick=function(){$$('#mf button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');draw(a)};$('#mf').appendChild(b)});draw('All');
};
/* ---------- DECISIONS ---------- */
var DEC_Q='';
function openDecision(id){DEC_Q=id;go('decisions',function(){var i=$('#dq');if(i){$('#dp').value='All';i.value=id;i.dispatchEvent(new Event('input'))}})}
R.decisions=function(el){
  var favs=store('favs')||{};var phases=['All','Important'].concat(D.decisions.map(function(d){return d.phase}).filter(function(v,i,a){return a.indexOf(v)===i}).sort());
  var tags=['all'].concat(Object.keys(D.decisions.reduce(function(o,d){d.tags.forEach(function(t){o[t]=1});return o},{})).sort());
  el.innerHTML='<h2>Decision explorer</h2><p class="lead">'+D.decisions.length+' decisions with the reason for each. Start with the <b>Important</b> filter: the '+D.decisions.filter(function(d){return d.imp}).length+' an interviewer is likely to care about. Use the phase filters to dig deeper.</p><div class="row"><input type="search" id="dq" placeholder="Search text, id or title..." style="max-width:360px" aria-label="Search decisions"><select id="dp" style="max-width:150px" aria-label="Phase">'+phases.map(function(p){return '<option'+(p==='Important'?' selected':'')+'>'+p+'</option>'}).join('')+'</select><select id="dt" style="max-width:170px" aria-label="Tag">'+tags.map(function(p){return '<option>'+p+'</option>'}).join('')+'</select><button class="chip" id="df">&#9733; starred only</button><span class="small" id="dc"></span></div><div class="grid" id="dl" style="margin-top:12px"></div><div class="row" style="margin-top:12px"><button class="btn ghost" id="dm">Show more</button></div>';
  var lim=40,onlyFav=false;
  function filt(){var q=$('#dq').value.toLowerCase(),p=$('#dp').value,t=$('#dt').value;return D.decisions.filter(function(d){return (p==='All'||(p==='Important'?d.imp:d.phase===p))&&(t==='all'||d.tags.indexOf(t)>-1)&&(!onlyFav||favs[d.id])&&(!q||(d.id+' '+d.title+' '+d.text+' '+d.why).toLowerCase().indexOf(q)>-1)})}
  function draw(){var r=filt();$('#dc').textContent=r.length+' shown';$('#dl').innerHTML=r.slice(0,lim).map(function(d){return '<article class="card dec"><div class="meta"><span class="tag">'+esc(d.id)+'</span><span class="tag">phase '+esc(d.phase)+'</span><span class="tag">'+esc(d.date)+'</span>'+d.tags.map(function(t){return '<span class="tag">'+esc(t)+'</span>'}).join('')+'<button class="star'+(favs[d.id]?' on':'')+'" data-s="'+esc(d.id)+'" aria-label="Star" aria-pressed="'+!!favs[d.id]+'" style="margin-left:auto">&#9733;</button></div><h4>'+esc(d.title)+'</h4><p>'+esc(d.text)+'</p>'+(d.why?'<p class="why">'+esc(d.why)+'</p>':'')+'</article>'}).join('');$('#dm').classList.toggle('hide',r.length<=lim);
    $$('[data-s]').forEach(function(b){b.onclick=function(){var i=b.dataset.s;if(favs[i])delete favs[i];else favs[i]=1;store('favs',favs);b.classList.toggle('on',!!favs[i]);b.setAttribute('aria-pressed',!!favs[i])}})}
  ['dq','dp','dt'].forEach(function(i){$('#'+i).oninput=$('#'+i).onchange=function(){lim=40;draw()}});$('#dm').onclick=function(){lim+=40;draw()};
  $('#df').onclick=function(){onlyFav=!onlyFav;this.classList.toggle('on',onlyFav);lim=40;draw()};
  if(DEC_Q){$('#dp').value='All';$('#dq').value=DEC_Q;DEC_Q=''}draw();
};
/* ---------- STORIES ---------- */
R.stories=function(el){
  var areas=['All'].concat(D.stories.map(function(s){return s.area}).filter(function(v,i,a){return a.indexOf(v)===i}));
  el.innerHTML='<h2>War stories</h2><p class="lead">Real bugs and lessons from building this. Interviewers love these: say the symptom, the cause, the fix, and what you learned.</p><div class="row" id="sf"></div><div class="grid g2 story" id="sl" style="margin-top:12px"></div>';
  function draw(a){$('#sl').innerHTML=D.stories.filter(function(s){return a==='All'||s.area===a}).map(function(s){return '<article class="card"><span class="tag">'+esc(s.area)+'</span><h3 style="margin-top:6px">'+esc(s.title)+'</h3><dl><dt>Problem</dt><dd>'+esc(s.problem)+'</dd><dt>Cause</dt><dd>'+esc(s.cause)+'</dd><dt>Fix</dt><dd>'+esc(s.fix)+'</dd><dt>Lesson</dt><dd><b>'+esc(s.lesson)+'</b></dd></dl></article>'}).join('')}
  areas.forEach(function(a,i){var b=h('button',{class:'chip'+(i?'':' on')},esc(a));b.onclick=function(){$$('#sf button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');draw(a)};$('#sf').appendChild(b)});draw('All');
};
/* ---------- INTERVIEW ---------- */
R.interview=function(el){
  var box=store('box')||{};var cats=['All'].concat(D.qa.map(function(q){return q.cat}).filter(function(v,i,a){return a.indexOf(v)===i}));var cat='All',cur=null,mode='cards';
  el.innerHTML='<h2>Interview practice</h2><p class="lead">Say your answer out loud first, then reveal. Cards you miss come back more often (a simple three-box system saved in this browser).</p><div class="row" id="ic"></div><div class="row" style="margin-top:8px"><button class="chip on" data-m="cards">Flashcards</button><button class="chip" data-m="list">All answers</button><button class="chip" id="ireset">Reset progress</button></div><div id="ib" style="margin-top:12px"></div>';
  cats.forEach(function(c,i){var b=h('button',{class:'chip'+(i?'':' on')},esc(c));b.onclick=function(){$$('#ic button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');cat=c;next();render()};$('#ic').appendChild(b)});
  $$('[data-m]',el).forEach(function(b){b.onclick=function(){$$('[data-m]',el).forEach(function(x){x.classList.remove('on')});b.classList.add('on');mode=b.dataset.m;render()}});
  $('#ireset').onclick=function(){box={};store('box',box);next();render()};
  function pool(){return D.qa.map(function(q,i){return {i:i,q:q}}).filter(function(x){return cat==='All'||x.q.cat===cat})}
  function next(){var p=pool();if(!p.length){cur=null;return}var w=p.map(function(x){var b=box[x.i]||1;return b===1?5:b===2?2:1}),tot=w.reduce(function(a,b){return a+b},0),r=Math.random()*tot,k=0;for(;k<p.length-1;k++){r-=w[k];if(r<0)break}if(p.length>1&&cur===p[k].i)k=(k+1)%p.length;cur=p[k].i}
  function stats(){var p=pool(),c=[0,0,0,0];p.forEach(function(x){c[box[x.i]||1]++});return '<div class="boxes" style="margin-bottom:10px"><span>New / missed: '+c[1]+'</span><span>Learning: '+c[2]+'</span><span>Confident: '+c[3]+'</span></div>'}
  function render(){var b=$('#ib');
    if(mode==='list'){b.innerHTML=pool().map(function(x){var q=x.q;return '<details class="qa"><summary>'+esc(q.q)+' <span class="tag">'+esc(q.cat)+'</span></summary><p>'+esc(q.a)+'</p>'+(q.follow?'<p class="small"><b>They might ask next:</b> '+esc(q.follow)+'</p>':'')+'</details>'}).join('');return}
    if(cur==null)next();var q=D.qa[cur];if(!q){b.innerHTML='';return}
    b.innerHTML=stats()+'<div class="fc" id="fc"><div class="face"><span class="tag">'+esc(q.cat)+' &middot; box '+(box[cur]||1)+'</span><p class="q" style="margin-top:10px">'+esc(q.q)+'</p><div class="a"><p>'+esc(q.a)+'</p>'+(q.follow?'<p class="small"><b>They might ask next:</b> '+esc(q.follow)+'</p>':'')+'</div></div></div><div class="row" style="justify-content:center"><button class="btn ghost" id="rv">Reveal (space)</button><button class="btn hide" id="miss" style="background:var(--red);color:#fff">Missed it</button><button class="btn hide" id="got">Got it</button></div>';
    function reveal(){$('#fc').classList.add('show');$('#rv').classList.add('hide');$('#miss').classList.remove('hide');$('#got').classList.remove('hide')}
    $('#rv').onclick=reveal;$('#miss').onclick=function(){box[cur]=1;store('box',box);next();render()};$('#got').onclick=function(){box[cur]=Math.min(3,(box[cur]||1)+1);store('box',box);next();render()};
    b._reveal=reveal}
  document.addEventListener('keydown',function(e){if($('#v-interview').classList.contains('on')&&mode==='cards'&&e.code==='Space'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();var b=$('#ib');if(b._reveal&&!$('#fc').classList.contains('show'))b._reveal()}});
  next();render();
};
/* ---------- GLOSSARY ---------- */
R.gloss=function(el){
  el.innerHTML='<h2>Glossary</h2><p class="lead">'+D.gloss.length+' terms in plain words.</p><input type="search" id="gq" placeholder="Filter terms..." style="max-width:360px" aria-label="Filter terms"><div class="grid g3" id="gl" style="margin-top:12px"></div>';
  function draw(q){$('#gl').innerHTML=D.gloss.filter(function(g){return !q||(g[0]+g[1]).toLowerCase().indexOf(q)>-1}).map(function(g){return '<div class="card"><b>'+esc(g[0])+'</b><p class="small" style="margin:.3em 0 0">'+esc(g[1])+'</p></div>'}).join('')}
  $('#gq').oninput=function(){draw(this.value.toLowerCase())};draw('');
};
/* ---------- WEBSITE ---------- */
R.web=function(el){
  el.innerHTML='<h2>The website</h2><p class="lead">A static page for professors and organisations: no download, a collaboration email instead. It has its own design document and was verified by measurement.</p><div class="grid g3">'+D.website.map(function(w){return '<div class="card"><h3>'+esc(w.title)+'</h3><ul>'+w.body.map(function(b){return '<li>'+esc(b)+'</li>'}).join('')+'</ul></div>'}).join('')+'</div>';
};
/* ---------- SEARCH ---------- */
var idx=null;function build(){idx=[];
  D.decisions.forEach(function(d){idx.push({k:'decisions',t:d.id+' '+d.title,s:d.text,go:function(){openDecision(d.id)}})});
  D.qa.forEach(function(q){idx.push({k:'interview',t:q.q,s:q.a,go:function(){go('interview')}})});
  D.gloss.forEach(function(g){idx.push({k:'gloss',t:g[0],s:g[1],go:function(){go('gloss')}})});
  D.nodes.forEach(function(n){idx.push({k:'map',t:n.label,s:n.what,go:function(){go('map',function(){var e=$$('#svg .node')[D.nodes.indexOf(n)];if(e)e.dispatchEvent(new Event('click'))})}})});
  D.tables.forEach(function(t){idx.push({k:'data',t:t.name,s:t.cols.map(function(c){return c.n}).join(' '),go:function(){go('data',function(){var b=$('#tl [data-n="'+t.name+'"]');if(b)b.click()})}})});
  D.routes.forEach(function(r){idx.push({k:'api',t:r.m+' '+r.p,s:r.d,go:function(){go('api')}})});
  D.stories.forEach(function(s){idx.push({k:'stories',t:s.title,s:s.problem,go:function(){go('stories')}})});
  D.mech.forEach(function(m){idx.push({k:'internals',t:m.title,s:m.body.join(' '),go:function(){go('internals')}})})}
var sov=$('#sov'),sin=$('#sin'),sres=$('#sres'),ssel=0,shown=[];
function openS(){if(!idx)build();sov.classList.add('on');sin.value='';sin.focus();runS('')}
function closeS(){sov.classList.remove('on')}
function runS(q){q=q.toLowerCase().trim();var r=q?idx.filter(function(x){return (x.t+' '+x.s).toLowerCase().indexOf(q)>-1}).sort(function(a,b){return (b.t.toLowerCase().indexOf(q)>-1)-(a.t.toLowerCase().indexOf(q)>-1)}).slice(0,30):[];shown=r;ssel=0;
  sres.innerHTML=q?(r.map(function(x,i){return '<button data-i="'+i+'" class="'+(i?'':'sel')+'"><span class="tag">'+x.k+'</span><span><b>'+esc(x.t)+'</b><br><small>'+esc((x.s||'').slice(0,110))+'</small></span></button>'}).join('')||'<p class="small">No matches.</p>'):'<p class="small">Type to search everything.</p>';
  $$('button',sres).forEach(function(b){b.onclick=function(){pick(+b.dataset.i)}})}
function pick(i){var x=shown[i];if(x){closeS();x.go()}}
sin.oninput=function(){runS(sin.value)};
sin.onkeydown=function(e){if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();ssel=Math.max(0,Math.min(shown.length-1,ssel+(e.key==='ArrowDown'?1:-1)));$$('button',sres).forEach(function(b,i){b.classList.toggle('sel',i===ssel);if(i===ssel)b.scrollIntoView({block:'nearest'})})}else if(e.key==='Enter')pick(ssel)};
sov.onclick=function(e){if(e.target===sov)closeS()};
$('#sbtn').onclick=openS;
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeS();else if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();openS()}});
/* ---------- THEME + BOOT ---------- */
var th=store('theme');if(th)document.documentElement.dataset.theme=th;else if(window.matchMedia&&matchMedia('(prefers-color-scheme: light)').matches)document.documentElement.dataset.theme='light';
$('#tbtn').onclick=function(){var t=document.documentElement.dataset.theme==='light'?'dark':'light';document.documentElement.dataset.theme=t;store('theme',t)};
window.addEventListener('hashchange',function(){go(location.hash.slice(1)||'start')});
go(location.hash.slice(1)||store('tab')||'start');
})();
