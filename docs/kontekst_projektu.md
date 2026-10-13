# Money Tracker – kontekst projektu (wiedza dla Projects)

## 1. Czym jest projekt
Money Tracker to jednoplikowa aplikacja HTML/CSS/JS do osobistych finansów. Działa w całości w przeglądarce (localStorage), bez backendu. Hostowana na Netlify (*.netlify.app). Używa jej użytkownik i jego partner. Język użytkownika: polski (strefa Europe/Warsaw). Aplikacja ma też wersję EN.

Aktualna wersja: **0.16.1** (v0.16.1: na dotyku układarka okien przeciąga tylko za uchwyt ⠿ (`pointerType!==mouse`), kafelki w jednej kolumnie; lista operacji `.tx` zwarta z odstępami; propozycja samouczka tylko po pierwszej konfiguracji; `.tour` z-index 5500. v0.16: wersja mobilna – blok CSS `@media(max-width:700px)` na końcu `<style>` (dolny pasek z zakładek `.tabs`, nagłówek nieprzyklejony, kalendarz `minmax(0,1fr)`, karty 2 w rzędzie, okna jako arkusz od dołu, inputy 16px dla iOS) + skrypt: ikony zakładek `.ti/.tl`, `html[data-view]`, pływający przycisk `.m-fab` (otwiera `openDayModal(dziś)`), „pokaż wszystkie aktualizacje” na Home. Flaga powrotu po samouczku w localStorage `mt_tour_after` (sessionStorage bywał gubiony przy reload). v0.15.1: v0.15.1: część samouczka „Pokaż ustawienia” – `SET_STEPS()` z polem `st` (none/local/global) otwierającym odpowiednie okno ustawień, `el()` dla celów bez id; wzmianka o liniach w kalendarzu i personalizacji. v0.15: samouczek z Pieniążkiem – ostatni blok `<script>`, `startTour()`, kroki w `STEPS()` (pomijane, gdy okno ukryte), dane przykładowe `demoData()`; prawdziwe dane kopiowane do `mt_tour_backup` i przywracane skryptem w `<head>` przy następnym wczytaniu (koniec samouczka = reload); propozycja po kreatorze (owinięty `finishWiz`), przycisk w ustawieniach trackera `#btnTour`; `window.__coinSvg` z modułu Pieniążka. v0.14: v0.14: zgoda na regulamin jako przycisk `.terms-btn` (ukryty checkbox `#wzTerms`), gotowe układy `PRESETS` (simple/planner/full) + `applyPreset()` w kroku 2 kreatora, domyślnie Planista; Pieniążek ukryty podczas kreatora. v0.13.1: v0.13.1: ikona ustawień trackera po lewej stronie nagłówka, bez rezerwowania miejsca po prawej. v0.13: Pieniążek na Home, w Aktualnościach, Poradnikach i artykule – tylko zaprasza do trackera (`TEASE`, 3 teksty na sekcję, przycisk `data-coin-go` przenosi do trackera i otwiera porady); prawdziwe porady wyłącznie w trackerze; wpisy u12–u12.3 scalone w jeden wpis u13 na Home. v0.12.3: v0.12.3: porady wyłącznie kontekstowe – reguły a–h w `candidates()` (duża wpłata na cel, cel bez planu, duży zakup, mało do wypłaty, wpływ pensji, brak celu, udział rachunków, podsumowanie miesiąca); kategorie oszczędnościowe (`goal_savings`, `invest`) i rachunki wyłączone z prognoz tempa; przycisk `#btnLocalSettings` jako ikona ⚙️, stałe miejsce na monetę w nagłówku trackera. v0.12.2: moneta `.coin-dock` po prawej od całej strony (≥1420px w marginesie, `right:-64px`), porada w chmurce `.coin-bubble` w `.coin-bubble-slot` nakładanej na treść; śpiący Pieniążek (brak porad albo ukryty na dziś) z możliwością obudzenia; licznik dni z rzędu `S.coin.streak`; zamykanie kliknięciem obok i Esc; stan na `<html>` (klasy coin-on, coin-hint-on); odręczne dopiski czcionką Caveat (Google Fonts) przy monecie i przy „Buy me a coffee”. v0.12: „Pieniążek” – codzienna porada; ostatni blok `<script>`; sloty `.coin-slot` na Home i w trackerze; reguły w `candidates()`, stan w `S.coin`; teksty generowane funkcją `L(pl,en)` zamiast słownika; `render` owinięty, żeby odświeżać poradę). Wcześniej v0.11 (v0.11: PWA – `site/manifest.webmanifest`, `site/sw.js`, ikony w `site/icons/`, przycisk 📲 `#btnInstall`, klasa `body.is-offline` i `.offline-note` w Aktualnościach/Poradnikach/artykule; v0.10.1: przyklejony spis kropek – `stickyH()` uwzględnia `.hero`). Wcześniej v0.10 (v0.10: słownik EN dla czytnika artykułów, list i panelu autora/publikacji – dopisany blok `Object.assign(I18N_EN.exact,…)` + `I18N_EN.rx.push(…)` zaraz po definicji słownika; administrator w regulaminie: „Tommy”, e-mail nadal do uzupełnienia). Wcześniej v0.9: (plik `claude/money_tracker_v9.html` w projekcie, ok. 5050 linii, 8 bloków `<script>`). v0.9 = poprawka porównania z poprzednim okresem w oknach podsumowania (`deltaInfo`): przy |zmianie| ≥ 300% pokazuje krotność i różnicę kwotową (▲ ×151 (+4500,00 zł)), przy zmianie znaku samą różnicę kwotową.

**Repozytorium:** github.com/Bamboo869/Moneytrackrr (prywatne, gałąź `main`). Źródło prawdy dla kodu: `site/index.html` w repo (Netlify publikuje folder `site/`; `docs/` nie trafia na stronę) (aktualna wersja aplikacji), dokumentacja w `docs/`. Każda wersja = commit z opisem. Na początku nowego czatu: podłączyć repo (add_repo Bamboo869/Moneytrackrr), sklonować i pracować na `site/index.html`. Opublikowane treści (content.json, artykuly/, poradniki/, img/, sitemap.xml, rss.xml, robots.txt) też muszą leżeć w `site/`, inaczej wdrożenie z GitHuba je skasuje.

## 2. Funkcje (stan v0.9)
- Operacje: dodawanie, edycja, szybkie dodawanie, usuwanie z cofnięciem (undo), filtry, wyszukiwarka, import CSV.
- Kalendarz z kropkami kolorów kategorii; okno dnia z zwijaną sekcją „Zaplanowane”.
- Operacje planowane i cykliczne, przycisk „Zaksięguj teraz” (zielony ptaszek), automatyczne księgowanie, przypomnienia.
- Kategorie edytowalne i usuwalne, kolory propagują się do kalendarza i wykresów.
- Okna podsumowań powiązane z kategoriami (Saldo nieusuwalne), ikona (i) w prawym górnym rogu, porównanie z poprzednim okresem.
- Budżety, cele oszczędnościowe (cykliczne wpłaty, prognoza liczby miesięcy do celu), konta i przelewy (wybór ikony konta).
- Wykresy z własnym wyborem dnia/miesiąca/roku; okno średnich wydatków.
- 4 motywy: jasny, kremowy, ciemny, północny (przy pierwszym uruchomieniu żaden nie jest wybrany).
- Zwijanie i ukrywanie okien; ustawienia globalne vs lokalne.
- PL/EN dla całej strony; format daty `01.01.2026` lub „1 stycznia 2026”.
- Zakładki: Home (aktualności, aktualizacje, plany), Poradniki, Regulamin (brak odpowiedzialności, to nie bank).
- Panel autora: dodawanie/edycja artykułów i treści Home, publikacja jako ZIP.
- Pełne strony artykułów (aktualności, poradniki): okładki, galerie, spis treści w formie kropek z scroll-spy po lewej, reklama tylko w aktualnościach (lewa strona), sugestie po prawej. Ambicja: ruch 10 000+ odwiedzin miesięcznie.

## 3. Architektura
- Jeden plik HTML. Dane w localStorage:
  `money_tracker_tx_v3`, `money_tracker_rec_v3`, `mt_settings_v1`, `mt_cats_v1`/`mt_cats_v2`, `mt_cards_v1`, `mt_budgets_v1`, `mt_goals_v1`, `mt_accounts_v1`, `mt_transfers_v1`, `mt_content_draft`, `mt_admin_h` (hash SHA-256 hasła autora).
  sessionStorage: `mt_admin`. Obrazy: IndexedDB `mt_images`.
- Skrypty ładowane kolejno; późniejsze nadpisują wcześniejsze funkcje przez ponowne przypisanie (np. `render`, `openWallet`, `fillAccSelects`, `saveCat`, `bookRec`, `recRow`, `renderRecurring`, `openGuide`, `saveArticle`, `publishFiles`). Kolejność bloków: oryginał v3 → v4 (+i18n) → v5 → v6 → seeds (`DEFAULT_ARTICLES`) → v7 → v8.
- i18n: tłumaczenie węzłów tekstowych DOM i atrybutów przez MutationObserver; słownik `I18N_EN.exact` + `.rx`; funkcje `LANG`, `setLang`, `trStr`, `trWalk`, `trRestore`. `Date.prototype.toLocaleDateString` i `Intl.NumberFormat` są spatchowane pod język.
- Treści: obiekt `CONTENT` (artykuły `kind: news|guide`, cover, gallery, featured, pola EN; announcements, updates, plans, site{baseUrl, author, ad}). Wczytywany z `content.json` (fetch), szkic autora w localStorage. Wpisy updates/plans mają opcjonalne `titleEn`/`textEn`.
- Publikacja = pobierany ZIP (content.json, sitemap.xml, robots.txt, rss.xml, HTML artykułów w `/artykuly/` i `/poradniki/`, `/img/*.jpg`) przeciągany na Netlify. ZIP budowany własnym mini-writerem (`makeZip`, `crc32`).
- Czytnik artykułów: `mdFull` (markdown-lite: `## rozdział`, `![alt](img:id lub https)`), spis kropek + `spy()`, `stickyH()`, lightbox, `coverFor()` (gradient SVG wg tagu).
- Inne ważne funkcje: `recPaid(r,ym)` (sprawdza też przelewy), `goalForecast(g)`, `wireForm(f)`, stan czytnika `RD`, ustawienia wykresów `chartP`, ustawienia średnich `S.avg`, `defContent()`, `deltaInfo(c,val)`/`prevInView`/`prevLabel` (porównanie okresów), `APP_VERSION`.

## 4. Pułapki (nauczone na błędach)
1. Podgląd w sandboxowanym iframe blokuje wysyłanie formularzy (brak `allow-forms`) → formularze obsługuje `wireForm()` (click/Enter ręcznie). Nie wracać do natywnego `submit`.
2. localStorage może być zablokowany → shim + `safeSet`; zawsze try/catch.
3. Wstrzykiwanie kodu przed końcem dokumentu: używać `rindex('</body>')`, nigdy `replace('</body>')`, bo szablony artykułów zawierają `</body>`.
4. W template literalach pisać `<\/script>`, inaczej skrypt się ucina („Unexpected end of input”).
5. Menu/popovery: jeden `#floatMenu` w `body` (nie wewnątrz modala – były ucinane); zamykanie przy scrollu chronione znacznikiem `__fo`.
6. Okna mają stałą wysokość z suwakiem tylko przy przepełnieniu; pary okien równej wysokości (`align-self:stretch`, `max-height:640px`).
7. Przesuwanie dat na wykresach: `chShift` przycina dzień do końca miesiąca.
8. Po każdej zmianie sprawdzać składnię każdego bloku `<script>` (`node --check`) i testować w Chromium/Playwright. W testach Playwright najpierw zamknąć/ukryć kreator powitalny (zasłania stronę i rozmywa tło).
9. Nowe teksty UI zawsze dopisywać do słownika EN, inaczej wersja angielska zostaje po polsku.
10. `DEFAULT_UPDATES` działa tylko, gdy `content.json` (Netlify) i szkic autora nie mają własnej listy updates (`normContent` bierze niepustą listę z content.json). Po wdrożeniu nowej wersji dopisać wpis aktualizacji w panelu autora i opublikować, inaczej nie pojawi się na Home.
12. **Service worker:** przy każdej nowej wersji podbić `CACHE` w `site/sw.js` (np. `mt-v0.12`). Strategia „najpierw sieć” – nowa wersja ładuje się od razu, gdy jest internet; użytkownik dostaje toast „Dostępna nowa wersja – Odśwież”. SW działa tylko przez https/localhost (nie z pliku, nie w podglądzie). Test offline: lokalny `python3 -m http.server` + Playwright `context.set_offline(True)`.
14. **Nazwy funkcji w IIFE:** lokalna funkcja o nazwie globalnej (np. `go`) przesłania globalną – w v0.15 samouczek miał własne `go()` i nie przełączał widoku. Do globalnych funkcji z wnętrza modułów odwoływać się przez `window.go` albo nadawać lokalnym unikalne nazwy.
13. **Publikacja artykułów:** Netlify wdraża teraz z GitHuba (folder `site/`). Nie przeciągać ZIP-a z panelu na Netlify (nadpisałby sw.js/manifest i zniknąłby przy następnym commicie). Pliki z ZIP-a (bez index.html) wrzucić do `site/` w repo – do czasu backendu (Etap 2).
11. Stopka wersji ma swój wpis w słowniku EN („© Money Tracker · wersja X”) – podbijać oba.

## 5. Zasady pracy z użytkownikiem
- **Aktualizacje na Home:** drobne poprawki (wersje typu 0.x.y) NIE dostają osobnego wpisu – dopisujemy je do wpisu najbliższej większej wersji albo scalamy. Jeden wpis = jedna funkcja/zestaw zmian, bez „śmiecenia” poprawkami (prośba użytkownika z 13.10.2026).
- Odpowiadać po polsku, konkretnie. Użytkownik zgłasza błędy krótko i oczekuje poprawek, nie dyskusji.
- Gdy prosi o poprawki – robić dokładnie to, co napisał; nie przebudowywać niezwiązanych części.
- Każda nowa wersja = wpis w aktualizacjach na Home (`DEFAULT_UPDATES`, z `titleEn`/`textEn`) i podbicie numeru wersji (`APP_VERSION`, stopka PL + EN).
- Szczerze podawać, czego nie przetestowano (podgląd wizualny, realne Netlify, telefon, Google).
- Pipeline budowania (skrypty `patch*.py`) nie istnieje. Edytować bezpośrednio najnowszy plik HTML z projektu. Zmiany robić chirurgicznie, nie przepisywać całości.

## 6. Otwarte sprawy
- Zrzuty ekranu v8 nie przejrzane wizualnie; czytnik artykułów wymaga kontroli na telefonie.
- Regulamin: administrator = „Tommy”; brakuje e-maila kontaktowego; zalecany przegląd prawnika.
- Link „Buy me a coffee”: zamienić `TWOJ_NICK`.
- W panelu publikacji ustawić `baseUrl` (adres Netlify), żeby sitemap/RSS były poprawne.
- Porównanie okresów zestawia trwający miesiąc z całym poprzednim – rozważyć opcję „do tego samego dnia”.
- Plany (omówione w v0.9, niewdrożone): Premium (raport A4/PDF, sync, import banków, wspólny budżet, OCR paragonów, prognozy), pakiet dla firm, backend PHP+MySQL na seohost (konta, sync, artykuły bez redeployu), PWA/offline z komunikatem „brak połączenia”, kampania TikTok/IG/YT/Reddit.
- Pomysły odłożone: PIN, automatyczne kopie zapasowe, reklamy (np. AdSense po osiągnięciu ruchu).

## 7. Jak publikować
1. W aplikacji: zalogować się do panelu autora, edytować artykuły/Home.
2. „Publikuj” → pobrać ZIP → rozpakować → przeciągnąć cały folder (z `index.html` = aktualny plik aplikacji) na Netlify Deploys.
3. Dane użytkowników zostają w ich przeglądarkach (localStorage) – wdrożenie ich nie kasuje; zalecić eksport/kopię przed większymi zmianami.
