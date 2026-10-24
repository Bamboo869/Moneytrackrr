"""Strony prawne (v0.23.3): polityka prywatności, kontakt, regulamin – PL i EN.
Wywoływane z pages.build(); regulamin brany z TERMS_HTML w aplikacji (EN przez słownik I18N_EN.exact)."""
import json,re,html as H
EMAIL='kontakt@moneytrackrr.app'
UPDATED_PL='25 października 2026';UPDATED_EN='25 October 2026'

PRIVACY={
'pl':('Polityka prywatności','Jakie dane przetwarza Money Trackrr, do czego służą pliki cookies i reklamy Google oraz jakie masz prawa.',f'''
<h1>Polityka prywatności</h1>
<p class="lead">Krótko: Twoje dane finansowe z trackera nie opuszczają Twojego urządzenia. Poniżej opisujemy wszystko, co dzieje się z danymi podczas korzystania z serwisu moneytrackrr.app.</p>
<p><em>Ostatnia aktualizacja: {UPDATED_PL}</em></p>
<h2>1. Kto odpowiada za dane</h2>
<p>Serwis Money Trackrr (moneytrackrr.app) prowadzi osoba prywatna – autor projektu. W sprawach prywatności napisz na <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>2. Dane wpisywane do trackera</h2>
<p>Operacje, kategorie, budżety, cele, konta i ustawienia zapisują się <strong>wyłącznie w pamięci Twojej przeglądarki</strong> (localStorage) na Twoim urządzeniu. Nie wysyłamy ich na żaden serwer, nie mamy do nich dostępu i nie przekazujemy ich nikomu – również reklamodawcom. Możesz je w każdej chwili usunąć, czyszcząc dane przeglądarki dla tej strony.</p>
<h2>3. Pliki cookies i pamięć przeglądarki</h2>
<p>Sam serwis nie ustawia plików cookies. Korzysta z pamięci przeglądarki tylko po to, żeby działać: zapamiętać Twoje dane w trackerze, motyw, język i inne ustawienia.</p>
<p>Pliki cookies mogą ustawiać zewnętrzni dostawcy reklam opisani w punkcie 4 – tylko na stronach z reklamami i w zakresie, na który się zgodzisz.</p>
<h2>4. Reklamy Google AdSense</h2>
<p>W Aktualnościach i Poradnikach (oprócz poradników o samej aplikacji) wyświetlamy reklamy Google AdSense. W samym trackerze reklam nie ma.</p>
<ul>
<li>Google, jako zewnętrzny dostawca, używa plików cookies do wyświetlania reklam, m.in. na podstawie Twoich wcześniejszych wizyt w tej i innych witrynach.</li>
<li>Pliki cookies reklamowe pozwalają Google i jego partnerom wyświetlać Ci reklamy na podstawie odwiedzin w naszym serwisie i w innych miejscach w internecie.</li>
<li>Przy pierwszej wizycie na stronie z reklamami zobaczysz okienko zgody. Możesz zgodzić się na reklamy spersonalizowane albo odmówić – wtedy Google może wyświetlać reklamy niespersonalizowane.</li>
<li>Reklamy spersonalizowane możesz wyłączyć w <a href="https://adssettings.google.com" rel="noopener">Ustawieniach reklam Google</a>, a reklamy innych firm – na stronie <a href="https://www.aboutads.info/choices/" rel="noopener">aboutads.info</a> lub <a href="https://www.youronlinechoices.com/pl/" rel="noopener">youronlinechoices.com</a>.</li>
<li>Więcej o tym, jak Google wykorzystuje dane: <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a>.</li>
</ul>
<h2>5. Statystyki odwiedzin</h2>
<p>Korzystamy z Cloudflare Web Analytics. To anonimowe statystyki (liczba wejść, kraj, rodzaj urządzenia i przeglądarki, czas ładowania, strona, z której nastąpiło wejście). Narzędzie nie używa plików cookies, nie tworzy profili użytkowników i nie widzi danych z trackera.</p>
<h2>6. Hosting i zasoby zewnętrzne</h2>
<ul>
<li><strong>Cloudflare</strong> (hosting) przetwarza standardowe dane techniczne, np. adres IP i logi serwera, żeby dostarczyć stronę i chronić ją przed atakami.</li>
<li>Strona pobiera publiczne dane i pliki z zewnętrznych serwerów: kursy walut z <strong>API Narodowego Banku Polskiego</strong>, zdjęcia z <strong>Unsplash</strong> i czcionkę z <strong>Google Fonts</strong>. Przy takim pobraniu Twoja przeglądarka łączy się z tymi serwerami i przekazuje im m.in. adres IP.</li>
</ul>
<h2>7. Podstawy prawne</h2>
<p>Dane techniczne (hosting, bezpieczeństwo, anonimowe statystyki) przetwarzamy na podstawie prawnie uzasadnionego interesu (art. 6 ust. 1 lit. f RODO), a pliki cookies reklam spersonalizowanych – na podstawie Twojej zgody (art. 6 ust. 1 lit. a RODO), którą możesz w każdej chwili wycofać.</p>
<h2>8. Twoje prawa</h2>
<p>Masz prawo do dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, sprzeciwu oraz wycofania zgody. Możesz też złożyć skargę do Prezesa Urzędu Ochrony Danych Osobowych (uodo.gov.pl). Ponieważ dane z trackera są tylko na Twoim urządzeniu, kontrolujesz je w pełni sam.</p>
<h2>9. Zmiany</h2>
<p>Jeśli zmieni się sposób przetwarzania danych (np. pojawi się nowe narzędzie), zaktualizujemy tę stronę i datę u góry.</p>
'''),
'en':('Privacy policy','What data Money Trackrr processes, how cookies and Google ads are used, and what your rights are.',f'''
<h1>Privacy policy</h1>
<p class="lead">In short: your financial data from the tracker never leaves your device. Below we describe everything that happens to data while you use moneytrackrr.app.</p>
<p><em>Last updated: {UPDATED_EN}</em></p>
<h2>1. Who is responsible</h2>
<p>Money Trackrr (moneytrackrr.app) is run by a private individual – the author of the project. For privacy matters, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>2. Data you enter in the tracker</h2>
<p>Transactions, categories, budgets, goals, accounts and settings are stored <strong>only in your browser's storage</strong> (localStorage) on your device. We never send them to a server, we have no access to them and we don't share them with anyone – including advertisers. You can delete them at any time by clearing your browser data for this site.</p>
<h2>3. Cookies and browser storage</h2>
<p>The site itself does not set cookies. It uses browser storage only to work: to remember your tracker data, theme, language and other settings.</p>
<p>Cookies may be set by the third-party ad providers described in section 4 – only on pages with ads and only to the extent you agree to.</p>
<h2>4. Google AdSense ads</h2>
<p>We show Google AdSense ads in News and Guides (except guides about the app itself). There are no ads in the tracker.</p>
<ul>
<li>Google, as a third-party vendor, uses cookies to serve ads, including based on your previous visits to this and other websites.</li>
<li>Advertising cookies enable Google and its partners to serve ads to you based on your visits to our site and other sites on the internet.</li>
<li>On your first visit to a page with ads you will see a consent message. You can agree to personalised ads or decline – in that case Google may show non-personalised ads.</li>
<li>You can opt out of personalised advertising in <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>, and out of other vendors' ads at <a href="https://www.aboutads.info/choices/" rel="noopener">aboutads.info</a> or <a href="https://www.youronlinechoices.com/" rel="noopener">youronlinechoices.com</a>.</li>
<li>More on how Google uses data: <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">policies.google.com/technologies/partner-sites</a>.</li>
</ul>
<h2>5. Visit statistics</h2>
<p>We use Cloudflare Web Analytics – anonymous statistics (number of visits, country, device and browser type, load time, referring page). It uses no cookies, builds no user profiles and cannot see tracker data.</p>
<h2>6. Hosting and external resources</h2>
<ul>
<li><strong>Cloudflare</strong> (hosting) processes standard technical data such as IP addresses and server logs to deliver the site and protect it from attacks.</li>
<li>The site loads public data and files from external servers: exchange rates from the <strong>National Bank of Poland API</strong>, photos from <strong>Unsplash</strong> and a font from <strong>Google Fonts</strong>. When that happens your browser connects to those servers and passes on, among other things, your IP address.</li>
</ul>
<h2>7. Legal bases</h2>
<p>We process technical data (hosting, security, anonymous statistics) on the basis of legitimate interest (Art. 6(1)(f) GDPR), and personalised advertising cookies on the basis of your consent (Art. 6(1)(a) GDPR), which you can withdraw at any time.</p>
<h2>8. Your rights</h2>
<p>You have the right to access, rectify and erase data, restrict processing, object and withdraw consent. You can also lodge a complaint with the Polish data protection authority (uodo.gov.pl) or the authority in your country. Since tracker data lives only on your device, you are fully in control of it.</p>
<h2>9. Changes</h2>
<p>If the way we process data changes (e.g. a new tool is added), we will update this page and the date at the top.</p>
''')}

CONTACT={
'pl':('Kontakt','Jak skontaktować się z redakcją Money Trackrr: błędy w artykułach, pytania o aplikację, prywatność i współpraca.',f'''
<h1>Kontakt</h1>
<p class="lead">Money Trackrr to mały, niezależny projekt – ale na każdą wiadomość staramy się odpowiedzieć.</p>
<h2>E-mail</h2>
<p><a href="mailto:{EMAIL}"><strong>{EMAIL}</strong></a> – odpowiadamy zwykle w ciągu kilku dni.</p>
<h2>W jakich sprawach pisać</h2>
<ul>
<li><strong>Błąd w artykule</strong> – podaj tytuł i fragment. Poprawimy tekst i zaktualizujemy datę.</li>
<li><strong>Problem z aplikacją</strong> – opisz, co się stało, na jakim urządzeniu i w jakiej przeglądarce. Nie wysyłaj nam swoich danych finansowych ani kopii zapasowej.</li>
<li><strong>Prywatność</strong> – pytania o dane, pliki cookies i reklamy (zobacz też <a href="/polityka-prywatnosci/">politykę prywatności</a>).</li>
<li><strong>Współpraca</strong> – propozycje tematów, materiały prasowe, partnerstwa.</li>
</ul>
<h2>Social media</h2>
<p>TikTok: <a href="https://www.tiktok.com/@moneytrackrr" rel="noopener">@moneytrackrr</a></p>
'''),
'en':('Contact','How to contact the Money Trackrr team: mistakes in articles, app questions, privacy and partnerships.',f'''
<h1>Contact</h1>
<p class="lead">Money Trackrr is a small, independent project – but we try to answer every message.</p>
<h2>Email</h2>
<p><a href="mailto:{EMAIL}"><strong>{EMAIL}</strong></a> – we usually reply within a few days.</p>
<h2>What to write about</h2>
<ul>
<li><strong>A mistake in an article</strong> – give us the title and the passage. We will fix it and update the date.</li>
<li><strong>A problem with the app</strong> – describe what happened, on which device and browser. Please don't send us your financial data or backup file.</li>
<li><strong>Privacy</strong> – questions about data, cookies and ads (see also our <a href="/en/privacy/">privacy policy</a>).</li>
<li><strong>Partnerships</strong> – topic ideas, press materials, collaborations.</li>
</ul>
<h2>Social media</h2>
<p>TikTok: <a href="https://www.tiktok.com/@moneytrackrr" rel="noopener">@moneytrackrr</a></p>
''')}

PATHS={'privacy':('/polityka-prywatnosci/','/en/privacy/'),'contact':('/kontakt/','/en/contact/'),'terms':('/regulamin/','/en/terms/')}

def terms(app_html):
    i=app_html.index('const TERMS_HTML=')+len('const TERMS_HTML=');pl,_=json.JSONDecoder().raw_decode(app_html,i)
    j=app_html.index('const I18N_EN={exact:')+len('const I18N_EN={exact:');ex,_=json.JSONDecoder().raw_decode(app_html,j)
    def tr(m):
        t=m.group(0);core=t.strip()
        if not core:return t
        out=ex.get(core) or ex.get(H.unescape(core))
        return t.replace(core,out) if out else t
    pl=re.sub(r'<h2>(.*?)</h2>',r'<h1>\1</h1>',pl,count=1)
    en=re.sub(r'(?<=>)[^<]+(?=<)',tr,pl)
    desc_pl='Regulamin serwisu Money Trackrr: czym jest narzędzie, odpowiedzialność, dane, prywatność i zasady korzystania.'
    desc_en='Money Trackrr terms of use: what the tool is, liability, data, privacy and rules of use.'
    return {'pl':('Regulamin',desc_pl,pl),'en':('Terms of use',desc_en,en)}

def build(shell,write,org,BASE,card_cta,L,P):
    app=open(P,encoding='utf-8').read()
    T=terms(app)
    for key,data in (('privacy',PRIVACY),('contact',CONTACT),('terms',T)):
        for lang,(t,d,b) in data.items():
            pl,en=PATHS[key];path=pl if lang=='pl' else en;alt=en if lang=='pl' else pl
            ld={'@context':'https://schema.org','@type':'ContactPage' if key=='contact' else 'WebPage','name':t,'url':BASE+path,'inLanguage':lang,'publisher':org()}
            body='<div class="about">'+b+card_cta(L[lang],'about')+'</div>'
            write(path,shell(lang,f'{t} | Money Trackrr',d,path,alt,body,ld,tab=''))
