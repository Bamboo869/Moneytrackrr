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
__SPOOKY__
  try{build();}catch(e){}
}
})();
