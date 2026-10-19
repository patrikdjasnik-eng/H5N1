# H5N1 🐇🛸

**Drone Safety & Cyber Defense Research Lab**

H5N1 je výzkumná platforma pro **bezpečnost dronů, prevenci kolizí s obytnými budovami a kybernetickou odolnost vlastní flotily**. Produktový koncept zahrnuje hlavní dron a doprovodné Guardiany se specializovanými rolemi. První dodaná verze je **lokální simulátor**, nikoliv produkční autopilot.

## Co tato vývojová verze reálně obsahuje

- Deterministický Python simulátor se třemi virtuálními drony, oblastí obytné budovy a veřejným prostorem.
- Predikce TTC vůči jednoduchým 3D překážkám a odhad konzervativní brzdné dráhy.
- Výstrahy na nebezpečně malou vzdálenost dronů, poruchu motoru, slabou baterii, ztrátu linku a zastaralou telemetrii.
- Prototyp identity zpráv vlastních uzlů přes HMAC s odmítáním replay.
- In-memory auditní řetězec s kontrolou hash integrity.
- REST API FastAPI a React/TypeScript dashboard s tmavým fialovým rozhraním.
- Šest reprodukovatelných testovacích scénářů, automatizovaná testovací sada a GitHub Actions konfigurace.
- Kompletní česká specifikace **všech dříve navržených funkcí** včetně stavu jejich realizace.

**Není implementováno:** skutečné ovládání dronů, živý FPV obraz, akustická klasifikace modelů, kamery, RF senzory, fyzická formace, reálné failsafe ani produkční AI Máša. Jsou vedené jako samostatné, testovatelné vývojové úkoly. UI je výslovně označuje jako PLANNED nebo SIM.

## Rychlé spuštění – PowerShell

    git clone https://github.com/patrikdjasnik-eng/H5N1.git
    cd H5N1
    git switch feat/h5n1-defense-foundation
    .\scripts\start.ps1

Skript nainstaluje chybějící závislosti, spustí backend na http://127.0.0.1:8765 a dashboard na http://127.0.0.1:5174. Ke spuštění skriptu potřebuješ Python 3.11+, Node.js s npm a běžný PowerShell. Pro ruční a snadněji laditelný postup viz dokument 04-SPUSTENI-A-OVLADANI.md.

### Testy

Backend v prostředí s balíčkem nainstalovaným v režimu editable:

    cd backend
    python -m pip install -e ".[dev]"
    python -m pytest -q

Frontend:

    cd frontend
    npm install
    npm run build

## Dokumentace v češtině

| Dokument | Obsah |
|---|---|
| [00 – Vize a rozsah](docs/00-VIZE-A-ROZSAH.md) | cíle, odpovědnost a hranice |
| [01 – Katalog funkcí](docs/01-KATALOG-FUNKCI.md) | všechny požadavky a stav každého modulu |
| [02 – Architektura](docs/02-ARCHITEKTURA.md) | logika, datové vrstvy a role |
| [03 – Safety, Security a právo](docs/03-SAFETY-SECURITY-A-PRAVO.md) | model hrozeb, provozní rizika |
| [04 – Instalace a ovládání](docs/04-SPUSTENI-A-OVLADANI.md) | Windows PowerShell a API |
| [05 – Testy a metriky](docs/05-TESTY-A-METRIKY.md) | přejímka a měřitelnost |
| [06 – Senzory a hardware](docs/06-SENZORY-A-HARDWARE.md) | budoucí integrace a akustická AI |
| [07 – API a události](docs/07-API-A-UDALOSTI.md) | přesné endpointy v0.1 |
| [08 – Roadmap a BRAVE1](docs/08-ROADMAP-A-BRAVE1.md) | etapy a prezentační podklady |

## Zásadní bezpečnostní hranice

Projekt je **simulation-first**, bez aktivního RF rušení, hackování cizích zařízení, převzetí cizího řízení, zbraní či autonomního cílení. Simulační část nikdy nevydává skutečné motorové nebo navigační příkazy. Hlavní prioritou je bezpečnost lidí, budov a vzdušného prostoru; AI smí doporučovat, ne obcházet lokální bezpečnostní mechanismy. Neexistuje záruka 100% ochrany před střetem.

## Stav

**Vývojová větev:** feat/h5n1-defense-foundation

**Release:** dosud nevydáno a neověřeno na fyzických dronech.

**Licence:** zatím nebyla stanovena; nepředpokládej open-source licenci bez výslovného rozhodnutí vlastníka.
