import json,re,sys
A='docs/artykuly/'
P='site/index.html'
U=lambda i,w=1200:f'https://images.unsplash.com/photo-{i}?auto=format&fit=crop&w={w}&q=80'
def md(fn):
  t=open(A+fn).read().strip('\n')
  head,body=t.split('\n---\n',1)
  title,summary=head.split('\n',1)
  return title.strip(),summary.strip(),body.strip()
NEW=[ # key, kind, slug, tag, date, cover, alt, featured
 ('n1','news','ropa-ormuz-portfel','Paliwa','2026-10-15','1518527989017-5baca7a58d3c','Tankowiec na morzu widziany z góry',True),
 ('n2','news','inflacja-wrzesien-2026-stopy-nbp','Inflacja','2026-10-14','1601598851547-4302969d0614','Wózek sklepowy w alejce supermarketu',False),
 ('n3','news','fed-ebc-podwyzki-stop-2026','Rynki','2026-10-12','1701434001217-16428abc6309','Rzeźba ze znakiem euro przed siedzibą banku we Frankfurcie',False),
 ('n4','news','placa-minimalna-2027','Praca','2026-10-10','1504307651254-35680f356dfd','Dwóch pracowników przy pracy',False),
 ('g1','guide','obligacje-skarbowe-jak-wybrac','Oszczędzanie','2026-10-16','1633158829875-e5316a358c6f','Słoik z monetami i małą roślinką',False),
 ('g2','guide','jak-wyjsc-z-dlugow','Długi','2026-10-16','1563013544-824ae1b704d3','Osoba przy laptopie trzymająca kartę płatniczą',False),
 ('t1','guide','pierwsze-kroki-money-trackrr','Aplikacja','2026-10-16','1709880945165-d2208c6ad2ec','Kalkulator obok laptopa',False),
 ('t2','guide','budzety-cele-stale-oplaty','Aplikacja','2026-10-16','1578091436046-ecd3f4fe6992','Słoik z monetami z napisem „house fund”',False),
 ('t3','guide','pieniazek-porady-bez-ai','Aplikacja','2026-10-16','1619718082268-5a1b74988497','Złote i srebrne monety',False),
 ('t4','guide','kopia-zapasowa-telefon','Aplikacja','2026-10-16','1713947506242-8fcae733d158','Kobieta przy stole patrząca w telefon',False),
]
OLD_COVERS={'s_inflacja-po-ludzku':('1654370849443-0aa7e3d2920f','Etykieta z ceną'),
 's_procent-skladany':('1583902340377-052b7159b97b','Monety w szklanym słoiku'),
 's_zasada-50-30-20':('1648201637025-1c77b9be3013','Kalkulator i długopis na kartce'),
 's_jak-zalozyc-konto-oszczednosciowe':('1589758438368-0ad531db3366','Karta płatnicza'),
 's_automatyczne-odkladanie':('1633158829556-6ea20ad39b4f','Słoik z napisem savings'),
 's_poduszka-finansowa':('1634474588707-de99f09285c0','Słoik z oszczędnościami w dłoniach'),
 's_budzet-miesieczny':('1642043175009-5997b3a078d8','Kalkulator na stosie dokumentów')}
s=open(P).read()
i=s.index('const DEFAULT_ARTICLES=')+len('const DEFAULT_ARTICLES=')
old,end=json.JSONDecoder().raw_decode(s,i)
assert s[end]==';'
out=[]
for k,kind,slug,tag,date,cov,alt,feat in NEW:
  t,su,b=md(k+'_pl.md');te,sue,be=md(k+'_en.md')
  out.append({'id':'s_'+slug,'kind':kind,'slug':slug,'tag':tag,'date':date,'status':'published','title':t,'summary':su,'body':b,'author':'Money Trackrr','titleEn':te,'summaryEn':sue,'bodyEn':be,'featured':feat,'cover':U(cov),'coverAlt':alt,'gallery':[]})
for a in old:
  a=dict(a)
  if a['id'] in [x['id'] for x in out]:continue
  a['kind']='guide';a['featured']=False
  if a['id'] in OLD_COVERS and not a.get('cover'):
    c,al=OLD_COVERS[a['id']];a['cover']=U(c);a['coverAlt']=al
  out.append(a)
js=json.dumps(out,ensure_ascii=False).replace('</','<\\/')
s=s[:i]+js+s[end:]
open(P,'w').write(s)
print(len(out),[ (a['kind'],a['slug']) for a in out])
