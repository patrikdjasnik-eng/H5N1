"""Centrální pravdivý registr všech požadovaných schopností H5N1."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Feature:
    code: str
    category: str
    title: str
    status: str
    description: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


_MODULE_ROWS = """
FL-01|FLIGHT|H5N1 Control Center|PROTOTYPE|React dashboard pro virtuální flotilu
FL-02|FLIGHT|FPV HUD / OSD|HW_REQUIRED|Budoucí OSD podle kompatibilního videosystému
FL-03|FLIGHT|Flight Telemetry|SIM|Pozice, rychlost, baterie a kvalita simulovaného spojení
FL-04|FLIGHT|Flight Replay|PLANNED|Zpětné přehrání časové osy letu
FL-05|FLIGHT|Guardian Escort|SIM|Role Primary a Guardian v softwarové flotile
FL-06|FLIGHT|Guardian Coordination|PLANNED|Sdílení výstrah mezi vlastními uzly
FL-07|FLIGHT|Secure Drone Mesh|PROTOTYPE|Pouze prototyp autentizace; síť není implementována
FL-08|FLIGHT|Emergency Command Isolation|PLANNED|Oddělení pravomocí AI a autopilota
FL-09|FLIGHT|Formation Safety Bubble|SIM|Predikce nedostatečného rozestupu dronů
FL-10|FLIGHT|Flight Black Box|PROTOTYPE|In-memory hash-chain audit
SE-01|SENSORS|Acoustic Drone Detection|HW_REQUIRED|Vyžaduje nahrávky a validovaný model
SE-02|SENSORS|Acoustic Fingerprinting|PLANNED|Akustické podpisy a porovnání
SE-03|SENSORS|Drone Type Classifier|PLANNED|Odhad modelu s UNKNOWN výsledkem
SE-04|SENSORS|Sound Library|PLANNED|Verzovaný katalog nahrávek
SE-05|SENSORS|Drone Vision|HW_REQUIRED|Vizuální detekce s validovanými daty
SE-06|SENSORS|Passive RF Observer|HW_REQUIRED|Pouze pasivní a povolené RF vstupy
SE-07|SENSORS|Signal Fingerprint AI|HW_REQUIRED|Analýza legálně přijatých signálů
SE-08|SENSORS|Airspace Awareness|HW_REQUIRED|Dostupná data o dalším provozu
SE-09|SENSORS|AI Explanation|PLANNED|Vysvětlení nejistoty dat a odhadu
CY-01|CYBER|H5N1 Port Audit|PLANNED|Audit vlastních autorizovaných uzlů
CY-02|CYBER|Drone IDS|PLANNED|Detekce anomálií vlastní telemetrie
CY-03|CYBER|Link Integrity Shield|PROTOTYPE|HMAC testovacích zpráv, ne reálný link
CY-04|CYBER|Anti-Jamming Defense|HW_REQUIRED|Detekce degradace vlastního spojení
CY-05|CYBER|GNSS Spoofing Detector|HW_REQUIRED|Kontrola rozporu GNSS a senzorů
CY-06|CYBER|Sensor Trust Engine|PLANNED|Důvěra ve více nezávislých měření
CY-07|CYBER|Secure Boot Guardian|HW_REQUIRED|Ověření integrity firmwaru
CY-08|CYBER|Drone Identity Shield|PROTOTYPE|Autentizace a anti-replay v testovacím jádru
CY-09|CYBER|Firmware Rollback Defense|HW_REQUIRED|Bezpečný návrat ověřené verze
CY-10|CYBER|Cyber Incident Recorder|PROTOTYPE|Audit událostí simulace
CY-11|CYBER|Drone Red Team Simulator|PLANNED|Izolované laboratorní testy vlastních uzlů
CY-12|CYBER|Electronic Warfare Simulator|PLANNED|Výpadky a latence pouze softwarově
SF-01|SAFETY|Civilian Safety Shield|SIM|Konzervativní výstrahy při bezpečnostním riziku
SF-02|SAFETY|Collision Risk Engine|SIM|Přímočará predikce proti 3D boxům
SF-03|SAFETY|Time to Collision|SIM|Výpočet času do geometrické kolize
SF-04|SAFETY|Stopping Distance|SIM|Orientační model brzdné dráhy
SF-05|SAFETY|Civilian Risk Map|PLANNED|Mapové vrstvy chráněných oblastí
SF-06|SAFETY|Impact Zone Predictor|PLANNED|Oblast možného dopadu po poruše
SF-07|SAFETY|Smart Parachute Controller|HW_REQUIRED|Podpora pouze ověřeného záchranného systému
SF-08|SAFETY|Motor Health AI|HW_REQUIRED|Vibrace a telemetrie motorů
SF-09|SAFETY|Battery Failure Predictor|HW_REQUIRED|Odhady rezervy energie a teploty
SF-10|SAFETY|Wind Intelligence|HW_REQUIRED|Turbulence a větrná nejistota
SF-11|SAFETY|Safe Flight Envelope|PLANNED|Konzervativní limity pohybu
SF-12|SAFETY|Safe Landing Intelligence|HW_REQUIRED|Vyhodnocení bezpečného místa přistání
SF-13|SAFETY|Civilian Presence Warning|HW_REQUIRED|Lokální detekce osob u přistávací oblasti
SF-14|SAFETY|Flight Recovery|HW_REQUIRED|Ověřené bezpečnostní postupy autopilota
SF-15|SAFETY|Autonomous Preflight Inspector|PROTOTYPE|Checklist virtuálních motorů a napájení
SF-16|SAFETY|Safe Route Planning|PLANNED|Trasy preferující bezpečnost okolí
SF-17|SAFETY|Flight Geofence|HW_REQUIRED|Provozní zóny a omezení prostoru
DEV-01|RESEARCH|H5N1 Digital Twin Lab|SIM|Softwarové experimentální prostředí
DEV-02|RESEARCH|Multi-UAS Simulator|SIM|Tři virtuální drony v lokálních souřadnicích
DEV-03|RESEARCH|Safety Scenario Runner|SIM|Šest deterministických scénářů
DEV-04|RESEARCH|Máša Defense Analyst|PLANNED|AI analytik bez oprávnění řídit hardware
DEV-05|RESEARCH|AI Vision Lab|PLANNED|Offline obrazová klasifikace
DEV-06|RESEARCH|Evidence & Report Builder|PLANNED|Export testovacích protokolů
DEV-07|RESEARCH|Hardware Adapter|HW_REQUIRED|Čtení autorizované telemetrie autopilota
DEV-08|RESEARCH|Simulation First Gate|SIM|Povinné označení dat jako simulace
""".strip()


def module_catalog() -> dict[str, object]:
    features: list[Feature] = []
    codes: set[str] = set()
    allowed = {"SIM", "PROTOTYPE", "PLANNED", "HW_REQUIRED"}

    for row in _MODULE_ROWS.splitlines():
        parts = row.split("|", 4)
        if len(parts) != 5:
            raise ValueError("Poškozený katalog H5N1")
        feature = Feature(*parts)
        if feature.code in codes or feature.status not in allowed:
            raise ValueError("Neplatný identifikátor nebo stav modulu")
        codes.add(feature.code)
        features.append(feature)

    summary = dict(sorted(Counter(item.status for item in features).items()))
    return {
        "project": "H5N1",
        "count": len(features),
        "summary": summary,
        "modules": [item.as_dict() for item in features],
        "simulation": True,
    }
