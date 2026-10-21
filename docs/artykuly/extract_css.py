"""Wyciąga z aplikacji (site/index.html) style potrzebne stałym stronom artykułów:
nagłówek, czytnik (kropki rozdziałów, pasek czytania, boczne kolumny), stopka, motywy i dekoracje Halloween.
Zapisuje site/assets/reader.css. Uruchamiaj po zmianach wyglądu czytnika:  python3 docs/artykuly/extract_css.py
Wymaga Playwright + Chromium."""
import os,sys
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT=os.path.join(ROOT,'site','assets','reader.css')
JS=r"""()=>{
  const scope=new Set([document.documentElement,document.body]);
  for(const sel of ['.page','.hero','#view-reader','footer.site','#spooky','#spookyHero'])
    document.querySelectorAll(sel).forEach(r=>{scope.add(r);r.querySelectorAll('*').forEach(e=>scope.add(e));});
  // .page i rodzic czytnika
  const simp=s=>{let x=s.replace(/::?[a-zA-Z-]+(\([^)]*\))?/g,m=>/^:(not|is|where)\(/.test(m)?'':'')
     .replace(/\[data-theme=[^\]]+\]/g,'').replace(/html\.[\w-]+/g,'html').replace(/html\[[^\]]+\]/g,'html').trim();
     x=x.replace(/\s+>/g,' >').replace(/>\s*$/,'').trim();return x||':root';};
  const used=sel=>sel.split(',').some(p=>{const s=simp(p);if(s===':root'||s==='html'||s==='*'||s==='body')return true;
     try{for(const e of document.querySelectorAll(s))if(scope.has(e))return true;}catch(_){return false;}return false;});
  const out=[];
  const walk=(rules,ind)=>{for(const r of rules){
    if(r.type===1){if(used(r.selectorText))out.push(r.cssText);}
    else if(r.type===4){const before=out.length;out.push('@media '+r.conditionText+'{');const n=out.length;walk(r.cssRules);if(out.length===n)out.splice(before,2);else out.push('}');}
    else if(r.type===12){const before=out.length;out.push('@supports '+r.conditionText+'{');const n=out.length;walk(r.cssRules);if(out.length===n)out.splice(before,2);else out.push('}');}
    else if(r.type===7){out.push(r.cssText);}
  }};
  for(const sh of document.styleSheets){try{walk(sh.cssRules);}catch(_){}}
  return out.join('\n');
}"""
EXTRA="""
/* --- dodatki stałych stron artykułów --- */
a.sug{color:inherit;text-decoration:none}a.sug:hover b{color:var(--blue)}
.rd-top a.btn-small{text-decoration:none;color:inherit;display:inline-block}
.hero h1 a{color:inherit;text-decoration:none}
.hero-right a.ibtn{color:var(--text)}
.cta-card a.cbtn{display:block;text-align:center;text-decoration:none}
.rd-crumbs{font-size:13px;color:var(--muted);margin:0 0 6px}.rd-crumbs a{color:var(--muted)}
.ls-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:18px;margin-top:22px}
.ls-card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;text-decoration:none;color:var(--text);transition:transform .2s,border-color .2s}
.ls-card:hover{transform:translateY(-3px);border-color:var(--blue)}
.ls-card img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--panel2)}
.ls-card div{padding:14px 16px}.ls-card small{color:var(--muted);font-size:12.5px}.ls-card b{display:block;font-size:17px;line-height:1.3;margin:4px 0}
.ls-card p{margin:0;color:var(--muted);font-size:14px;line-height:1.5}
.ls-wrap{max-width:1180px;margin:0 auto}.ls-wrap h1{font-size:clamp(30px,4.5vw,44px);letter-spacing:-.02em;margin:6px 0 8px}.ls-lead{color:var(--muted);font-size:17px;max-width:760px;line-height:1.6}
.about{max-width:760px;margin:0 auto;font-size:17px;line-height:1.75}.about h1{font-size:clamp(30px,4.5vw,42px)}.about h2{margin-top:1.6em}.about a{color:var(--blue)}
"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1366,'height':900})
    pg.goto('file://'+os.path.join(ROOT,'site','index.html'));pg.wait_for_timeout(1000)
    pg.evaluate("document.querySelectorAll('.modal-overlay.open').forEach(m=>m.classList.remove('open'));S.theme='halloween';applyTheme();go('news');document.querySelector('.feat').click()")
    pg.wait_for_timeout(700)
    css=pg.evaluate(JS)
    b.close()
os.makedirs(os.path.dirname(OUT),exist_ok=True)
open(OUT,'w',encoding='utf-8').write('/* wygenerowane z aplikacji przez docs/artykuly/extract_css.py – nie edytuj ręcznie */\n'+css+EXTRA)
print('reader.css',len(css)//1024,'KB')
