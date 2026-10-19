"""Lokální REST API pouze pro H5N1 simulaci."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .simulation import SCENARIOS, FleetSimulator


app = FastAPI(
    title="H5N1 Drone Safety Lab",
    description="Pouze virtuální flotila; neovládá skutečné drony ani nevysílá rádiový signál.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
sim = FleetSimulator()


class ScenarioInput(BaseModel):
    name: str = Field(min_length=1, max_length=40)


class StepInput(BaseModel):
    seconds: float = Field(default=1.0, gt=0, le=5)


@app.get("/api/v1/health")
def health() -> dict[str, object]:
    return {"status": "ok", "project": "H5N1", "mode": "SIMULATION", "simulation": True}


@app.get("/api/v1/fleet")
def fleet() -> dict[str, object]:
    return sim.snapshot()


@app.get("/api/v1/scenarios")
def scenarios() -> dict[str, object]:
    return {"scenarios": list(SCENARIOS), "simulation": True}


@app.post("/api/v1/scenario")
def select_scenario(request: ScenarioInput) -> dict[str, object]:
    try:
        sim.set_scenario(request.name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return sim.snapshot()


@app.post("/api/v1/step")
def step(request: StepInput) -> dict[str, object]:
    try:
        return sim.tick(request.seconds)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/v1/preflight")
def preflight() -> dict[str, object]:
    return sim.preflight()


@app.get("/api/v1/audit")
def audit() -> dict[str, object]:
    return {"entries": sim.audit.entries[-100:], "chainValid": sim.audit.verify(), "simulation": True}
