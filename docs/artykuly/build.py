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
 ('n12','news','oplata-2-euro-paczki-spoza-ue-listopad-2026','Podatki','2026-10-27','1566576721346-d4a3b4eaeb55','Osoba podająca kartonową paczkę',True),
 ('n11','news','wszystkich-swietych-2026-ile-wydamy','Budżet','2026-10-26','1775128634801-9bb665957274','Znicze świecące nocą na cmentarzu',False),
 ('n10','news','slaby-zloty-kurs-euro-dolara-pazdziernik-2026','Rynki','2026-10-25','1580048915913-4f8f5cb481c4','Ręka trzymająca banknoty euro i dolarów',False),
 ('n9','news','nowe-progi-podatkowe-pit-2027','Podatki','2026-10-23','1554224155-6726b3ff858f','Osoba z dokumentami, długopisem i kalkulatorem',False),
 ('n8','news','wynagrodzenia-wrzesien-2026-realne-place','Praca','2026-10-21','1767423646401-cd5b90ba5e11','Plik polskich banknotów w portfelu',False),
 ('n7','news','ceny-paliw-maksymalne-20-pazdziernika-2026','Paliwa','2026-10-20','1646836724019-0e0f16757c93','Tankowanie samochodu na stacji paliw',False),
 ('n5','news','rosja-polska-grozby-finanse','Bezpieczeństwo','2026-10-18','1740759009286-606a45347231','Polska flaga na wietrze',False),
 ('n6','news','ai-banka-wstrzas-gieldy-pazdziernik-2026','Rynki','2026-10-17','1562408590-e32931084e23','Niebieska płytka drukowana',False),
 ('n1','news','ropa-ormuz-portfel','Paliwa','2026-10-15','1518527989017-5baca7a58d3c','Tankowiec na morzu widziany z góry',False),
 ('n2','news','inflacja-wrzesien-2026-stopy-nbp','Inflacja','2026-10-14','1601598851547-4302969d0614','Wózek sklepowy w alejce supermarketu',False),
 ('n3','news','fed-ebc-podwyzki-stop-2026','Rynki','2026-10-12','1701434001217-16428abc6309','Rzeźba ze znakiem euro przed siedzibą banku we Frankfurcie',False),
 ('n4','news','placa-minimalna-2027','Praca','2026-10-10','1504307651254-35680f356dfd','Dwóch pracowników przy pracy',False),
 ('g1','guide','obligacje-skarbowe-jak-wybrac','Oszczędzanie','2026-10-16','1633158829875-e5316a358c6f','Słoik z monetami i małą roślinką',False),
 ('g2','guide','jak-wyjsc-z-dlugow','Długi','2026-10-16','1563013544-824ae1b704d3','Osoba przy laptopie trzymająca kartę płatniczą',False),
 ('t1','guide','pierwsze-kroki-money-trackrr','Aplikacja','2026-10-16','1709880945165-d2208c6ad2ec','Kalkulator obok laptopa',False),
 ('t5','guide','jak-zainstalowac-aplikacje','Aplikacja','2026-10-16','1554224155-8d04cb21cd6c','Smartfon z otwartą aplikacją',False),
 ('t2','guide','budzety-cele-stale-oplaty','Aplikacja','2026-10-16','1578091436046-ecd3f4fe6992','Słoik z monetami z napisem „house fund”',False),
 ('t3','guide','pieniazek-porady-bez-ai','Aplikacja','2026-10-16','1619718082268-5a1b74988497','Złote i srebrne monety',False),
 ('t4','guide','kopia-zapasowa-telefon','Aplikacja','2026-10-16','1713947506242-8fcae733d158','Kobieta przy stole patrząca w telefon',False),
# v0.23.3: stare, zbyt krótkie poradniki napisane od nowa (te same adresy)
 ('o1','guide','inflacja-po-ludzku','Inflacja','2026-10-25','1654370849443-0aa7e3d2920f','Etykieta z ceną',False),
 ('o2','guide','procent-skladany','Oszczędzanie','2026-10-25','1583902340377-052b7159b97b','Monety w szklanym słoiku',False),
 ('o3','guide','zasada-50-30-20','Budżet','2026-10-25','1648201637025-1c77b9be3013','Kalkulator i długopis na kartce',False),
 ('o4','guide','jak-zalozyc-konto-oszczednosciowe','Oszczędzanie','2026-10-25','1589758438368-0ad531db3366','Karta płatnicza',False),
 ('o5','guide','automatyczne-odkladanie','Oszczędzanie','2026-10-25','1633158829556-6ea20ad39b4f','Słoik z napisem savings',False),
 ('o6','guide','poduszka-finansowa','Bezpieczeństwo','2026-10-25','1634474588707-de99f09285c0','Słoik z oszczędnościami w dłoniach',False),
 ('o7','guide','budzet-miesieczny','Budżet','2026-10-25','1642043175009-5997b3a078d8','Kalkulator na stosie dokumentów',False),
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
WAR=re.compile(r'(?i)wojn|rosj|ukrai|putin|zbroj|militar|NATO|inwazj|ostrza|rakiet|dron')
def no_ads(*txt):
  # zasady Google: nie zarabiamy na treściach o wojnie (m.in. w Ukrainie) – takie artykuły są bez reklam
  return len(WAR.findall(' '.join(txt)))>=5
for k,kind,slug,tag,date,cov,alt,feat in NEW:
  t,su,b=md(k+'_pl.md');te,sue,be=md(k+'_en.md')
  out.append({'id':'s_'+slug,'kind':kind,'slug':slug,'tag':tag,'date':date,'status':'published','title':t,'summary':su,'body':b,'author':'Money Trackrr','titleEn':te,'summaryEn':sue,'bodyEn':be,'featured':feat,'cover':U(cov),'coverAlt':alt,'gallery':[]})
  if no_ads(t,b):out[-1]['noAds']=True
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

# v0.22: statyczne strony artykułów + mapa strony
import importlib.util as _u
_s=_u.spec_from_file_location('pages',A+'pages.py');_m=_u.module_from_spec(_s);_s.loader.exec_module(_m);_m.build()
