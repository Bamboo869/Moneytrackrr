# Money Tracker – plan etapów (roadmapa)

Ustalone 13.10.2026. Kolejność ma znaczenie: każdy etap stoi na poprzednim.

## Zasady produktu (nie zmieniamy)
- Aplikacja działa w pełni offline i bez konta. Dane domyślnie zostają w przeglądarce użytkownika.
- Konto jest dodatkiem: synchronizacja między urządzeniami, kopia w chmurze, później wspólny budżet dla par.
- Narzędzie jest czyste, bez reklam. Zarabia tylko Premium.
- Reklamy wyłącznie w sekcji artykułów (aktualności).

## Etap 0 – porządek (teraz, 0 zł)
- Kod w repozytorium GitHub (historia wersji, koniec ze znikającymi plikami).
- Domknięcie spraw v0.8/v0.9: słownik EN, dane w regulaminie, link Buy me a coffee.

## Pomysły zatwierdzone do zrobienia przed Etapem 1
- PWA (instalacja na komputerze, offline, komunikat „brak połączenia” w wiadomościach).
- „Codzienna porada” – lokalny silnik reguł (bez AI): przypomnienie o wpisywaniu, wzrost kategorii vs średnia, częste drobne zakupy, wykryte subskrypcje, tempo budżetu, wpływ ograniczenia na cel. Wersja reguł za darmo; AI i raporty tygodniowe jako kandydat do Premium.
- Wersja mobilna strony (obecnie prawie nie działa na telefonie) – osobny etap, przed instalacją PWA na telefonie.

## Etap 1 – domena i hosting
- Domena moneytrackrr.app (sprawdzić cenę odnowienia, nie tylko pierwszego roku).
- Hosting seohost (SH 1 lub SH 2; sprawdzić cenę odnowienia i możliwość zmiany pakietu).
- Strona pod własną domeną z HTTPS.
- PWA: instalacja na telefonie, działanie offline, komunikat „brak połączenia” w wiadomościach.

## Etap 2 – artykuły z serwera (pierwszy backend: PHP + MySQL)
- Panel autora zapisuje artykuły na serwerze, bez wdrażania strony.
- Strony artykułów generowane przez serwer (dobre dla Google), sitemap automatyczna.
- Polityka prywatności i cookies.
- Treści: własne, nie przepisywane z cudzych artykułów. Codzienne szkice może przygotowywać Claude (zadanie zaplanowane), autor sprawdza i publikuje.

## Etap 3 – reklamy
- Po zebraniu ok. 20–30 wartościowych artykułów i pierwszego ruchu: wniosek do AdSense.
- Tylko ręcznie wstawiane jednostki reklamowe w artykułach (bez automatycznych reklam).
- Certyfikowany baner zgody na cookies (CMP) – wymóg Google w UE.

## Etap 4 – konta i synchronizacja
- Rejestracja, logowanie, reset hasła.
- Synchronizacja: dane nadal lokalnie, serwer to kopia i pośrednik między urządzeniami.
- Rozważyć szyfrowanie po stronie użytkownika (spójne z hasłem „prywatność”).

## Etap 5 – Premium
- Płatności (np. Stripe / Przelewy24), forma prawna działalności – konsultacja z księgowym.
- Pierwsze funkcje: raport A4/PDF, prognoza salda, reguły importu z banków.

## Etap 6 – dalej
- Wspólny budżet dla par.
- Aplikacja na telefon (na tym samym API).
- Ewentualny pakiet dla firm.
