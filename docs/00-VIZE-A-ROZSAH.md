# H5N1 – vize, rozsah a pravidla projektu

Verze dokumentu: 0.1 · Jazyk: čeština · Stav: návrh + první simulátor

## Poslání

H5N1 je platforma pro **bezpečnost bezpilotních prostředků (UAS)**. Cílem je ochrana vlastních dronů, ochrana osob a budov v okolí, včasné rozpoznávání technických poruch, spolehlivá spolupráce flotily a auditovatelná rozhodnutí asistenta Máša. Výzkumný případ použití zahrnuje **hlavní dron + doprovodné drony Guardian**, nejprve jako simulaci a později v civilně bezpečném testovacím prostředí.

H5N1 **není** systém pro útočné zaměřování, navádění zbraní, rušení cizích rádiových sítí ani autonomní bojové reakce. Slovo „obrana“ znamená detekci, varování, odmítnutí neoprávněných příkazů, bezpečný ústup, nouzový režim a ochranu civilního okolí. Útočné bezpečnostní testy lze provádět výhradně v izolované laboratoři na vlastních autorizovaných systémech.

## Hierarchie priorit

1. Bezpečnost života a zdraví; prevence rizika pro obyvatele, domy a další letový provoz.
2. Dodržení omezení prostoru, povolení a provozních limitů.
3. Udržení dronu ve stabilním, řiditelném stavu; bezpečný návrat nebo přistání.
4. Autenticita řídicích příkazů, integrita palubních dat a ochrana komunikace.
5. Záchrana vybavení, pokračování mise a výkonnost – **nikdy** na úkor bodů 1–4.

## Role flotily

- **Primary:** hlavní civilní výzkumná platforma; nese užitečná data a navigační senzory.
- **Guardian Sentinel:** pozorování stavu okolí a identifikace anomálií v údajích vlastních senzorů.
- **Guardian Shield:** audit autorizovaných příkazů, identita a integrita vlastní flotily.
- **Guardian Relay:** dohled nad vlastní komunikační cestou a upozornění na ztrátu spojení; žádné neautorizované retransmise.
- **Guardian Rescue:** dohled nad bezpečnou vzdáleností, návratem a možnostmi přistání.
- **Máša:** vysvětlující AI analytik poskytující návrhy; nemá právo přebírat bezpečnostní autoritu autopilota.

Role nejsou vázané na konkrétní počet fyzických dronů. První simulace pracuje se třemi virtuálními uzly; rozšiřování závisí na ověřené stabilitě a právních podmínkách.

## Provozní hranice

- Výchozí režim: **offline simulace**, žádný vysílač, žádný letový motor, žádné aktivní řízení fyzického dronu.
- Skenování portů, pokud bude doplněno, pouze u **vlastních výslovně povolených IP uzlů** avioniky a testovací infrastruktury; žádné plošné vyhledávání cizích zařízení.
- Pasivní RF pozorování je výzkumná možnost, ne potvrzení příslušnosti nebo „nepřátelskosti“ dronu.
- Akustická klasifikace nikdy sama neurčuje úmysl či právní status pozorovaného dronu.
- Funkce nevyžadují přístup k telefonům či počítačům jiných osob.
- Žádné aktivní RF rušení, spoofing signálů, převzetí řízení cizího dronu, fyzické zachytávání ani útoky.
- Žádné automatické vynucování rozhodnutí jazykovým modelem; kritická bezpečnost musí běžet deterministicky lokálně a nezávisle.

## Stavy implementace

Každá funkce má **jednoznačný stav**:
- **IMPLEMENTOVÁNO (SIM):** skutečně vykonávaná logika v izolované softwarové simulaci, testovaná.
- **PROTOTYP:** funkční omezený kus bez ověření v reálném provozu.
- **SPECIFIKACE:** návrh, dosud žádný funkční modul.
- **HW/TEST NUTNÝ:** vyžaduje senzory, autopilot, vlastní testovací prostor a ověření.
- **MIMO ROZSAH:** aktivní rušení, neautorizované zásahy, zbraně či zaměřování.

Zápis „AI“, „radar“, „shield“ ani vizuální indikátor v dashboardu **neznamená**, že je připojen skutečný senzor nebo že je systém certifikován. Taková data musejí být vždy označena „SIMULACE“ nebo „DEMO“.

## Kritéria dokončení projektu

Modul nesmí být označen za hotový jen podle UI. Pro přijetí musí existovat:
1. Implementace a popis vstupů/výstupů.
2. Reprodukovatelný pozitivní i negativní test a měřená chybovost.
3. Fail-safe při nedostupnosti zdroje dat a při zastaralých údajích.
4. Auditní záznam a popis bezpečnostních hranic.
5. Srozumitelná česká dokumentace a verze komponent.
6. U hardwaru oddělené ověření v kontrolovaných podmínkách.

Základní pravidlo: **bez důkazu nikdy neslibovat 100% bezpečnost, nulový počet kolizí ani přesnou identifikaci modelu dronu jen podle zvuku.**
