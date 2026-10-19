# H5N1 – úplný katalog požadavků

Tento dokument konsoliduje **všechny dosud navržené funkce**. Jde o produktový rozsah, **nikoliv seznam hotových schopností**. Aktuální stav implementace je popsán dále v dokumentaci a má přednost před marketingovými názvy.

## A. Řízení produktu, vizualizace, flotila

| ID | Modul | Úloha | Stav na startu |
|---|---|---|---|
| FL-01 | H5N1 Control Center | přehled flotily, stav, alerty, úlohy | prototyp |
| FL-02 | FPV HUD / OSD | uživatelské indikátory, kritická varování | specifikace / HW |
| FL-03 | Flight Telemetry | rychlost, výška, napětí, kvalita spojení, GPS, historie | simulace |
| FL-04 | Flight Replay | zpětná rekonstrukce letu z časové osy | specifikace |
| FL-05 | Guardian Escort | konfigurace rolí Primary/Sentinel/Shield/Relay/Rescue | simulace rolí |
| FL-06 | Guardian Coordination | bezpečné sdílení upozornění a stavu flotily | specifikace |
| FL-07 | Secure Drone Mesh | autentizované zprávy, více cest, prevence replay | prototyp identity; síť specifikace |
| FL-08 | Emergency Command Isolation | oddělení pravomocí AI/operátor/autopilot | specifikace |
| FL-09 | Formation Safety Bubble | varování při přiblížení členů flotily | simulace |
| FL-10 | Flight Black Box | auditní log telemetrie a bezpečnostních rozhodnutí | prototyp |

## B. Pasivní pozorování a analýza okolí

| ID | Modul | Úloha | Stav na startu |
|---|---|---|---|
| SE-01 | Acoustic Drone Detection | rozpoznat pravděpodobnou přítomnost zvuku dronu | specifikace / dataset |
| SE-02 | Acoustic Fingerprinting | porovnat zvuk s dokumentovanými referencemi | specifikace |
| SE-03 | Drone Type Classifier | výrobce/model + kalibrovaná důvěra, třída UNKNOWN | specifikace |
| SE-04 | Sound Library | verzovaná databáze nahrávek, metadat a souhlasů | specifikace |
| SE-05 | Drone Vision | vizuální detekce dronu v obraze | specifikace / HW |
| SE-06 | Passive RF Observer | pasivní anomálie ve spektru tam, kde je to legální | specifikace / HW |
| SE-07 | Signal Fingerprint AI | charakteristiky legálně přijatých signálů | specifikace / HW |
| SE-08 | Airspace Awareness | dostupné informace o okolním provozu | specifikace / HW |
| SE-09 | AI Explanation | zdůvodnění odhadu s uvedením limitů dat | specifikace |

## C. Kybernetická obrana vlastních dronů

| ID | Modul | Úloha | Stav na startu |
|---|---|---|---|
| CY-01 | H5N1 Port Audit („Nmap Shield“) | audit povolených služeb výhradně u vlastních uzlů | specifikace |
| CY-02 | Drone IDS | detekce anomálií vlastního palubního provozu | specifikace |
| CY-03 | Link Integrity Shield | autenticita, konzistence a stáří zpráv | prototyp autentizace |
| CY-04 | Anti-Jamming Defense | indikace degradace vlastního spojení a failsafe | specifikace / HW |
| CY-05 | GNSS Spoofing Detector | křížová kontrola GNSS vs. další senzory | specifikace / HW |
| CY-06 | Sensor Trust Engine | detekce rozporů senzorů, práce s nejistotou | specifikace |
| CY-07 | Secure Boot Guardian | ověřený start a podepsaný firmware | specifikace / HW |
| CY-08 | Drone Identity Shield | identita uzlů, autentizace a anti-replay | prototyp |
| CY-09 | Firmware Rollback Defense | bezpečná aktualizace a návrat k ověřené verzi | specifikace / HW |
| CY-10 | Cyber Incident Recorder | časová osa, evidence a reporty | prototyp |
| CY-11 | Drone Red Team Simulator | jen izolované simulované scénáře | specifikace |
| CY-12 | Electronic Warfare Simulator | simulované rušení/ztráty signálu bez RF vysílání | specifikace |

## D. Bezpečnost letu a okolí

| ID | Modul | Úloha | Stav na startu |
|---|---|---|---|
| SF-01 | Civilian Safety Shield | právo přerušit misi v zájmu okolí | prototyp pravidel |
| SF-02 | Collision Risk Engine | předpověď střetu s překážkou | simulace |
| SF-03 | Time to Collision | čas k průniku obálky překážky | simulace |
| SF-04 | Stopping Distance | konzervativní odhad brzdné dráhy | simulace |
| SF-05 | Civilian Risk Map | mapové vrstvy budov, škol a veřejných prostor | specifikace / mapová data |
| SF-06 | Impact Zone Predictor | množina možných dopadů při poruše | specifikace |
| SF-07 | Smart Parachute Controller | jen podpora certifikovaného HW a konfigurace | specifikace / HW |
| SF-08 | Motor Health AI | predikce poruch z vibrací, proudu a otáček | specifikace / HW |
| SF-09 | Battery Failure Predictor | stav, teplota, rezerva pro návrat | specifikace / HW |
| SF-10 | Wind Intelligence | turbulence, boční vítr a bezpečnostní rezerva | specifikace / HW |
| SF-11 | Safe Flight Envelope | limity povolených manévrů a rychlostí | specifikace |
| SF-12 | Safe Landing Intelligence | vhodné a ověřené nouzové přistání | specifikace / HW |
| SF-13 | Civilian Presence Warning | upozornění na osoby v rizikové zóně | specifikace / HW |
| SF-14 | Flight Recovery | předem validované nouzové postupy | specifikace / autopilot |
| SF-15 | Autonomous Preflight Inspector | systémový checklist před vzletem | prototyp / HW |
| SF-16 | Safe Route Planning | trasa upřednostňující nízké riziko pro okolí | specifikace |
| SF-17 | Flight Geofence | vyloučené/provozní oblasti a hraniční pravidla | specifikace / autopilot |

## E. Vývoj, AI, testy a důvěryhodnost

| ID | Modul | Úloha | Stav na startu |
|---|---|---|---|
| DEV-01 | H5N1 Digital Twin Lab | izolovaná virtuální flotila | prototyp |
| DEV-02 | Multi-UAS Simulator | stavy více virtuálních dronů | simulace |
| DEV-03 | Safety Scenario Runner | ztráta spojení, porucha, překážka, degradace | prototyp |
| DEV-04 | Máša Defense Analyst | analýza a vysvětlování; bez řízení aktuátorů | specifikace |
| DEV-05 | AI Vision Lab | offline vyhodnocení testovacích obrazových dat | specifikace |
| DEV-06 | Evidence & Report Builder | reprodukovatelné výsledky testů a protokoly | specifikace |
| DEV-07 | Hardware Adapter | budoucí PX4/ArduPilot pouze ve schváleném režimu | specifikace |
| DEV-08 | Test in Simulation First | testovací brána před jakýmkoliv HW testem | procesní pravidlo |

## F. Výslovně vyloučené funkce

- Aktivní rušení komunikačních nebo navigačních signálů cizích dronů.
- Prolamování řídicích kanálů, převzetí cizího dronu, zásahy do jeho firmwaru.
- Autonomní cílení, fyzické zachytávání či ničení dalších dronů.
- Skenování neautorizovaných telefonů, PC, cizích Wi-Fi nebo infrastruktury.
- Ukrytá/nekontrolovaná aktivní protiopatření spuštěná AI bez schváleného bezpečnostního rámce.

## Pravidlo transparentního UI

Každá karta modulu musí zobrazovat stav **LIVE / SIM / PLANNED / UNAVAILABLE** podle reality. Žádný digitální ukazatel nesmí vytvářet dojem živého senzoru, pokud zobrazuje fiktivní hodnoty. Každý procentuální odhad musí uvést metodiku kalibrace, nebo musí být označen jako demonstrační.

## Zkratky

- UAS: Unmanned Aircraft System (bezpilotní systém).
- GNSS: globální družicové navigační systémy.
- OSD: On-Screen Display, prvky promítané do obrazu.
- TTC: Time to Collision.
- RF: radiofrekvenční oblast.
- IDS: Intrusion Detection System.
- SITL: Software In The Loop, simulace běhu autopilota.
- HIL: Hardware In The Loop, test se skutečnou řídicí elektronikou.
- MAVLink: komunikační protokol běžně používaný v robotice/UAS.
- Fail-safe: předem ověřená reakce na ztrátu spolehlivosti nebo řídicí schopnosti.
