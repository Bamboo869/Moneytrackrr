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

L={'pl':dict(news='Aktualności',guides='Poradniki',home='Home',tracker='Money Tracker',about='O nas',read='min czytania',
             by='Redakcja Money Trackrr',chapters='Spis rozdziałów',intro='Wstęp',pct='przeczytane',all_news='Wszystkie aktualności',all_guides='Wszystkie poradniki',
             sug_news='Czytaj też',sug_guide='Inne poradniki',ad='Reklama',copy='🔗 Kopiuj link',share='↗ Udostępnij',copied='Skopiowano link ✓',
             disc='Materiał ma charakter wyłącznie informacyjny i edukacyjny. Nie stanowi porady finansowej, inwestycyjnej, podatkowej ani prawnej.',
             cta_t='💰 Prowadź budżet za darmo',cta_p='Kalendarz wydatków, budżety i cele oszczędnościowe. Dane zostają w Twojej przeglądarce.',cta_b='Otwórz Money Trackrr',
             sub='Twoje finanse, rynek i budżet w jednym miejscu',other='English',terms='Regulamin',all='Wszystkie artykuły',
             news_h='Aktualności finansowe',news_i='Najważniejsze wiadomości ze świata i z Polski – wyjaśnione prosto: co się stało i co to znaczy dla Twojego portfela. Zawsze z podanymi źródłami.',
             guides_h='Poradniki o pieniądzach',guides_i='Jak oszczędzać, budżetować, wyjść z długów i korzystać z Money Trackrr – krok po kroku, bez żargonu.'),
   'en':dict(news='News',guides='Guides',home='Home',tracker='Money Tracker',about='About',read='min read',
             by='Money Trackrr editorial team',chapters='Chapters',intro='Introduction',pct='read',all_news='All news',all_guides='All guides',
             sug_news='Read also',sug_guide='More guides',ad='Advertisement',copy='🔗 Copy link',share='↗ Share',copied='Link copied ✓',
             disc='This material is for information and education only. It is not financial, investment, tax or legal advice.',
             cta_t='💰 Budget for free',cta_p='Expense calendar, budgets and savings goals. Your data stays in your browser.',cta_b='Open Money Trackrr',
             sub='Your finances, markets and budget in one place',other='Polski',terms='Terms',all='All articles',
             news_h='Money news',news_i='The most important news from Poland and the world – explained simply: what happened and what it means for your wallet. Always with sources.',
             guides_h='Money guides',guides_i='How to save, budget, get out of debt and use Money Trackrr – step by step, no jargon.')}

def fmt_date(d,lang):
    y,m,dd=map(int,d.split('-'))
    return f'{dd} {MON_PL[m-1]} {y}' if lang=='pl' else f'{dd} {MON_EN[m-1]} {y}'
def words(t):return len(re.findall(r'\w+',t or ''))
VER=['']
# motyw z ustawień aplikacji (ten sam localStorage), ustawiany zanim strona się narysuje – bez mignięcia
THEME_JS=("<script>(function(){var d=document.documentElement,A={dark:'#4d90fe',light:'#2563eb',cream:'#b9722f',midnight:'#5b9bff',halloween:'#ff7a1a'};"
          "try{var s=JSON.parse(localStorage.getItem('mt_settings_v1')||'{}'),t=A[s.theme]?s.theme:'dark';d.dataset.theme=t;var a=s.accent||A[t];"
          "d.style.setProperty('--blue',a);d.style.setProperty('--blue-bg',a+'1f');if(s.spookyAnim===false)d.classList.add('sp-still');}catch(e){d.dataset.theme='dark';}})();</script>")

def shell(lang,title,desc,canon,alt,body,ld,og_img=None,og_type='website',extra_head='',robots='index,follow,max-image-preview:large',tab='news',reader=False):
    l=L[lang];other='en' if lang=='pl' else 'pl'
    hl=''
    if alt:
        xd=canon if lang=='pl' else alt
        hl=(f'<link rel="alternate" hreflang="{lang}" href="{BASE}{canon}"><link rel="alternate" hreflang="{other}" href="{BASE}{alt}">'
            f'<link rel="alternate" hreflang="x-default" href="{BASE}{xd}">')
    og=(f'<meta property="og:image" content="{esc(og_img)}"><meta name="twitter:card" content="summary_large_image">' if og_img
        else '<meta name="twitter:card" content="summary">')
    news_u='/aktualnosci/' if lang=='pl' else '/en/news/';guides_u='/poradniki/' if lang=='pl' else '/en/guides/';about_u='/o-nas/' if lang=='pl' else '/en/about/'
    def tb(v,ico,lab,href):
        act='active' if tab==v else ''
        return f'<button type="button" data-v="{v}" class="{act}" onclick="location.href=\'{href}\'"><span class="ti" aria-hidden="true">{ico}</span><span class="tl">{lab}</span></button>'
    tabs=tb('home','🏠',l['home'],'/#home')+tb('news','📰',l['news'],news_u)+tb('guides','📚',l['guides'],guides_u)+tb('tracker','💰',l['tracker'],'/#tracker')
    ib='text-decoration:none;display:inline-flex;align-items:center;justify-content:center'
    lang_btn=f'<a class="ibtn" href="{alt}" hreflang="{other}" title="{l["other"]}" style="{ib};font-weight:800;font-size:13px">{other.upper()}</a>' if alt else ''
    ldj=json.dumps(ld,ensure_ascii=False).replace('</','<\\/')
    loc='pl_PL' if lang=='pl' else 'en_US'
    vid='view-reader' if reader else 'view-static'
    return (f'<!doctype html>\n<html lang="{lang}" data-theme="dark">\n<head>\n<meta charset="utf-8">\n'
     f'<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{esc(title)}</title>\n'
     f'<meta name="description" content="{esc(desc)}">\n<meta name="robots" content="{robots}">\n<link rel="canonical" href="{BASE}{canon}">{hl}\n'
     f'<meta property="og:site_name" content="Money Trackrr"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{esc(title)}">'
     f'<meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE}{canon}"><meta property="og:locale" content="{loc}">{og}\n'
     f'<meta name="theme-color" content="#0a0c0f">\n<meta name="google-adsense-account" content="{AD_CLIENT}">\n'
     f'<link rel="icon" href="/favicon.ico"><link rel="apple-touch-icon" href="/icons/apple-touch-icon.png"><link rel="manifest" href="/manifest.webmanifest">\n'
     f'{THEME_JS}\n<link rel="stylesheet" href="/assets/reader.css?v={VER[0]}">\n<script defer src="/assets/reader.js?v={VER[0]}"></script>\n'
     f'{extra_head}<script type="application/ld+json">{ldj}</script>\n</head>\n'
     f'<body data-lang="{lang}" data-copied="{esc(l["copied"])}">\n<div class="page">\n'
     f'<div class="hero"><div class="hero-in">\n  <div class="hero-top">\n'
     f'    <div><h1><a href="/">Money <span>Trackrr</span></a></h1><div class="tag">{l["sub"]}</div></div>\n'
     f'    <div class="hero-right">{lang_btn}<a class="ibtn" href="/#tracker" title="{l["tracker"]}" style="{ib}">💰</a></div>\n'
     f'  </div>\n  <div class="tabs" id="tabs">{tabs}</div>\n</div></div>\n'
     f'<section class="view active" id="{vid}">\n{body}\n</section>\n'
     f'<footer class="site"><div class="foot-in"><span>© Money Trackrr</span><span class="foot-links"><a href="{news_u}">{l["all"]}</a>'
     f'<a href="{about_u}">{l["about"]}</a><a href="/#terms">{l["terms"]}</a>'
     f'<a href="https://www.tiktok.com/@moneytrackrr" target="_blank" rel="noopener" class="foot-tt">TikTok @moneytrackrr</a></span>'
     f'<span class="coffee-wrap"><a class="coffee" href="https://buymeacoffee.com/moneytrackrr" target="_blank" rel="noopener">☕ Buy me a coffee</a></span></div></footer>\n'
     f'</div>\n</body>\n</html>\n')

def write(path,txt):
    full=os.path.join(SITE,path.strip('/'),'index.html');os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w',encoding='utf-8').write(txt)

READER_JS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'reader_src.js'),encoding='utf-8').read()

def spooky_code():
    s=open(P,encoding='utf-8').read()
    i=s.index('  const BAT=`');j=s.index('d.innerHTML=h;document.body.insertBefore(d,document.body.firstChild);',i)
    j=s.index('}',j)+1
    return s[i:j]

def card_cta(l,ref):
    return (f'<div class="cta-card"><b>{l["cta_t"]}</b><p>{l["cta_p"]}</p>'
            f'<a class="cbtn" href="/?ref={ref}#tracker"><button type="button" tabindex="-1">{l["cta_b"]}</button></a></div>')

def article_html(a,lang,A_by_kind):
    l=L[lang];en=lang=='en'
    title=a.get('titleEn') if en else a['title'];summ=(a.get('summaryEn') if en else a.get('summary')) or '';body=(a.get('bodyEn') if en else a.get('body')) or ''
    html_body,chs=md(body)
    tag=TAG_EN.get(a.get('tag'),a.get('tag')) if en else a.get('tag')
    guide=a.get('kind')=='guide'
    k_path=('/en/guides/' if en else '/poradniki/') if guide else ('/en/news/' if en else '/aktualnosci/')
    k_name=l['guides'] if guide else l['news']
    cover=img(a.get('cover'),1200);mins=max(1,round(words(body)/200))
    ads=a.get('tag')!='Aplikacja'
    ad=(f'<div class="gad" data-gad><span class="gad-lab">{l["ad"]}</span><ins class="adsbygoogle" style="display:block" data-ad-client="{AD_CLIENT}" '
        f'data-ad-slot="{AD_SLOT}" data-ad-format="auto" data-full-width-responsive="true"></ins></div>') if ads else ''
    allch=[('ch-top',l['intro'])]+[(cid,re.sub(r'[*]','',t)) for cid,t in chs]
    lis=''.join(f'<li data-i="{i}" data-c="{cid}"><button type="button" data-i="{i}"><span class="dot"></span><span class="lbl">{esc(t)}</span></button></li>' for i,(cid,t) in enumerate(allch))
    toc=(f'<nav class="toc" id="rdToc"><div class="toc-h">{l["chapters"]}</div><div class="toc-line"><i class="toc-fill" id="tocFill"></i></div>'
         f'<ol>{lis}</ol><div class="toc-meta"><b id="tocPct">0%</b> {l["pct"]}</div></nav>')
    pool=[r for r in A_by_kind('guide' if guide else 'news') if r is not a and (not en or r.get('bodyEn'))]
    pool=sorted(pool,key=lambda r:((r.get('tag')==a.get('tag')),r.get('date','')),reverse=True)[:4]
    def sug1(r):
        href=('/en/a/'+r['slugEn']) if en else ('/a/'+r['slug'])
        t=r.get('titleEn') if en else r['title'];m=max(1,round(words(r.get('bodyEn') if en else r.get('body'))/200))
        return f'<a class="sug" href="{href}/"><img loading="lazy" decoding="async" src="{esc(img(r.get("cover"),200))}" alt=""><div><b>{esc(t)}</b><small>{m} {l["read"]}</small></div></a>'
    sug=''.join(sug1(r) for r in pool)
    right=(f'<div><div class="sug-h">{l["sug_guide"] if guide else l["sug_news"]}</div>{sug}</div>' if sug else '')+card_cta(l,'article')
    alt_txt=esc(title if en else (a.get('coverAlt') or title))
    hero=f'<figure class="rd-hero"><img fetchpriority="high" decoding="async" src="{esc(cover)}"{srcset(a.get("cover"))} alt="{alt_txt}"></figure>' if cover else ''
    lead=f'<p class="rd-lead">{esc(summ)}</p>' if summ else ''
    back=l['all_guides'] if guide else l['all_news']
    out=('<div id="rdProg"></div>\n'
         f'<div class="rd-top"><a class="btn-small" id="rdBack" href="{k_path}">← <span id="rdBackLbl">{back}</span></a></div>\n'
         f'<div class="rd-layout{" guide" if guide else ""}" id="rdLayout">\n'
         f'<aside class="rd-left"><div class="rd-sticky">{toc}</div></aside>\n'
         '<article class="rd-main" id="rdMain">\n'
         f'<div class="rd-crumbs"><a href="/">Money Trackrr</a> › <a href="{k_path}">{k_name}</a></div>\n'
         f'<span class="tagpill">{esc(tag)}</span><h1>{esc(title)}</h1>\n'
         f'<div class="rd-meta"><span><time datetime="{a["date"]}">{fmt_date(a["date"],lang)}</time></span><span>·</span><span>{mins} {l["read"]}</span><span>·</span><span>{l["by"]}</span></div>\n'
         f'{lead}\n{hero}\n<div class="rd-body"><div id="ch-top"></div>{html_body}</div>\n'
         f'<div class="rd-share"><button type="button" class="btn-small" id="rdCopy">{l["copy"]}</button><button type="button" class="btn-small" id="rdShare">{l["share"]}</button></div>\n'
         f'<div class="rd-disc">{l["disc"]}</div>\n{ad}\n</article>\n'
         f'<aside class="rd-right"><div class="rd-sticky" id="rdRight">{right}</div></aside>\n</div>')
    return out,title,summ,body,cover,tag,guide,k_path,k_name,ads

def org():
    return {'@type':'Organization','name':'Money Trackrr','url':BASE+'/','logo':{'@type':'ImageObject','url':BASE+'/icons/icon-512.png'}}

def build():
    import hashlib
    A=load()
    for a in A:
        a['slugEn']=a.get('slugEn') or slugify(a.get('titleEn') or a['title'])
    js=READER_JS.replace('__SPOOKY__',spooky_code())
    os.makedirs(os.path.join(SITE,'assets'),exist_ok=True)
    open(os.path.join(SITE,'assets','reader.js'),'w',encoding='utf-8').write(js)
    css=open(os.path.join(SITE,'assets','reader.css'),encoding='utf-8').read()
    VER[0]=hashlib.md5((css+js).encode()).hexdigest()[:8]
    by_kind=lambda k:sorted([a for a in A if (a.get('kind')=='guide')==(k=='guide')],key=lambda a:a.get('date',''),reverse=True)
    for d in ['a','en/a']:shutil.rmtree(os.path.join(SITE,d),ignore_errors=True)
    urls=[]
    for a in A:
        for lang in ('pl','en'):
            en=lang=='en';l=L[lang]
            if en and not a.get('bodyEn'):continue
            path=f"/en/a/{a['slugEn']}/" if en else f"/a/{a['slug']}/"
            alt=(f"/a/{a['slug']}/" if en else (f"/en/a/{a['slugEn']}/" if a.get('bodyEn') else None))
            body_html,title,summ,body,cover,tag,guide,k_path,k_name,ads=article_html(a,lang,by_kind)
            thin=len(body)<THIN
            ld=[{'@context':'https://schema.org','@type':'Article' if guide else 'NewsArticle','headline':title[:110],'description':summ,
                 'image':[cover] if cover else [],'datePublished':a['date']+'T08:00:00+02:00','dateModified':a['date']+'T08:00:00+02:00',
                 'inLanguage':lang,'author':{'@type':'Organization','name':l['by'],'url':BASE+('/en/about/' if en else '/o-nas/')},
                 'publisher':org(),'mainEntityOfPage':BASE+path,'articleSection':tag},
                {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
                 {'@type':'ListItem','position':1,'name':'Money Trackrr','item':BASE+'/'},
                 {'@type':'ListItem','position':2,'name':k_name,'item':BASE+k_path},
                 {'@type':'ListItem','position':3,'name':title,'item':BASE+path}]}]
            head=f'<meta property="article:published_time" content="{a["date"]}T08:00:00+02:00">'
            if ads: head+=f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={AD_CLIENT}" crossorigin="anonymous"></script>'
            desc=summ if len(summ)<=160 else summ[:157].rsplit(' ',1)[0]+'…'
            write(path,shell(lang,f'{title} | Money Trackrr',desc,path,alt,body_html,ld,cover or None,'article',head,
                             'noindex,follow' if thin else 'index,follow,max-image-preview:large',tab='guides' if guide else 'news',reader=True))
            if not en: urls.append((path,alt,a['date'],not thin))
    # ---- spisy ----
    for lang in ('pl','en'):
        l=L[lang];en=lang=='en'
        for kind in ('news','guide'):
            items=[a for a in by_kind(kind) if not en or a.get('bodyEn')]
            guide=kind=='guide'
            path=('/en/guides/' if en else '/poradniki/') if guide else ('/en/news/' if en else '/aktualnosci/')
            alt=('/poradniki/' if en else '/en/guides/') if guide else ('/aktualnosci/' if en else '/en/news/')
            h=l['guides_h'] if guide else l['news_h'];intro=l['guides_i'] if guide else l['news_i']
            def card(a):
                href=('/en/a/'+a['slugEn']) if en else ('/a/'+a['slug'])
                t=a.get('titleEn') if en else a['title'];sm=((a.get('summaryEn') if en else a.get('summary')) or '')[:150]
                tg=TAG_EN.get(a.get('tag'),a.get('tag')) if en else a.get('tag')
                return (f'<a class="ls-card" href="{href}/"><img loading="lazy" decoding="async" src="{esc(img(a.get("cover"),640))}" alt="{esc(t)}">'
                        f'<div><small>{TAG_EMO.get(a.get("tag"),"📰")} {esc(tg)} · {fmt_date(a["date"],lang)}</small><b>{esc(t)}</b><p>{esc(sm)}…</p></div></a>')
            body=f'<div class="ls-wrap"><h1>{h}</h1><p class="ls-lead">{intro}</p><div class="ls-list">{"".join(card(a) for a in items)}</div></div>'
            ld={'@context':'https://schema.org','@type':'CollectionPage','name':h,'description':intro,'inLanguage':lang,'url':BASE+path,'publisher':org(),
                'mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+(f'/en/a/{a["slugEn"]}/' if en else f'/a/{a["slug"]}/')} for i,a in enumerate(items)]}}
            write(path,shell(lang,f'{h} | Money Trackrr',intro[:158],path,alt,body,ld,None,'website','',tab='guides' if guide else 'news'))
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
{card_cta(L['pl'],'about')}'''),
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
{card_cta(L['en'],'about')}''')}
    for lang,(t,d,b) in ABOUT.items():
        path='/o-nas/' if lang=='pl' else '/en/about/';alt='/en/about/' if lang=='pl' else '/o-nas/'
        ld={'@context':'https://schema.org','@type':'AboutPage','name':t,'url':BASE+path,'inLanguage':lang,'publisher':org()}
        write(path,shell(lang,f'{t} | Money Trackrr',d,path,alt,'<div class="about">'+b+'</div>',ld,tab=''))
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
