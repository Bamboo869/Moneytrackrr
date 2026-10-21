/* stałe strony artykułów (wygenerowane przez docs/artykuly/pages.py):
   kropki rozdziałów, pasek czytania, kopiowanie linku, reklamy, dekoracje Halloween (kod wklejany z aplikacji) */
(function(){
var $=function(i){return document.getElementById(i)};
var H=0;
function stickyH(){var hd=document.querySelector('.hero');var p=hd?getComputedStyle(hd).position:'';H=(p==='sticky'||p==='fixed')?hd.offsetHeight:0;document.documentElement.style.setProperty('--sh',H+'px');return H;}
var CH=[].slice.call(document.querySelectorAll('#rdToc li')).map(function(li){return li.getAttribute('data-c');});
function spy(){var m=$('rdMain');if(!m)return;var r=m.getBoundingClientRect(),vh=innerHeight;
  var done=Math.min(1,Math.max(0,(H-r.top)/Math.max(1,r.height-(vh-H))));
  if(r.bottom<=vh+2||innerHeight+scrollY>=document.documentElement.scrollHeight-4)done=1;
  var pr=$('rdProg');if(pr)pr.style.transform='scaleX('+done+')';
  var f=$('tocFill');if(f)f.style.height=(done*100)+'%';
  var p=$('tocPct');if(p)p.textContent=Math.round(done*100)+'%';
  var act=0;CH.forEach(function(id,i){var el=$(id);if(el&&el.getBoundingClientRect().top<=H+90)act=i;});
  if(done>=.985)act=CH.length-1;
  [].forEach.call(document.querySelectorAll('#rdToc li'),function(li,i){li.classList.toggle('active',i===act);li.classList.toggle('past',i<act);});}
var tk=false;
addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(function(){tk=false;spy();});}},{passive:true});
addEventListener('resize',function(){stickyH();spy();});
/* jak w aplikacji: wstrzymanie animacji podczas przewijania */
var st=0,h=document.documentElement;
addEventListener('scroll',function(){if(!st)h.classList.add('is-scrolling');clearTimeout(st);st=setTimeout(function(){h.classList.remove('is-scrolling');st=0;},180);},{passive:true});
document.addEventListener('click',function(e){
  var t=e.target;if(!t.closest)return;
  var b=t.closest('#rdToc button');
  if(b){var el=$(b.parentNode.getAttribute('data-c'));if(el)scrollTo({top:el.getBoundingClientRect().top+scrollY-H-20,behavior:'smooth'});return;}
  if(t.closest('#rdCopy')){copy();return;}
  if(t.closest('#rdShare')){if(navigator.share)navigator.share({title:document.title,url:location.href.split('#')[0]}).catch(function(){});else copy();}
});
function copy(){var u=location.href.split('#')[0];
  (navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){var c=$('rdCopy');if(c){var t=c.textContent;c.textContent=document.body.getAttribute('data-copied');setTimeout(function(){c.textContent=t;},1600);}}).catch(function(){prompt('',u);});}
stickyH();spy();
[].forEach.call(document.querySelectorAll('ins.adsbygoogle'),function(){try{(window.adsbygoogle=window.adsbygoogle||[]).push({});}catch(_){}});
if(document.documentElement.dataset.theme==='halloween'){
  const BAT=`<svg viewBox="0 0 100 50"><path class="wg" fill="currentColor" d="M47 20 C39 9 22 5 3 12 C10 16 12 21 9 27 C16 22 22 24 24 31 C28 25 34 25 38 31 C40 26 44 26 47 30 Z"/><g transform="translate(100 0) scale(-1 1)"><path class="wg" fill="currentColor" d="M47 20 C39 9 22 5 3 12 C10 16 12 21 9 27 C16 22 22 24 24 31 C28 25 34 25 38 31 C40 26 44 26 47 30 Z"/></g><ellipse cx="50" cy="26" rx="6" ry="10" fill="currentColor"/><circle cx="50" cy="15" r="5.5" fill="currentColor"/><path d="M46 13 L44.5 5 L49 11 Z M54 13 L55.5 5 L51 11 Z" fill="currentColor"/><circle class="eye" cx="48" cy="15" r="1"/><circle class="eye" cx="52" cy="15" r="1"/></svg>`;
  const LEAF=c=>`<svg viewBox="0 0 40 40"><path fill="${c}" d="M20 2 L23 11 L31 7 L28 16 L38 17 L30 23 L34 31 L24 28 L21 38 L19 38 L16 28 L6 31 L10 23 L2 17 L12 16 L9 7 L17 11 Z"/><path d="M20 38 L20 12" stroke="rgba(60,25,8,.6)" stroke-width="1.4"/></svg>`;
  const WEB=`<svg viewBox="0 0 210 210" fill="none" stroke="rgba(225,215,205,.55)" stroke-width="1"><path d="M0 0 L210 30 M0 0 L190 110 M0 0 L120 190 M0 0 L30 210"/>${[40,80,125,170].map(r=>{const p=a=>[Math.cos(a)*r,Math.sin(a)*r];const A=[Math.atan2(30,210),Math.atan2(110,190),Math.atan2(190,120),Math.atan2(210,30)];let d=`M${r} 0`;A.forEach(a=>{const[x,y]=p(a);d+=` Q${(x*0.82).toFixed(1)} ${(y*0.82).toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)}`;});return `<path d="${d}"/>`;}).join('')}</svg>`;
  const SPIDER=`<div class="sp-thread"></div><svg viewBox="0 0 30 30"><g stroke="#0a0604" stroke-width="1.6" fill="none"><path d="M15 15 L4 6 M15 15 L2 14 M15 16 L3 23 M15 17 L6 29 M15 15 L26 6 M15 15 L28 14 M15 16 L27 23 M15 17 L24 29"/></g><ellipse cx="15" cy="16" rx="5" ry="6" fill="#0a0604"/><circle cx="15" cy="9.5" r="3.4" fill="#0a0604"/><circle cx="13.8" cy="9" r=".8" fill="#ff7a1a"/><circle cx="16.2" cy="9" r=".8" fill="#ff7a1a"/></svg>`;
  const PUMPKIN=`<svg viewBox="0 0 80 70"><path d="M38 12 C37 6 40 2 45 1 L46 4 C42 5 41 8 42 12 Z" fill="#4a5a22"/><ellipse cx="24" cy="40" rx="18" ry="26" fill="#c95a12"/><ellipse cx="56" cy="40" rx="18" ry="26" fill="#c95a12"/><ellipse cx="40" cy="40" rx="20" ry="28" fill="#e2731c"/><path class="fire" d="M24 32 L32 26 L33 36 Z M56 32 L48 26 L47 36 Z M38 40 L40 35 L42 40 Z M20 46 C30 58 50 58 60 46 L54 49 L52 45 L47 51 L44 46 L40 52 L36 46 L33 51 L28 45 L26 49 Z"/></svg>`;
  /* nietoperze po bokach: [left/right %, top %, szerokość, czas lotu, opóźnienie, machanie, ukryj na telefonie] */
  const BATS=[[3,22,66,15,0,.30,0],[9,48,44,19,-6,.26,1],[1,70,54,17,-3,.34,1],[90,16,58,18,-9,.28,0],[93,42,72,14,-2,.32,0],[86,64,46,21,-12,.24,1],[48,9,34,24,-5,.22,1]];
  const LEAVES=[[4,'#c8611d',26,19,0],[12,'#a8431a',20,23,-8],[22,'#d9902a',18,27,-15],[78,'#c8611d',22,21,-4],[88,'#7a3e1b',28,17,-11],[95,'#d9902a',20,25,-19],[60,'#a8431a',16,29,-22]];
  function build(){
    const d=document.createElement('div');d.id='spooky';d.setAttribute('aria-hidden','true');
    const hero=document.querySelector('.hero');
    if(hero&&!document.getElementById('spookyHero')){const w=document.createElement('div');w.id='spookyHero';w.setAttribute('aria-hidden','true');w.innerHTML=`<div class="sp-web">${WEB}</div><div class="sp-web r">${WEB}</div><div class="sp-spider">${SPIDER}</div>`;hero.insertBefore(w,hero.firstChild);}
    let h=`<div class="sp-moon"></div><div class="sp-fog"></div><div class="sp-fog b"></div><div class="sp-pk l">${PUMPKIN}</div><div class="sp-pk r">${PUMPKIN}</div>`;
    BATS.forEach(([x,y,w,dur,dl,f,hm],i)=>{const r=(i*37%7)-3;h+=`<div class="sp-bat${hm?' hm':''}" style="left:${x}%;top:${y}%;--w:${w}px;--d:${dur}s;--dl:${dl}s;--f:${f}s;--x1:${30+r*8}px;--y1:${-40-r*6}px;--x2:${-35+r*5}px;--y2:${-90+r*9}px;--x3:${25-r*6}px;--y3:${-30+r*4}px">${BAT}</div>`;});
    LEAVES.forEach(([x,c,w,dur,dl],i)=>{h+=`<div class="sp-leaf${i%3===2?' hm':''}" style="left:${x}%;--w:${w}px;--d:${dur}s;--dl:${dl}s;--dx:${i%2?-70:70}px;--r:${i%2?-480:600}deg;--s:${2.6+i*.3}s">${LEAF(c)}</div>`;});
    d.innerHTML=h;document.body.insertBefore(d,document.body.firstChild);
  }
  try{build();}catch(e){}
}
})();
