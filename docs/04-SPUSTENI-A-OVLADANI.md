# H5N1 – instalace a ovládání (Windows / PowerShell)

## Co bude spuštěno

První verze obsahuje lokální REST API v Pythonu a React dashboard. Jsou to skutečné procesy pracující s virtuálními drony. Žádná část neovládá motory, skutečnou GPS nebo rádiové zařízení. Mapa je v lokálních souřadnicích simulace (metry), nikoliv v zeměpisné poloze.

Požadavky: Python 3.11+, Node.js 20+, npm a Git. Pro běh se používají porty 8765 (backend) a 5174 (dashboard). Port 5174 je zvolen kvůli možnému souběhu s jinými projekty na 5173.

## 1. Stáhni H5N1

    git clone https://github.com/patrikdjasnik-eng/H5N1.git
    cd H5N1
    git switch feat/h5n1-defense-foundation

## 2. Spusť backend v prvním okně PowerShellu

    cd backend
    py -3 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
    .\.venv\Scripts\python.exe -m pytest -q
    .\.venv\Scripts\python.exe -m uvicorn h5n1.api:app --host 127.0.0.1 --port 8765

Interaktivní API dokumentace: http://127.0.0.1:8765/docs

Kontrolní endpoint: http://127.0.0.1:8765/api/v1/health

V Linuxu se Python v prostředí obvykle nachází v .venv/bin/python.

## 3. Spusť dashboard ve druhém okně

V kořeni repozitáře:

    cd frontend
    npm install
    npm run dev

Otevři: http://127.0.0.1:5174/

Vite proxy přesměrovává API volání na 127.0.0.1:8765. Pokud backend neběží, rozhraní vypíše chybu, nikoli vymyšlené hodnoty.

## 4. Simulační scénáře

- Standardní let – tři virtuální drony, jedna obytná budova, jedna veřejná oblast.
- Riziko budovy – hlavní dron je blízko budovy a model má určit čas do předpokládaného kontaktu.
- Zhoršené spojení – pokles kvality vlastního linku v datech.
- Porucha motoru – virtuální příznak poruchy, kritické upozornění.
- Kritická baterie – nedostatečná rezerva energie.
- Stará telemetrie – data starší než 3 sekundy musí znamenat UNKNOWN, ne bezpečí.

Tlačítko Posunout simulaci o 1 s posune modelované pozice při konstantní rychlosti. Není to plná simulace aerodynamiky.

## 5. Příklady REST API

Získání přehledu:

    Invoke-RestMethod http://127.0.0.1:8765/api/v1/fleet

Přepnutí scénáře:

    Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8765/api/v1/scenario -ContentType "application/json" -Body '{"name":"near_building"}'

Posun modelového času:

    Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8765/api/v1/step -ContentType "application/json" -Body '{"seconds":1}'

Rychlý kontrolní výpis bez webového API ze složky backend:

    .\.venv\Scripts\python.exe -m h5n1

## 6. Typické chyby

| Chyba | Příčina | Doporučený postup |
|---|---|---|
| No module named h5n1 | balíček není instalován nebo běží jiný interpreter | instaluj v backendu: python -m pip install -e . |
| Failed to fetch | není spuštěný backend | otevři /api/v1/health a ověř port 8765 |
| EADDRINUSE | jiný proces používá port | Get-NetTCPConnection -LocalPort 5174 -State Listen |
| npm ENOENT | příkaz spuštěn mimo frontend | přejdi do frontend |
| Acoustic ID PLANNED | chybí validovaný model | očekávané chování |
| Máša neovládá dron | bezpečnostní oddělení | očekávané chování |

## 7. Testování a sestavení

Backend, ve složce backend:

    .\.venv\Scripts\python.exe -m pytest -q

Frontend, ve složce frontend:

    npm run build

Pro zastavení procesů v terminálu použij Ctrl+C. Nevypínáš fyzický hardware, protože žádný není připojen.

## 8. Bezpečnostní nastavení

API je určeno k vazbě na localhost. Neupravuj vazbu na 0.0.0.0 bez autentizace, rate limitingu, revize CORS a oddělení prostředí. Mutující API scénářů není vhodné vystavovat veřejnému internetu. V první etapě neukládej reálnou telemetrii ani tajné klíče do repozitáře.

Před jakoukoliv integrací skutečného dronu prostuduj dokumenty 03-SAFETY-SECURITY-A-PRAVO.md a 06-SENZORY-A-HARDWARE.md.
