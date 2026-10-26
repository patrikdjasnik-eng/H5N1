# H5N1 – hardware, senzory a akustická identifikace

První etapa je jen software. Tento dokument vymezuje budoucí integrační požadavky a upozorňuje na limity.

## Senzory pro ochranu okolí

| Senzor | Možná funkce | Limity |
|---|---|---|
| GNSS / RTK | poloha a rychlost | drift, odrazy, ztráta, možné podvržení |
| IMU | zrychlení, náklon | šum, vibrace, drift |
| barometr | výška | změna počasí |
| optický tok | relativní pohyb | světlo, textura |
| stereo kamera | hloubka a překážky | déšť, tma, protisvětlo |
| LiDAR / radar | vzdálenost | hmotnost, slepé sektory, spotřeba |
| telemetrie ESC | zdraví motorů | závisí na řadiči |
| bateriový senzor | proud, teplota, napětí | kalibrace, stáří článků |
| prostorová mapa | budovy a chráněné oblasti | aktuálnost a přesnost dat |

Senzory mohou být společně chybné. Aplikace musí pracovat s úrovní důvěry a při nepřesných údajích nesmí deklarovat „bezpečno“.

## Akustický modul

Cíl: rozpoznat pravděpodobnou přítomnost dronu, případně technickou rodinu a při dostatečných datech kandidátní model. Nikdy nevydávat klasifikaci modelu jako důkaz nepřátelskosti nebo oprávnění k zásahu.

Postup vývoje:
1. Sestavit licenčně čistý dataset vlastních či veřejně zdokumentovaných civilních dronů.
2. Evidovat model, variantu vrtulí, mikrofon, vzdálenost, prostředí, sampling rate a povětrnostní vlivy.
3. Nahrávky segmentovat, vyhodnotit SNR, připravit mel-spektrogramy nebo vhodné embeddingy.
4. Natrénovat nejprve detektor dronu, až pak identifikaci kategorie/modelu.
5. Podporovat výsledek UNKNOWN při nedostatečné nebo neznámé charakteristice.
6. Validovat na nezávislých letových sezeních, jiných kusech stejného modelu a v různých podmínkách.
7. Otestovat zvlášť mikrofon na zemi a na letícím Guardianu: vlastní vrtule výrazně omezují použitelnost.
8. Neuchovávat zbytečně řeč ani osobní záznamy třetích stran.

Příklad schématu (NENÍ výstup existujícího modelu):

    {
      "classification": "UNKNOWN",
      "modelCandidate": null,
      "calibratedConfidence": null,
      "sensor": "microphone",
      "limitations": ["MODEL_NOT_TRAINED"]
    }

## Komunikační vrstvy

Autopilot, letový spoj, analytický datový link a AI konzultant musí být logicky odděleny. Ztráta analytického linku nesmí vypnout základní bezpečnostní funkci autopilota. Pro vlastní uzly navrhnout ověřování identity a ochranu před replay; podpis zprávy není šifrováním.

## Fyzická bezpečnost

Kryty rotorů, bezpečná manipulace s baterií, kontrola těžiště, nouzová přistávací zóna a vhodně ověřené záchranné mechanismy. Padák lze podpořit pouze u kompatibilní, testované instalace; na malých FPV dronech nemusí dávat smysl.

## Brány k reálným testům

0. Offline testy algoritmů, scénáře poruch, reprodukovatelná chybovost.
1. Hardware na stole bez roztočených vrtulí, pouze čtení autorizovaných senzorů.
2. Samostatně schválený testovací prostor, pilot, pozorovatelé a povolené provozní podmínky.
3. Kontrolovaný let jediného dronu s předem ověřeným autopilot failsafe.
4. Test více dronů až po posouzení rozestupů, nouzových postupů, pravidel provozu a právních oprávnění.

Výsledkem není certifikovaný antikolizní systém ani záruka, že skutečný dron zabrání srážce s domem. Taková tvrzení vyžadují nezávislé bezpečnostní ověření a provozní schválení.
