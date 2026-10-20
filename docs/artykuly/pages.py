"""Statyczne strony artykułów pod SEO (v0.22).

Uruchamiaj z katalogu repo:  python3 docs/artykuly/pages.py
(build.py wywołuje go automatycznie na końcu).

Tworzy w site/:
  a/<slug>/index.html            – artykuł PL
  en/a/<slugEn>/index.html       – artykuł EN
  aktualnosci/, poradniki/, en/news/, en/guides/   – spisy
  o-nas/, en/about/              – strona redakcji
  sitemap.xml                    – mapa strony z wersjami językowymi
Źródłem jest DEFAULT_ARTICLES w site/index.html (czyli to samo, co widzi aplikacja).
"""
import json,re,os,html,shutil,unicodedata,datetime
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE=os.path.join(ROOT,'site');P=os.path.join(SITE,'index.html')
BASE='https://moneytrackrr.app'
AD_CLIENT='ca-pub-6452210585951054';AD_SLOT='2475490560'
THIN=1200   # krótsze teksty: noindex i poza mapą strony
TAG_EN={'Paliwa':'Fuel','Bezpieczeństwo':'Security','Rynki':'Markets','Inflacja':'Inflation','Praca':'Work','Oszczędzanie':'Savings',
        'Długi':'Debt','Aplikacja':'App','Budżet':'Budget','Poradnik':'Guide','Podatki':'Taxes','Krypto':'Crypto'}
TAG_EMO={'Inflacja':'📈','Oszczędzanie':'🐷','Budżet':'🧮','Rynki':'🌍','Paliwa':'⛽','Krypto':'🪙','Poradnik':'📘','Podatki':'🧾',
         'Bezpieczeństwo':'🛡️','Praca':'👷','Długi':'💳','Aplikacja':'🪙'}
MON_PL=['stycznia','lutego','marca','kwietnia','maja','czerwca','lipca','sierpnia','września','października','listopada','grudnia']
MON_EN=['January','February','March','April','May','June','July','August','September','October','November','December']
esc=lambda s:html.escape(str(s or ''),quote=True)

def slugify(s,maxlen=80):
    s=unicodedata.normalize('NFKD',s.replace('ł','l').replace('Ł','L')).encode('ascii','ignore').decode().lower()
    s=re.sub(r'[^a-z0-9]+','-',s).strip('-')
    if len(s)>maxlen: s=s[:maxlen].rsplit('-',1)[0]
    return s

def load():
    s=open(P,encoding='utf-8').read()
    i=s.index('const DEFAULT_ARTICLES=')+len('const DEFAULT_ARTICLES=')
    A,_=json.JSONDecoder().raw_decode(s,i)
    return [a for a in A if a.get('status','published')!='draft' and a.get('slug')]

def img(ref,w=1200):
    if not ref:return ''
    if ref.startswith('img:'):return f'/img/{ref[4:]}.jpg'
    if ref.startswith('https://images.unsplash.com/'):
        u=re.sub(r'([?&])w=\d+',rf'\g<1>w={w}',ref);return re.sub(r'([?&])q=\d+',r'\1q=70',u)
    return ref if ref.startswith('https://') else ''
def srcset(ref):
    if not ref or not ref.startswith('https://images.unsplash.com/'):return ''
    return ' srcset="'+', '.join(f'{esc(img(ref,w))} {w}w' for w in (640,1000,1400))+'" sizes="(max-width:820px) 100vw, 760px"'

def md(src):
    """port mdFull z aplikacji (+ listy numerowane); zwraca (html, rozdziały)"""
    def inl(s):
        s=esc(s)
        s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s);s=re.sub(r'\*(.+?)\*',r'<em>\1</em>',s)
        s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',r'<a href="\2" target="_blank" rel="noopener nofollow">\1</a>',s)
        return s
    out=[];para=[];lst=[None];chs=[]
    def fp():
        if para:out.append('<p>'+inl(' '.join(para))+'</p>');para.clear()
    def fl():
        if lst[0]:out.append(f'</{lst[0]}>');lst[0]=None
    for l in str(src or '').replace('\r','').split('\n'):
        t=l.strip()
        if not t:fp();fl();continue
        m=re.match(r'^##\s+(.*)$',t)
        if m:fp();fl();cid=f'ch-{len(chs)}';chs.append((cid,m.group(1)));out.append(f'<h2 id="{cid}">{inl(m.group(1))}</h2>');continue
        m=re.match(r'^###\s+(.*)$',t)
        if m:fp();fl();out.append('<h3>'+inl(m.group(1))+'</h3>');continue
        m=re.match(r'^!\[([^\]]*)\]\(([^)\s]+)\)$',t)
        if m:
            fp();fl();s=img(m.group(2))
            if s:out.append(f'<figure><img loading="lazy" decoding="async" src="{esc(s)}"{srcset(m.group(2))} alt="{esc(m.group(1))}">'+(f'<figcaption>{esc(m.group(1))}</figcaption>' if m.group(1) else '')+'</figure>')
            continue
        for kind,rx in (('ul',r'^[-*]\s+'),('ol',r'^\d+\.\s+')):
            if re.match(rx,t):
                fp()
                if lst[0]!=kind:fl();out.append(f'<{kind}>');lst[0]=kind
                out.append('<li>'+inl(re.sub(rx,'',t))+'</li>');break
        else:
            if re.match(r'^>\s',t):fp();fl();out.append('<blockquote>'+inl(re.sub(r'^>\s+','',t))+'</blockquote>');continue
            fl();para.append(t)
    fp();fl();return '\n'.join(out),chs

PENNY='<svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="#e9a915" stroke="#b8800c" stroke-width="2"/><circle cx="32" cy="32" r="24" fill="#ffd24a" stroke="#e9a915" stroke-width="2"/><path d="M14 22 A21 21 0 0 1 30 10" fill="none" stroke="#fff3c2" stroke-width="3" stroke-linecap="round" opacity=".8"/><g fill="#3a2a06"><ellipse cx="25" cy="29" rx="3" ry="3.6"/><ellipse cx="39" cy="29" rx="3" ry="3.6"/></g><circle cx="19" cy="37" r="3" fill="#ff8a8a" opacity=".45"/><circle cx="45" cy="37" r="3" fill="#ff8a8a" opacity=".45"/><path d="M22 37 Q32 46 42 37" fill="none" stroke="#3a2a06" stroke-width="2.6" stroke-linecap="round"/></svg>'

CSS=""":root{--bg:#f6efe2;--panel:#fffaf0;--line:#e6d9bf;--text:#2a2016;--muted:#6b5a44;--acc:#b9722f;--acc2:#c96a1c;color-scheme:light dark}
@media(prefers-color-scheme:dark){:root{--bg:#14100c;--panel:#1d1711;--line:#352a1f;--text:#f3e9dc;--muted:#b3a38f;--acc:#e09a52;--acc2:#ff9a3c}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;background:var(--bg);color:var(--text);font:18px/1.7 system-ui,-apple-system,"Segoe UI",Roboto,Inter,sans-serif}
a{color:var(--acc2)}img{max-width:100%;height:auto}
.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top-in{max-width:1080px;margin:0 auto;padding:12px 18px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.logo{font-weight:900;font-size:22px;letter-spacing:-.02em;color:var(--text);text-decoration:none}.logo span{color:var(--acc2)}
.nav{display:flex;gap:14px;align-items:center;margin-left:auto;font-size:15px;font-weight:600;flex-wrap:wrap}.nav a{color:var(--muted);text-decoration:none}.nav a:hover{color:var(--text)}
.btn{display:inline-block;background:var(--acc2);color:#fff!important;font-weight:800;padding:9px 16px;border-radius:999px;text-decoration:none}
main{max-width:760px;margin:0 auto;padding:22px 18px 60px}
.crumbs{font-size:14px;color:var(--muted)}.crumbs a{color:var(--muted)}
.tag{display:inline-block;font-size:13px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:var(--acc2);background:color-mix(in srgb,var(--acc2) 12%,transparent);padding:4px 10px;border-radius:999px;margin-top:16px}
h1{font-size:clamp(30px,5vw,44px);line-height:1.15;letter-spacing:-.02em;margin:12px 0 10px}
h2{font-size:26px;line-height:1.25;margin:1.8em 0 .5em}h3{font-size:21px;margin:1.4em 0 .4em}
.meta{font-size:14.5px;color:var(--muted);margin-bottom:18px}
.lead{font-size:20px;line-height:1.6;border-left:4px solid var(--acc2);padding-left:16px;margin:0 0 22px}
.cover{margin:0 0 26px}.cover img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:16px;background:var(--panel)}
figure{margin:1.6em 0}figure img{border-radius:14px;display:block}figcaption{font-size:14px;color:var(--muted);text-align:center;margin-top:6px}
blockquote{margin:1.2em 0;padding:.4em 1em;border-left:4px solid var(--line);color:var(--muted)}
.toc{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:0 0 26px;font-size:16px}.toc b{display:block;margin-bottom:4px}.toc ol{margin:0;padding-left:20px}
.cta{display:flex;gap:16px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:20px;margin:36px 0}
.cta p{margin:0 0 10px;font-size:16.5px;line-height:1.5}.cta b{font-size:19px}
.ad{margin:30px 0;min-height:0}.ad small{display:none;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}.ad:has(ins[data-ad-status="filled"]) small{display:block}
.rel h2{font-size:22px}.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;text-decoration:none;color:var(--text)}
.card img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}.card div{padding:12px 14px}.card b{display:block;line-height:1.3;font-size:16.5px}.card span{font-size:13px;color:var(--muted)}
.card p{font-size:14.5px;line-height:1.5;color:var(--muted);margin:6px 0 0}
.wide{max-width:1080px}
footer{border-top:1px solid var(--line);font-size:14px;color:var(--muted)}footer div{max-width:1080px;margin:0 auto;padding:22px 18px;display:flex;gap:16px;flex-wrap:wrap}footer a{color:var(--muted)}
@media(max-width:600px){body{font-size:17px}.nav .hide-s{display:none}.top-in{gap:10px;padding:10px 14px;flex-wrap:nowrap}.logo{font-size:19px;white-space:nowrap}.nav{gap:10px;font-size:14px;flex-wrap:nowrap}.btn{padding:7px 12px;white-space:nowrap}.cta{flex-direction:column;align-items:flex-start}}
"""
L={'pl':dict(news='Aktualności',guides='Poradniki',about='O nas',app='Otwórz aplikację',home='Strona główna',read='min czytania',
             by='Redakcja Money Trackrr',toc='W tym artykule',rel_news='Czytaj też',rel_guide='Inne poradniki',ad='Reklama',
             cta_t='Sprawdź, dokąd naprawdę płyną Twoje pieniądze',cta_p='Money Trackrr to darmowy tracker wydatków i budżetu. Bez konta, działa offline, dane zostają w Twojej przeglądarce.',
             cta_b='Otwórz Money Trackrr →',open_app='Otwórz w aplikacji',other='English version',terms='Regulamin',
             news_h='Aktualności finansowe',news_i='Najważniejsze wiadomości ze świata i z Polski – wyjaśnione prosto: co się stało i co to znaczy dla Twojego portfela. Zawsze z podanymi źródłami.',
             guides_h='Poradniki o pieniądzach',guides_i='Jak oszczędzać, budżetować, wyjść z długów i korzystać z Money Trackrr – krok po kroku, bez żargonu.'),
   'en':dict(news='News',guides='Guides',about='About',app='Open the app',home='Home',read='min read',
             by='Money Trackrr editorial team',toc='In this article',rel_news='Read next',rel_guide='More guides',ad='Advertisement',
             cta_t='See where your money really goes',cta_p='Money Trackrr is a free expense and budget tracker. No account, works offline, your data stays in your browser.',
             cta_b='Open Money Trackrr →',open_app='Open in the app',other='Wersja polska',terms='Terms',
             news_h='Money news',news_i='The most important news from Poland and the world – explained simply: what happened and what it means for your wallet. Always with sources.',
             guides_h='Money guides',guides_i='How to save, budget, get out of debt and use Money Trackrr – step by step, no jargon.')}

def fmt_date(d,lang):
    y,m,dd=map(int,d.split('-'))
    return f'{dd} {MON_PL[m-1]} {y}' if lang=='pl' else f'{dd} {MON_EN[m-1]} {y}'
def words(t):return len(re.findall(r'\w+',t or ''))

def shell(lang,title,desc,canon,alt,body,ld,og_img=None,og_type='website',extra_head='',robots='index,follow,max-image-preview:large',wide=False):
    l=L[lang];other='en' if lang=='pl' else 'pl'
    hl=''
    if alt:
        hl=f'<link rel="alternate" hreflang="{lang}" href="{BASE}{canon}"><link rel="alternate" hreflang="{other}" href="{BASE}{alt}"><link rel="alternate" hreflang="x-default" href="{BASE}{canon if lang=="pl" else alt}">'
    nav_news='/aktualnosci/' if lang=='pl' else '/en/news/';nav_g='/poradniki/' if lang=='pl' else '/en/guides/';nav_a='/o-nas/' if lang=='pl' else '/en/about/'
    lang_link=f'<a class="hide-s" href="{alt}" hreflang="{other}">{"EN" if lang=="pl" else "PL"}</a>' if alt else ''
    og=f'<meta property="og:image" content="{esc(og_img)}"><meta name="twitter:card" content="summary_large_image">' if og_img else '<meta name="twitter:card" content="summary">'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{BASE}{canon}">{hl}
<meta property="og:site_name" content="Money Trackrr"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{canon}"><meta property="og:locale" content="{'pl_PL' if lang=='pl' else 'en_US'}">{og}
<meta name="theme-color" content="#f6efe2">
<meta name="google-adsense-account" content="{AD_CLIENT}">
<link rel="icon" href="/favicon.ico"><link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
{extra_head}<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False).replace('</','<\\/')}</script>
</head>
<body>
<header class="top"><div class="top-in"><a class="logo" href="/">Money <span>Trackrr</span></a><nav class="nav"><a href="{nav_news}">{l['news']}</a><a class="hide-s" href="{nav_g}">{l['guides']}</a><a class="hide-s" href="{nav_a}">{l['about']}</a>{lang_link}<a class="btn" href="/#tracker">{l['app']}</a></nav></div></header>
<main{' class="wide"' if wide else ''}>
{body}
</main>
<footer><div><span>© {datetime.date.today().year} Money Trackrr</span><a href="{nav_a}">{l['about']}</a><a href="{nav_news}">{l['news']}</a><a href="{nav_g}">{l['guides']}</a><a href="https://www.tiktok.com/@moneytrackrr" rel="noopener">TikTok</a><a href="https://buymeacoffee.com/moneytrackrr" rel="noopener">Buy me a coffee</a></div></footer>
</body>
</html>
'''

def write(path,txt):
    full=os.path.join(SITE,path.strip('/'),'index.html');os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w',encoding='utf-8').write(txt)

def org():
    return {'@type':'Organization','name':'Money Trackrr','url':BASE+'/','logo':{'@type':'ImageObject','url':BASE+'/icons/icon-512.png'}}

def build():
    A=load()
    for a in A:
        a['slugEn']=a.get('slugEn') or slugify(a.get('titleEn') or a['title'])
    by_kind=lambda k:sorted([a for a in A if (a.get('kind')=='guide')==(k=='guide')],key=lambda a:a.get('date',''),reverse=True)
    # wyczyść stare wygenerowane strony
    for d in ['a','en/a']:shutil.rmtree(os.path.join(SITE,d),ignore_errors=True)
    urls=[]  # (pl_path,en_path,lastmod,indexable)
    for a in A:
        for lang in ('pl','en'):
            l=L[lang];en=lang=='en'
            if en and not a.get('bodyEn'):continue
            title=a.get('titleEn') if en else a['title'];summ=(a.get('summaryEn') if en else a.get('summary')) or '';body=(a.get('bodyEn') if en else a.get('body')) or ''
            path=f"/en/a/{a['slugEn']}/" if en else f"/a/{a['slug']}/"
            alt=(f"/a/{a['slug']}/" if en else (f"/en/a/{a['slugEn']}/" if a.get('bodyEn') else None))
            thin=len(body)<THIN
            html_body,chs=md(body)
            tag=TAG_EN.get(a.get('tag'),a.get('tag')) if en else a.get('tag')
            kind=a.get('kind','news');k_path=('/en/guides/' if en else '/poradniki/') if kind=='guide' else ('/en/news/' if en else '/aktualnosci/')
            k_name=l['guides'] if kind=='guide' else l['news']
            cover=img(a.get('cover'),1200)
            mins=max(1,round(words(body)/200))
            toc=('<nav class="toc"><b>'+l['toc']+'</b><ol>'+''.join(f'<li><a href="#{cid}">{esc(re.sub(r"[*]","",t))}</a></li>' for cid,t in chs if not re.match(r'^(W skrócie|In short)$',t))+'</ol></nav>') if len(chs)>=3 else ''
            ads=a.get('tag')!='Aplikacja'
            ad=(f'<div class="ad"><small>{l["ad"]}</small><ins class="adsbygoogle" style="display:block" data-ad-client="{AD_CLIENT}" data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>') if ads else ''
            rel=[r for r in by_kind(kind) if r is not a and (not en or r.get('bodyEn'))][:3]
            rel_html=''.join(f'<a class="card" href="{("/en/a/"+r["slugEn"]) if en else ("/a/"+r["slug"])}/"><img loading="lazy" src="{esc(img(r.get("cover"),640))}" alt=""><div><span>{fmt_date(r["date"],lang)}</span><b>{esc(r.get("titleEn") if en else r["title"])}</b></div></a>' for r in rel)
            app_link=f"/#{'guides' if kind=='guide' else 'news'}/{a['slug']}"
            body_html=f'''<div class="crumbs"><a href="/">{l['home']}</a> › <a href="{k_path}">{k_name}</a></div>
<article>
<span class="tag">{TAG_EMO.get(a.get('tag'),'📰')} {esc(tag)}</span>
<h1>{esc(title)}</h1>
<div class="meta"><time datetime="{a['date']}">{fmt_date(a['date'],lang)}</time> · {mins} {l['read']} · {l['by']}</div>
<p class="lead">{esc(summ)}</p>
{f'<figure class="cover"><img src="{esc(cover)}"{srcset(a.get("cover"))} alt="{esc(title if en else (a.get("coverAlt") or title))}" fetchpriority="high"></figure>' if cover else ''}
{toc}
{html_body}
</article>
{ad}
<aside class="cta">{PENNY}<div><b>{l['cta_t']}</b><p>{l['cta_p']}</p><a class="btn" href="/?ref=article#tracker">{l['cta_b']}</a></div></aside>
{f'<section class="rel"><h2>{l["rel_guide"] if kind=="guide" else l["rel_news"]}</h2><div class="cards">{rel_html}</div></section>' if rel_html else ''}'''
            ld=[{'@context':'https://schema.org','@type':'NewsArticle' if kind!='guide' else 'Article','headline':title[:110],'description':summ,
                 'image':[cover] if cover else [],'datePublished':a['date']+'T08:00:00+02:00','dateModified':a['date']+'T08:00:00+02:00',
                 'inLanguage':lang,'author':{'@type':'Organization','name':l['by'],'url':BASE+('/en/about/' if en else '/o-nas/')},
                 'publisher':org(),'mainEntityOfPage':BASE+path,'articleSection':tag},
                {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
                 {'@type':'ListItem','position':1,'name':l['home'],'item':BASE+'/'},
                 {'@type':'ListItem','position':2,'name':k_name,'item':BASE+k_path},
                 {'@type':'ListItem','position':3,'name':title,'item':BASE+path}]}]
            head=f'<meta property="article:published_time" content="{a["date"]}T08:00:00+02:00">'+(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={AD_CLIENT}" crossorigin="anonymous"></script>' if ads else '')
            desc=summ if len(summ)<=160 else summ[:157].rsplit(' ',1)[0]+'…'
            write(path,shell(lang,f'{title} | Money Trackrr',desc,path,alt,body_html,ld,cover or None,'article',head,
                             'noindex,follow' if thin else 'index,follow,max-image-preview:large'))
            if not en: urls.append((path,alt,a['date'],not thin))
    # ---- spisy ----
    for lang in ('pl','en'):
        l=L[lang];en=lang=='en'
        for kind in ('news','guide'):
            items=[a for a in by_kind(kind) if not en or a.get('bodyEn')]
            path=('/en/guides/' if en else '/poradniki/') if kind=='guide' else ('/en/news/' if en else '/aktualnosci/')
            alt=('/poradniki/' if en else '/en/guides/') if kind=='guide' else ('/aktualnosci/' if en else '/en/news/')
            h=l['guides_h'] if kind=='guide' else l['news_h'];intro=l['guides_i'] if kind=='guide' else l['news_i']
            cards=''.join(f'<a class="card" href="{("/en/a/"+a["slugEn"]) if en else ("/a/"+a["slug"])}/"><img loading="lazy" src="{esc(img(a.get("cover"),640))}" alt="{esc(a.get("coverAlt") or "")}"><div><span>{TAG_EMO.get(a.get("tag"),"📰")} {esc(TAG_EN.get(a.get("tag"),a.get("tag")) if en else a.get("tag"))} · {fmt_date(a["date"],lang)}</span><b>{esc(a.get("titleEn") if en else a["title"])}</b><p>{esc((a.get("summaryEn") if en else a.get("summary")) or "")[:150]}…</p></div></a>' for a in items)
            body=f'<div class="crumbs"><a href="/">{l["home"]}</a></div><h1>{h}</h1><p class="lead">{intro}</p><div class="cards">{cards}</div><aside class="cta">{PENNY}<div><b>{l["cta_t"]}</b><p>{l["cta_p"]}</p><a class="btn" href="/?ref=list#tracker">{l["cta_b"]}</a></div></aside>'
            ld={'@context':'https://schema.org','@type':'CollectionPage','name':h,'description':intro,'inLanguage':lang,'url':BASE+path,'publisher':org(),
                'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+(f'/en/a/{a["slugEn"]}/' if en else f'/a/{a["slug"]}/')} for i,a in enumerate(items)]}}
            write(path,shell(lang,f'{h} | Money Trackrr',intro[:158],path,alt,body,ld,None,'website','',wide=True))
    # ---- O nas ----
    ABOUT={'pl':('O nas – kim jesteśmy i jak piszemy','Money Trackrr to darmowe narzędzie do budżetu domowego i serwis z wiadomościami o pieniądzach. Wyjaśniamy, kto za nim stoi i jak powstają artykuły.',
f'''<h1>O nas</h1><p class="lead">Money Trackrr to mały, niezależny projekt: darmowy tracker wydatków i budżetu oraz serwis, który tłumaczy wiadomości ze świata finansów na język domowego portfela.</p>
<h2>Narzędzie</h2><p>Tracker działa w przeglądarce i offline, bez zakładania konta. Twoje dane zostają na Twoim urządzeniu – nie wysyłamy ich na żaden serwer i nie przekazujemy reklamodawcom. Możesz zainstalować go jak aplikację na telefonie i komputerze.</p>
<h2>Jak powstają artykuły</h2><ul>
<li><strong>Zawsze podajemy źródła.</strong> Pod każdym tekstem znajdziesz linki do materiałów, na których się opieramy: instytucji publicznych, agencji informacyjnych i serwisów finansowych.</li>
<li><strong>Fakty według stanu na dzień publikacji.</strong> Liczby (ceny, kursy, stopy procentowe) podajemy z datą – sytuacja może się później zmienić.</li>
<li><strong>Co to znaczy dla Ciebie.</strong> Każdy tekst kończymy praktycznym wyjaśnieniem, jak dana wiadomość wpływa na domowy budżet.</li>
<li><strong>Bez porad inwestycyjnych.</strong> Nasze materiały mają charakter informacyjny i edukacyjny. Nie są rekomendacją kupna ani sprzedaży czegokolwiek.</li>
<li><strong>Narzędzia AI.</strong> Przy researchu i redakcji tekstów korzystamy z pomocy narzędzi AI. Fakty sprawdzamy w źródłach podanych pod artykułem.</li>
<li><strong>Poprawki.</strong> Jeśli znajdziesz błąd, napisz do nas – poprawimy tekst i zaktualizujemy datę.</li></ul>
<h2>Finansowanie</h2><p>Projekt jest darmowy. Utrzymują go reklamy Google wyświetlane wyłącznie w artykułach (nigdy w samym trackerze) oraz dobrowolne wsparcie na <a href="https://buymeacoffee.com/moneytrackrr" rel="noopener">Buy me a coffee</a>.</p>
<h2>Kontakt</h2><p>Najszybciej przez TikToka: <a href="https://www.tiktok.com/@moneytrackrr" rel="noopener">@moneytrackrr</a>.</p>
<aside class="cta">{PENNY}<div><b>{L['pl']['cta_t']}</b><p>{L['pl']['cta_p']}</p><a class="btn" href="/?ref=about#tracker">{L['pl']['cta_b']}</a></div></aside>'''),
     'en':('About us – who we are and how we write','Money Trackrr is a free household budget tool and a money news site. Here is who is behind it and how our articles are made.',
f'''<h1>About us</h1><p class="lead">Money Trackrr is a small, independent project: a free expense and budget tracker, plus a site that translates financial news into what it means for your wallet.</p>
<h2>The tool</h2><p>The tracker runs in your browser and offline, with no account. Your data stays on your device – we never send it to a server or share it with advertisers. You can install it like an app on your phone or computer.</p>
<h2>How our articles are made</h2><ul>
<li><strong>We always cite sources.</strong> Below every article you will find links to the material we rely on: public institutions, news agencies and financial outlets.</li>
<li><strong>Facts as of the publication date.</strong> Numbers (prices, exchange rates, interest rates) come with a date – things may change later.</li>
<li><strong>What it means for you.</strong> Every article ends with a practical explanation of how the news affects a household budget.</li>
<li><strong>No investment advice.</strong> Our content is for information and education only. It is not a recommendation to buy or sell anything.</li>
<li><strong>AI tools.</strong> We use AI tools to help with research and editing. Facts are checked against the sources listed below each article.</li>
<li><strong>Corrections.</strong> If you spot a mistake, tell us – we will fix it and update the date.</li></ul>
<h2>Funding</h2><p>The project is free. It is supported by Google ads shown only in articles (never in the tracker itself) and by voluntary support on <a href="https://buymeacoffee.com/moneytrackrr" rel="noopener">Buy me a coffee</a>.</p>
<h2>Contact</h2><p>The fastest way is TikTok: <a href="https://www.tiktok.com/@moneytrackrr" rel="noopener">@moneytrackrr</a>.</p>
<aside class="cta">{PENNY}<div><b>{L['en']['cta_t']}</b><p>{L['en']['cta_p']}</p><a class="btn" href="/?ref=about#tracker">{L['en']['cta_b']}</a></div></aside>''')}
    for lang,(t,d,b) in ABOUT.items():
        path='/o-nas/' if lang=='pl' else '/en/about/';alt='/en/about/' if lang=='pl' else '/o-nas/'
        ld={'@context':'https://schema.org','@type':'AboutPage','name':t,'url':BASE+path,'inLanguage':lang,'publisher':org()}
        write(path,shell(lang,f'{t} | Money Trackrr',d,path,alt,b,ld))
    # ---- mapa strony ----
    today=datetime.date.today().isoformat();last=max(a['date'] for a in A)
    def u(loc,lm,alts=None,freq='weekly',pr='0.7'):
        x=f'  <url><loc>{BASE}{loc}</loc><lastmod>{lm}</lastmod><changefreq>{freq}</changefreq><priority>{pr}</priority>'
        for hl,h in (alts or []):x+=f'<xhtml:link rel="alternate" hreflang="{hl}" href="{BASE}{h}"/>'
        return x+'</url>'
    rows=[u('/',today,None,'daily','1.0'),
          u('/aktualnosci/',last,[('pl','/aktualnosci/'),('en','/en/news/')],'daily','0.9'),u('/en/news/',last,[('pl','/aktualnosci/'),('en','/en/news/')],'daily','0.8'),
          u('/poradniki/',last,[('pl','/poradniki/'),('en','/en/guides/')],'weekly','0.8'),u('/en/guides/',last,[('pl','/poradniki/'),('en','/en/guides/')],'weekly','0.7'),
          u('/o-nas/',today,[('pl','/o-nas/'),('en','/en/about/')],'monthly','0.4'),u('/en/about/',today,[('pl','/o-nas/'),('en','/en/about/')],'monthly','0.3')]
    for pl,en,lm,ok in urls:
        if not ok:continue
        alts=[('pl',pl)]+([('en',en)] if en else [])
        rows.append(u(pl,lm,alts if en else None,'monthly','0.8'))
        if en:rows.append(u(en,lm,alts,'monthly','0.7'))
    open(os.path.join(SITE,'sitemap.xml'),'w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+'\n'.join(rows)+'\n</urlset>\n')
    # slugEn do danych aplikacji (link „stała strona artykułu”)
    s=open(P,encoding='utf-8').read();i=s.index('const DEFAULT_ARTICLES=')+len('const DEFAULT_ARTICLES=');old,end=json.JSONDecoder().raw_decode(s,i)
    m={a['id']:a['slugEn'] for a in A}
    for a in old:
        if a['id'] in m:a['slugEn']=m[a['id']]
    s=s[:i]+json.dumps(old,ensure_ascii=False).replace('</','<\\/')+s[end:];open(P,'w',encoding='utf-8').write(s)
    print(f'strony: {sum(1 for _ in urls)} PL + EN, w mapie: {sum(1 for x in urls if x[3])} artykułów (×2 języki), cienkie (noindex): {sum(1 for x in urls if not x[3])}')

if __name__=='__main__':build()
