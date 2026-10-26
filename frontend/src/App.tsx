import { memo, useCallback, useEffect, useMemo, useState } from "react";
import {
  Activity, AlertTriangle, ArrowRight, BatteryCharging, CheckCircle2,
  CircleHelp, Cpu, LockKeyhole, Radar, RadioTower, RefreshCw, Shield,
  ShieldCheck, Waves, Zap
} from "lucide-react";

type Risk = "LOW" | "ELEVATED" | "HIGH" | "CRITICAL" | "UNKNOWN";

type Drone = {
  id: string;
  role: string;
  position: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
  batteryPct: number;
  linkQuality: number;
  telemetryAgeSeconds: number;
  motorOk: boolean;
  simulation: boolean;
};

type Assessment = {
  droneId: string;
  risk: Risk;
  timeToCollisionSeconds: number | null;
  stoppingDistanceMeters: number | null;
  action: string;
  reasons: string[];
  simulation: boolean;
};

type FeatureCatalog = {
  count: number;
  simulation: boolean;
  summary: Record<string, number>;
  modules: Array<{
    code: string;
    category: string;
    title: string;
    status: "SIM" | "PROTOTYPE" | "PLANNED" | "HW_REQUIRED";
    description: string;
  }>;
};

type FleetData = {
  project: string;
  mode: "SIMULATION";
  scenario: string;
  elapsedSeconds: number;
  drones: Drone[];
  obstacles: Array<{ id: string; category: string; min: { x: number; y: number }; max: { x: number; y: number } }>;
  riskAssessments: Assessment[];
  auditValid: boolean;
  simulation: boolean;
};

const scenarios = [
  { value: "nominal", label: "Standardní let" },
  { value: "near_building", label: "Riziko budovy" },
  { value: "link_loss", label: "Zhoršené spojení" },
  { value: "motor_fault", label: "Porucha motoru" },
  { value: "low_battery", label: "Kritická baterie" },
  { value: "stale_data", label: "Stará telemetrie" }
] as const;

const featureGroups = [
  { icon: Waves, title: "Acoustic Drone ID", description: "Trénování a validace klasifikátoru", status: "PLANNED" },
  { icon: Radar, title: "Passive RF Observer", description: "Pasivní senzorové vstupy", status: "PLANNED" },
  { icon: ShieldCheck, title: "Cyber / Identity", description: "HMAC ověřování v testovacím jádru", status: "PROTOTYPE" },
  { icon: Activity, title: "Collision Risk Engine", description: "Predikce překážek a rozestupů", status: "SIM" },
  { icon: Cpu, title: "Máša Analyst", description: "Vysvětlování výstrah bez řízení letu", status: "PLANNED" },
  { icon: LockKeyhole, title: "Electronic Defense", description: "Pouze software a bezpečné simulace", status: "PLANNED" }
] as const;

function riskLabel(risk: Risk): string {
  return ({ LOW: "Nízké", ELEVATED: "Zvýšené", HIGH: "Vysoké", CRITICAL: "Kritické", UNKNOWN: "Neznámé" })[risk];
}

function riskClass(risk: Risk): string {
  return risk.toLowerCase();
}

function meters(value: number): string {
  return new Intl.NumberFormat("cs-CZ", { maximumFractionDigits: 1 }).format(value);
}

const FormationMap = memo(function FormationMap({ data }: { data: FleetData }) {
  const objects = useMemo(() => data.drones.map((drone) => ({
    ...drone,
    x: 90 + drone.position.x * 1.8,
    y: 195 - drone.position.y * 1.8
  })), [data.drones]);

  return (
    <div className="map-wrap" role="img" aria-label="Schéma simulované flotily a obytné budovy">
      <svg viewBox="0 0 720 380" className="formation-svg" preserveAspectRatio="xMidYMid meet">
        <defs>
          <pattern id="mesh" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M30 0 L0 0 0 30" fill="none" stroke="#242b3d" strokeWidth=".8" />
          </pattern>
          <radialGradient id="glow"><stop offset="0" stopColor="#8d79ff" stopOpacity=".16"/><stop offset="1" stopColor="#8d79ff" stopOpacity="0"/></radialGradient>
        </defs>
        <rect width="720" height="380" fill="#0c101c" rx="16"/>
        <rect width="720" height="380" fill="url(#mesh)" rx="16"/>
        <circle cx="190" cy="195" r="180" fill="url(#glow)" />
        {data.obstacles.map((obstacle) => (
          <g key={obstacle.id}>
            <rect x={90 + obstacle.min.x * 1.8} y={195 - obstacle.max.y * 1.8}
              width={(obstacle.max.x - obstacle.min.x) * 1.8}
              height={(obstacle.max.y - obstacle.min.y) * 1.8}
              fill="#d3677a" fillOpacity=".13" stroke="#e77a8a" strokeDasharray="6 5" strokeWidth="1.5"/>
            <text x={90 + obstacle.min.x * 1.8} y={176 - obstacle.max.y * 1.8} className="svg-building-label">{obstacle.id}</text>
          </g>
        ))}
        {objects.filter((item) => item.role !== "PRIMARY").map((item) => (
          <line key={item.id} x1={objects[0]?.x ?? 90} y1={objects[0]?.y ?? 195} x2={item.x} y2={item.y}
            stroke="#a693ff" strokeOpacity=".35" strokeDasharray="5 6" />
        ))}
        {objects.map((drone) => (
          <g key={drone.id} className={"drone-body " + (drone.role === "PRIMARY" ? "drone-primary" : "drone-guardian")} transform={"translate(" + drone.x + " " + drone.y + ")"} style={{ ["--drone-phase" as string]: drone.id.length * 0.7 + "s" }}>
            <ellipse className="drone-shadow" cx="0" cy="9" rx={drone.role === "PRIMARY" ? 27 : 19} ry="8" fill="#05070c" fillOpacity=".42" />
            <circle className="drone-safety-ring" r={drone.role === "PRIMARY" ? 25 : 17} fill={drone.role === "PRIMARY" ? "#7665eb" : "#60d7bc"} fillOpacity=".09"
              stroke={drone.role === "PRIMARY" ? "#a693ff" : "#60d7bc"} strokeOpacity=".7"/>
            <g className="drone-frame" stroke={drone.role === "PRIMARY" ? "#baafff" : "#68d8c0"} strokeWidth="2.5" strokeLinecap="round">
              <path d="M-5 -5 L-13 -13 M5 -5 L13 -13 M-5 5 L-13 13 M5 5 L13 13" />
              <path d="M-9 -9 L9 9 M9 -9 L-9 9" strokeWidth="3.5" />
            </g>
            {[[-14,-14],[14,-14],[-14,14],[14,14]].map(([rx, ry], rotorIndex) => (
              <g key={rotorIndex} className="rotor" style={{ ["--rotor-delay" as string]: (rotorIndex * -0.12) + "s" }} transform={"translate(" + rx + " " + ry + ")"}>
                <circle r="6.5" fill="#0e1420" stroke="#b6c0da" strokeWidth="1.2"/>
                <ellipse className="rotor-blade" rx="5.5" ry="1.5" fill="#d6ddf2" fillOpacity=".9"/>
                <ellipse className="rotor-blade rotor-blade-second" rx="5.5" ry="1.5" fill="#d6ddf2" fillOpacity=".9" transform="rotate(90)"/>
                <circle r="1.7" fill="#b9aaff"/>
              </g>
            ))}
            <circle r="3.5" fill={drone.role === "PRIMARY" ? "#d9d0ff" : "#b3ffeb"} />
            <text textAnchor="middle" y="39" className="svg-label">{drone.id}</text>
            <line x1="17" y1="0" x2="58" y2="0" stroke="#aaa3fa" strokeWidth="1.5" strokeDasharray="4 5"/>
          </g>
        ))}
        <text x="24" y="32" className="svg-heading">SIMULATED AIRSPACE · XY VIEW</text>
        <text x="24" y="352" className="svg-heading">NENÍ TO REÁLNÁ GPS MAPA</text>
      </svg>
    </div>
  );
});

export default function App() {
  const [data, setData] = useState<FleetData | null>(null);
  const [catalog, setCatalog] = useState<FeatureCatalog | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const response = await fetch("/api/v1/fleet", { signal: AbortSignal.timeout(6000) });
      if (!response.ok) throw new Error("Backend vrátil chybu " + response.status);
      const payload = await response.json() as FleetData;
      if (payload.mode !== "SIMULATION" || !payload.simulation) throw new Error("Neočekávaný režim dat");
      setData(payload);
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Backend nedostupný");
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  useEffect(() => {
    const controller = new AbortController();
    void fetch("/api/v1/modules", { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("Katalog nedostupný");
        return response.json() as Promise<FeatureCatalog>;
      })
      .then((result) => {
        if (!controller.signal.aborted && result.simulation) setCatalog(result);
      })
      .catch(() => {
        // Katalog je doplňková sekce, nedostupnost nesmí zablokovat bezpečnostní stav.
      });
    return () => controller.abort();
  }, []);

  const execute = useCallback(async (path: string, body: object) => {
    setBusy(true);
    try {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(6000)
      });
      if (!response.ok) throw new Error("Operace selhala: " + response.status);
      const payload = await response.json() as FleetData;
      setData(payload);
      setError(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Nelze upravit simulaci");
    } finally {
      setBusy(false);
    }
  }, []);

  const primary = data?.drones.find((drone) => drone.role === "PRIMARY");
  const dangerous = data?.riskAssessments.filter((item) => item.risk !== "LOW") ?? [];

  return (
    <div className="app-shell">
      <aside className="side-bar">
        <div className="brand"><span className="brand-mark"><Shield size={24}/></span>
          <div><strong>H5N1</strong><small>DRONE DEFENSE LAB</small></div>
        </div>
        <div className="section-label">OPERATIONS</div>
        <a className="nav-item active" href="#overview"><Activity size={17}/> Mission Overview</a>
        <a className="nav-item" href="#formation"><Radar size={17}/> Guardian Formation</a>
        <a className="nav-item" href="#alerts"><AlertTriangle size={17}/> Safety Alerts</a>
        <div className="section-label section-gap">RESEARCH MODULES</div>
        {featureGroups.map(({ icon: Icon, title }) => (
          <a className="nav-item" href="#modules" key={title}><Icon size={17}/>{title}</a>
        ))}
        <div className="sidebar-bottom">
          <div className="sidebar-panel"><span className="live-dot"/><strong>LOCAL SIMULATION</strong>
            <p>Bez fyzického řízení, vysílání ani jammingu.</p>
          </div>
          <a className="docs-link" href="https://github.com/patrikdjasnik-eng/H5N1/tree/feat/h5n1-defense-foundation/docs"
            target="_blank" rel="noreferrer">Česká dokumentace <ArrowRight size={13}/></a>
        </div>
      </aside>

      <main id="overview" className="main-content">
        <header className="top-header">
          <div className="breadcrumb">H5N1 <span>/</span> Operations <span>/</span> Simulation</div>
          <div className="header-status"><span className="status-pill"><span className="live-dot"/> SIMULATION ONLY</span><span className="small-time">v0.1.0</span></div>
        </header>

        <section className="intro">
          <div><div className="eyebrow">FLIGHT SAFETY · CYBER RESILIENCE</div>
            <h1>Drone Defense <em>Command</em></h1>
            <p>Ochrana vlastních dronů a civilního okolí. Deterministické scénáře bez ovládání skutečného hardware.</p>
          </div>
          <button className="button secondary" onClick={() => void refresh()} disabled={busy}>
            <RefreshCw size={16}/> Obnovit
          </button>
        </section>

        {error && <div className="error-banner"><AlertTriangle size={17}/>{error}
          <span>Spusť backend na 127.0.0.1:8765.</span></div>}

        <div className="metric-grid">
          <div className="metric-card"><span className="metric-icon purple"><RadioTower/></span><small>SIMULATED DRONES</small>
            <strong>{data?.drones.length ?? "—"}</strong><span>Primary + Guardiani</span></div>
          <div className="metric-card"><span className="metric-icon green"><BatteryCharging/></span><small>PRIMARY BATTERY</small>
            <strong>{primary ? meters(primary.batteryPct) + "%" : "—"}</strong><span>Virtuální telemetrie</span></div>
          <div className="metric-card"><span className="metric-icon blue"><Zap/></span><small>LINK QUALITY</small>
            <strong>{primary ? meters(primary.linkQuality * 100) + "%" : "—"}</strong><span>Simulovaná kvalita</span></div>
          <div className="metric-card"><span className="metric-icon amber"><AlertTriangle/></span><small>ACTIVE WARNINGS</small>
            <strong>{data ? dangerous.length : "—"}</strong><span>Predikce, nikoli potvrzené nehody</span></div>
        </div>

        <div className="workspace-grid">
          <section id="formation" className="panel formation-panel">
            <div className="panel-head"><div><div className="eyebrow">DIGITAL TWIN</div><h2>Guardian Formation</h2></div>
              <span className="tiny-status">SIMULATED XY</span></div>
            {data ? <FormationMap data={data}/> : <div className="panel-placeholder">Načítání virtuální flotily…</div>}
            <div className="map-footer">
              <span><span className="legend-dot violet"/> Primary</span>
              <span><span className="legend-dot mint"/> Guardians</span>
              <span><span className="legend-dot rose"/> Residential zone</span>
            </div>
          </section>

          <section className="panel controls-panel">
            <div className="panel-head"><div><div className="eyebrow">TEST SCENARIOS</div><h2>Safety Simulation</h2></div>
              <CircleHelp size={18} className="muted-icon"/></div>
            <p className="support-copy">Vyber bezpečnostní scénář. Žádný krok neřídí fyzický dron.</p>
            <label htmlFor="scenario" className="form-label">SCENARIO</label>
            <select id="scenario" value={data?.scenario ?? "nominal"} disabled={busy || !data}
              onChange={(event) => void execute("/api/v1/scenario", { name: event.target.value })}>
              {scenarios.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}
            </select>
            <button className="button primary wide" disabled={!data || busy}
              onClick={() => void execute("/api/v1/step", { seconds: 1 })}>Posunout simulaci o 1 s <ArrowRight size={16}/></button>
            <div className="scenario-info"><div><small>SIMULATION TIME</small><strong>{meters(data?.elapsedSeconds ?? 0)} s</strong></div>
              <div><small>AUDIT CHAIN</small><strong className={data?.auditValid ? "success" : "danger"}>{data ? (data.auditValid ? "VALID" : "INVALID") : "—"}</strong></div></div>
            <div className="hint"><ShieldCheck size={17}/><span>Výsledky jsou doporučení bezpečnostního modelu, ne letové příkazy.</span></div>
          </section>
        </div>

        <div className="workspace-grid lower">
          <section id="alerts" className="panel">
            <div className="panel-head"><div><div className="eyebrow">SAFETY ENGINE</div><h2>Risk Assessment</h2></div><span className="tiny-status">SIM</span></div>
            <div className="risk-list">
              {data?.riskAssessments.map((item) => (
                <div className="risk-row" key={item.droneId}>
                  <span className={"risk-marker " + riskClass(item.risk)}/>
                  <div className="risk-meta"><strong>{item.droneId}</strong><small>{item.reasons.join(" · ")}</small></div>
                  <div className="risk-value"><span className={"risk-tag " + riskClass(item.risk)}>{riskLabel(item.risk)}</span>
                    <small>{item.timeToCollisionSeconds === null ? "TTC neurčeno" : "TTC " + meters(item.timeToCollisionSeconds) + " s"}</small></div>
                </div>
              )) ?? <div className="panel-placeholder">Žádná data</div>}
            </div>
          </section>
          <section id="modules" className="panel">
            <div className="panel-head"><div><div className="eyebrow">CAPABILITY STATUS</div><h2>Research Modules</h2></div><span className="tiny-status">{catalog ? catalog.count + " MODULŮ" : "ROADMAP"}</span></div>
            <p className="support-copy">Kompletní registr funkcí. Stav každého modulu odpovídá skutečné implementaci, nikoliv příslibu.</p>
            <div className="feature-list catalog-scroll">
              {catalog ? catalog.modules.map((module) => (
                <div className="feature-item" key={module.code}><span className="module-icon"><Radar size={18}/></span>
                  <div><strong>{module.code} · {module.title}</strong><small>{module.category} · {module.description}</small></div>
                  <span className="module-status">{module.status}</span>
                </div>
              )) : <div className="panel-placeholder">Katalog modulů není dostupný.</div>}
            </div>
          </section>
        </div>

        <footer className="page-footer"><div><CheckCircle2 size={15}/> H5N1 · local-first research</div><span>Žádná reálná telemetrie, zaměřování ani aktivní RF rušení.</span></footer>
      </main>
    </div>
  );
}
