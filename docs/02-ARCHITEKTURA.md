# H5N1 – technická architektura

## Principy

H5N1 odděluje **bezpečnostně kritické rozhodování** od analytické, experimentální a vizualizační vrstvy. Jazykový model Máša je pouze vysvětlující konzultant. Nikdy neposílá motorům ani autopilotu vlastní nouzové příkazy. Výchozí běh je **SITL-like softwarová simulace**, bez napojení na skutečné aktuátory.

```text
+-----------------------------+      +--------------------------------+
| H5N1 Dashboard (React / TS) |<---->| FastAPI + WebSocket (budoucí) |
| status / alerty / přehled   |      | bez přímého řízení hardware    |
+-----------------------------+      +----------------+---------------+
                                                     |
                +------------------------------------+----------------------------------+
                |                                    |                                  |
      +---------v---------+                +---------v----------+             +-----v-----------+
      | Digital Twin      |                | Safety Engine      |             | Cyber Monitor   |
      | virtuální drony   |                | kolize / riziko    |             | podpisy / nonce |
      +-------------------+                +--------------------+             +-----------------+
                |                                    |                                  |
                +--------------------+---------------+----------------------------------+
                                     |
                             +-------v--------+
                             | Audit / Evidence|
                             | jsonl a hash   |
                             +----------------+
```

## Rozdělení vrstev

### (1) Příjem dat

V simulaci jsou zdrojem scénářů interní objekty `DroneState` a `Obstacle`. V budoucnu mohou být zdrojem adaptéry na autopilot či senzor. Každá přijatá položka musí nést:
- `source_id`: známý, autorizovaný vlastní uzel.
- `timestamp_utc` a monotonní pořadí zpráv tam, kde to lze zaručit.
- `simulation`: bool – zdroj nikdy nesmí tvrdit, že jde o živý hardware, když je to simulace.
- `quality`: kvalita či nejistota měření, důvod degradace.
- `schema_version` a `device_firmware` při fyzickém zařízení.

Zastaralá, chybějící nebo nekonzistentní data se nesmějí automaticky nahradit odhadem a vydávat za skutečnost.

### (2) Deterministické bezpečnostní jádro

Přijme polohu `(x,y,z)`, rychlost `(vx,vy,vz)`, zadané překážky (geometrie boxu), bezpečnostní rezervu, časové okno predikce a parametry konzervativního brzdění. Vrací:
- `risk`: LOW / ELEVATED / HIGH / CRITICAL / UNKNOWN.
- `time_to_collision_s`: čas první predikované kolize (nebo `null`).
- `stopping_distance_m`: ilustrativní odhad.
- `action`: ADVISORY / SLOW_DOWN / ABORT_MISSION / HOLD_AND_REVIEW.
- `reasons`: důvody ve strojově čitelných kódech.
- `simulation`: explicitní údaj pro UI.

Tento model pracuje s **rovnoměrným přímočarým pohybem**. Nezahrnuje plné aerodynamické ani rotorové chování. Proto je pouze testovací. Reálná bezpečnostní autorita musí být na palubě certifikovaného/ověřeného řídicího systému.

### (3) Koordinace Guardian

Komunikace jednotlivých uzlů sdílí **zdravotní stav**, alerty a důvěryhodnost údajů, nikoliv příkazy k napadení nebo zaměření třetích stran.

Doporučené eventy:
- `drone.heartbeat`
- `drone.health.warning`
- `safety.risk.changed`
- `network.link.degraded`
- `identity.replay.blocked`
- `flight.recovery.requested` (jen doporučení / podklad)
- `operator.acknowledged`

Doporučené pravidlo: podpis každé zprávy, pořadové číslo, čas expirace, ochrana před přehráním, audit a omezení frekvence. První prototyp může mít HMAC v simulaci, produkční systém vyžaduje individuální klíče, bezpečné úložiště klíčů a důkladné kryptografické posouzení.

### (4) Akustika a počítačové vidění

Akustická a obrazová klasifikace jsou **nezávislé návrhové moduly**; samy nesmějí měnit trajektorii nebo aktivovat protiopatření. Přípustné výstupy: `drone_likely`, `family`, `model_candidate`, `unknown`, `calibrated_confidence`, `limitations`. Konkrétní typ dronu je pravděpodobnostní tvrzení, nikdy definitivní identita. Jakýkoliv záznam bez trénovaného a validovaného modelu zobrazí „model neurčen“.

### (5) Cyber Security

- Povolené uzly přes explicitní allowlist, nikoliv přes automatický průzkum neznámých sítí.
- HMAC / podpisy pro integritu a autenticitu, plus anti-replay.
- Šifrování kanálu oddělit od podpisu – podpis **není šifrování**.
- Audit správy přístupu, klíčů a API.
- Izolace logů, bezpečná práce s mediálními soubory, limity uploadu.
- Žádné vykonávání skriptů ani shell příkazů na základě volného textu od AI.
- Offline režim má být výchozí, externí konektivita volitelná a zdokumentovaná.

### (6) Evidence

Záznamy mohou být řetězené kryptografickým hashem pro detekci dodatečných změn. Samotný hash-chain **nezaručuje** autenticitu zdroje, nemožnost smazání ani důvěryhodný čas. Produkční důkazy vyžadují spravované podpisové klíče, oddělené úložiště a postup chain-of-custody.

## Režimy běhu

| Režim | Zdroj dat | Řídí skutečný dron? | Účel |
|---|---|---|---|
| DEMO | generované hodnoty | ne | seznámení s UI |
| SIM | deterministický scénář | ne | vývoj, testy, měření |
| REPLAY | uložený letový soubor | ne | forenzní analýza |
| HIL (plán) | ověřený hardware na stole | ne/podle bezpečné integrace | instrumentační test |
| FLIGHT (plán) | autorizovaný autopilot | až po schválení | oddělený projekt a provozní povolení |

Při spuštění musí být DEMO/SIM zřetelně uvedeno. Nikdy žádné tiché přepnutí do hardwarového režimu.

## Architektura repozitáře

```text
H5N1/
├── README.md
├── backend/
│   ├── pyproject.toml
│   ├── h5n1/
│   │   ├── __init__.py
│   │   ├── safety.py
│   │   ├── identity.py
│   │   ├── simulation.py
│   │   └── api.py
│   └── tests/
├── docs/
│   ├── 00-VIZE-A-ROZSAH.md
│   ├── 01-KATALOG-FUNKCI.md
│   ├── 02-ARCHITEKTURA.md
│   └── ...
└── .gitignore
```

Schéma neimplikuje, že všechny soubory již existují; aktuální seznam ověřuj v kořeni větve.

## Rozhraní a řízení přístupu

První API `/api/v1/...` se používá lokálně pouze s demo/simulačními daty. Jakmile bude dostupné na síti, vyžaduje samostatný návrh autentizace uživatele, povolených originů, limitů dotazů a izolace. Reálná telemetrie nesmí být automaticky veřejná. Websocket, až vznikne, musí mít autentizaci, backpressure a bezpečné ukončení spojení.

## Bezpečné chování při výpadku

- Stará telemetrie → `UNKNOWN`, výstraha; žádné tvrzení o bezpečí.
- Senzory si odporují → konzervativní výsledek, vyžádat kontrolu.
- AI nedostupná → pokračuje deterministický bezpečnostní subsystém.
- Výpadek centralizovaného backendu → žádný nový bezpečnostně kritický příkaz z backendu.
- Neplatná identita → zprávu ignorovat a zaznamenat.
- Ztráta spojení u skutečného letadla → rozhoduje předem validovaný autopilot failsafe.

## Integrace v budoucnu

PX4 nebo ArduPilot přes dokumentované adaptéry; výhradně čtení stavu v první etapě. Jakékoli aktivní ovládání je samostatná bezpečnostní změna, která vyžaduje revizi návrhu, vlastní testovací plán a odpovědnou obsluhu. Není součástí prvního simulátoru.
