"""Virtuální flotila H5N1; žádné fyzické aktuátory ani RF vysílání."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from .audit import AuditLog
from .safety import DroneState, Obstacle, Vector3, evaluate_risk


SCENARIOS = ("nominal", "near_building", "link_loss", "motor_fault", "low_battery", "stale_data")


def initial_fleet() -> dict[str, DroneState]:
    return {
        "PRIMARY-01": DroneState("PRIMARY-01", "PRIMARY", Vector3(0, 0, 40), Vector3(8, 0, 0), 84, 0.98),
        "GUARDIAN-01": DroneState("GUARDIAN-01", "SENTINEL", Vector3(-12, 18, 43), Vector3(8, 0, 0), 91, 0.99),
        "GUARDIAN-02": DroneState("GUARDIAN-02", "SHIELD", Vector3(-12, -18, 43), Vector3(8, 0, 0), 89, 0.97),
    }


def to_dict(drone: DroneState) -> dict[str, Any]:
    return {
        "id": drone.drone_id,
        "role": drone.role,
        "position": {"x": drone.position.x, "y": drone.position.y, "z": drone.position.z},
        "velocity": {"x": drone.velocity.x, "y": drone.velocity.y, "z": drone.velocity.z},
        "batteryPct": drone.battery_pct,
        "linkQuality": drone.link_quality,
        "telemetryAgeSeconds": drone.telemetry_age_s,
        "motorOk": drone.motor_ok,
        "simulation": True,
    }


class FleetSimulator:
    def __init__(self) -> None:
        self.drones = initial_fleet()
        self.obstacles = [
            Obstacle("RESIDENTIAL-01", Vector3(100, -12, 0), Vector3(130, 12, 62), "residential"),
            Obstacle("PUBLIC-SPACE-01", Vector3(155, 30, 0), Vector3(200, 80, 22), "public"),
        ]
        self.elapsed_s = 0.0
        self.scenario = "nominal"
        self.audit = AuditLog()
        self.audit.append("sim.started", {"scenario": self.scenario, "simulation": True})

    def set_scenario(self, name: str) -> None:
        if name not in SCENARIOS:
            raise ValueError("Neznámý scénář")
        self.scenario = name
        self.elapsed_s = 0.0
        self.drones = initial_fleet()
        primary = self.drones["PRIMARY-01"]
        if name == "near_building":
            primary = replace(primary, position=Vector3(62, 0, 40))
        elif name == "link_loss":
            primary = replace(primary, link_quality=0.05)
        elif name == "motor_fault":
            primary = replace(primary, motor_ok=False)
        elif name == "low_battery":
            primary = replace(primary, battery_pct=7)
        elif name == "stale_data":
            primary = replace(primary, telemetry_age_s=5)
        self.drones[primary.drone_id] = primary
        self.audit.append("sim.scenario.changed", {"name": name, "simulation": True})

    def tick(self, seconds: float = 1.0) -> dict[str, Any]:
        if seconds <= 0 or seconds > 5:
            raise ValueError("Krok musí být větší než 0 a nejvýše 5 sekund")
        self.elapsed_s += seconds
        self.drones = {
            key: replace(drone, position=drone.position + drone.velocity.scale(seconds))
            for key, drone in self.drones.items()
        }
        self.audit.append("sim.advanced", {"seconds": seconds, "elapsed": self.elapsed_s})
        return self.snapshot()

    def preflight(self) -> dict[str, Any]:
        checks = {}
        for drone in self.drones.values():
            checks[drone.drone_id] = {
                "batteryOk": drone.battery_pct >= 20,
                "linkOk": drone.link_quality >= 0.5,
                "motorOk": drone.motor_ok,
                "telemetryFresh": 0 <= drone.telemetry_age_s <= 3,
            }
        return {"checks": checks, "simulation": True}

    def snapshot(self) -> dict[str, Any]:
        drones = list(self.drones.values())
        evaluations = [
            evaluate_risk(drone, self.obstacles, (other for other in drones if other.drone_id != drone.drone_id)).as_dict()
            for drone in drones
        ]
        return {
            "project": "H5N1",
            "mode": "SIMULATION",
            "scenario": self.scenario,
            "elapsedSeconds": round(self.elapsed_s, 2),
            "drones": [to_dict(drone) for drone in drones],
            "obstacles": [
                {
                    "id": obstacle.obstacle_id,
                    "category": obstacle.category,
                    "min": vars(obstacle.minimum),
                    "max": vars(obstacle.maximum),
                }
                for obstacle in self.obstacles
            ],
            "riskAssessments": evaluations,
            "auditValid": self.audit.verify(),
            "simulation": True,
        }
