# H5N1 – REST API a události (simulace v0.1)

Základní adresa: http://127.0.0.1:8765

Všechna aktuální API volání se týkají **pouze virtuální flotily**. Neexistují zde žádné endpointy pro skutečné motorové řízení, navigaci či vysílání.

## GET /api/v1/health

Vrací stav služby a povinný údaj mode=SIMULATION. Tato odpověď nesvědčí o dostupnosti reálného hardware.

## GET /api/v1/fleet

Snapshot obsahuje:
- project: H5N1;
- mode: SIMULATION;
- scenario: identifikátor aktivního testu;
- elapsedSeconds: uběhlý simulační čas;
- drones: seznam vlastních virtuálních uzlů;
- obstacles: jednoduché geometrické 3D objekty;
- riskAssessments: predikce a výstrahy deterministického jádra;
- auditValid: stav in-memory hash-chain;
- simulation: true.

### Ukázka riskAssessment

    {
      "droneId": "PRIMARY-01",
      "risk": "HIGH",
      "timeToCollisionSeconds": 4.5,
      "stoppingDistanceMeters": 13.467,
      "action": "ABORT_MISSION",
      "reasons": ["OBSTACLE:RESIDENTIAL-01"],
      "simulation": true
    }

Hodnoty jsou příklad, mohou se lišit podle aktuálního scénáře, nikoliv podle skutečných senzorů.

Stavy rizika: LOW, ELEVATED, HIGH, CRITICAL, UNKNOWN.

Akce jsou doporučení: ADVISORY, SLOW_DOWN, ABORT_MISSION, HOLD_AND_REVIEW. Jejich text nikdy neznamená fyzické vykonání autopilotem.

## GET /api/v1/scenarios

Vrací názvy dovolených scénářů: nominal, near_building, link_loss, motor_fault, low_battery, stale_data.

## POST /api/v1/scenario

JSON požadavek:

    { "name": "near_building" }

Odpověď: kompletní nový snapshot. Neplatný název → HTTP 400. Při změně se resetuje virtuální pozice a simulační čas, nikoliv historie auditu.

## POST /api/v1/step

JSON požadavek:

    { "seconds": 1 }

Dovolený interval 0 < seconds <= 5. Odpověď: nový snapshot. Výpočet integruje rovnoměrnou rychlost, neobsahuje skutečný fyzikální solver. API odmítá neplatné vstupy validací.

## GET /api/v1/preflight

Obsahuje pro každý simulovaný uzel batteryOk, linkOk, motorOk a telemetryFresh. Jde o kontrolu datových příznaků v simulaci, nikoliv náhradu fyzické předletové kontroly.

## GET /api/v1/audit

Vrací posledních 100 událostí v paměti běžícího procesu a chainValid. Audit se po restartu backendu ztrácí; pro produkční dokazování by bylo nutné odolné, podepsané a vzdáleně replikované úložiště.

## Bezpečnost API

Mutující endpointy byly vytvořeny pro localhost. V0.1 nemá přihlašování uživatele, rate limiting ani ochranu pro veřejné nasazení. Nevystavuj ho internetu a nenapoj na skutečný hardware.

## Navrhované budoucí události (neimplementováno)

| Typ události | Účel |
|---|---|
| drone.heartbeat | autentizovaný stav vlastního uzlu |
| safety.risk.changed | změna rizika a její příčiny |
| network.link.degraded | odhad zhoršení vlastního spojení |
| telemetry.sensor.disagreement | nesoulad senzorů |
| identity.replay.blocked | odmítnutí znovu použité zprávy |
| model.audio.unknown | neznámý akustický podpis |
| operator.acknowledged | potvrzení výstrahy |
| recovery.requested | návrh konzervativního failsafe |

Každá budoucí událost musí mít schemaVersion, sourceId, timestampUtc, validity a simulation. Události z reálných zařízení nesmějí být smíchány s demo daty bez označení.
