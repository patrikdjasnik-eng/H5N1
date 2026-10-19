"""Deterministické vyhodnocení rizik v offline simulaci.

Model používá přímočarou predikci, není certifikovaným autopilotem.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import sqrt
from typing import Iterable


@dataclass(frozen=True)
class Vector3:
    x: float
    y: float
    z: float

    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def scale(self, scalar: float) -> "Vector3":
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other: "Vector3") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self) -> float:
        return sqrt(self.dot(self))


@dataclass(frozen=True)
class DroneState:
    drone_id: str
    role: str
    position: Vector3
    velocity: Vector3
    battery_pct: float
    link_quality: float
    telemetry_age_s: float = 0.0
    motor_ok: bool = True


@dataclass(frozen=True)
class Obstacle:
    obstacle_id: str
    minimum: Vector3
    maximum: Vector3
    category: str = "building"


class RiskLevel(str, Enum):
    LOW = "LOW"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class RiskResult:
    drone_id: str
    level: RiskLevel
    time_to_collision_s: float | None
    stopping_distance_m: float | None
    action: str
    reasons: tuple[str, ...]
    simulation: bool = True

    def as_dict(self) -> dict[str, object]:
        return {
            "droneId": self.drone_id,
            "risk": self.level.value,
            "timeToCollisionSeconds": self.time_to_collision_s,
            "stoppingDistanceMeters": self.stopping_distance_m,
            "action": self.action,
            "reasons": list(self.reasons),
            "simulation": self.simulation,
        }


def stopping_distance(speed_m_s: float, reaction_s: float, deceleration_m_s2: float) -> float:
    """Pouze orientační podélná brzdná dráha, nikoliv garance letu."""
    if speed_m_s < 0 or reaction_s < 0 or deceleration_m_s2 <= 0:
        raise ValueError("Neplatné parametry odhadu brzdné dráhy")
    return speed_m_s * reaction_s + speed_m_s ** 2 / (2 * deceleration_m_s2)


def time_to_aabb_collision(
    position: Vector3,
    velocity: Vector3,
    obstacle: Obstacle,
    horizon_s: float = 12.0,
    margin_m: float = 2.0,
) -> float | None:
    """Vrátí první čas vstupu do rozšířené 3D překážky."""
    if horizon_s < 0 or margin_m < 0:
        raise ValueError("Čas a rezerva musejí být nezáporné")

    entry, exit_time = 0.0, horizon_s
    for p, v, lo, hi in (
        (position.x, velocity.x, obstacle.minimum.x, obstacle.maximum.x),
        (position.y, velocity.y, obstacle.minimum.y, obstacle.maximum.y),
        (position.z, velocity.z, obstacle.minimum.z, obstacle.maximum.z),
    ):
        lo, hi = lo - margin_m, hi + margin_m
        if lo > hi:
            raise ValueError("Neplatné rozměry překážky")
        if abs(v) < 1e-9:
            if p < lo or p > hi:
                return None
            continue
        t1, t2 = (lo - p) / v, (hi - p) / v
        entry = max(entry, min(t1, t2))
        exit_time = min(exit_time, max(t1, t2))
        if entry > exit_time:
            return None
    return entry if 0 <= entry <= horizon_s else None


def closest_approach(
    first: DroneState, second: DroneState, horizon_s: float = 12.0
) -> tuple[float, float]:
    """Nejmenší vzájemná vzdálenost při konstantních rychlostech."""
    if horizon_s < 0:
        raise ValueError("Čas musí být nezáporný")
    relative_position = first.position - second.position
    relative_velocity = first.velocity - second.velocity
    velocity_sq = relative_velocity.dot(relative_velocity)
    instant = 0.0
    if velocity_sq > 1e-9:
        instant = max(0.0, min(horizon_s, -relative_position.dot(relative_velocity) / velocity_sq))
    minimum_distance = (relative_position + relative_velocity.scale(instant)).length()
    return instant, minimum_distance


def evaluate_risk(
    drone: DroneState,
    obstacles: Iterable[Obstacle],
    other_drones: Iterable[DroneState] = (),
    horizon_s: float = 12.0,
    collision_margin_m: float = 2.0,
    separation_m: float = 6.0,
) -> RiskResult:
    """Advisory-only riziko: funkce nevydává fyzické řídicí povely."""
    if drone.telemetry_age_s > 3.0 or drone.telemetry_age_s < 0:
        return RiskResult(drone.drone_id, RiskLevel.UNKNOWN, None, None, "HOLD_AND_REVIEW", ("STALE_TELEMETRY",))
    if not (0 <= drone.battery_pct <= 100 and 0 <= drone.link_quality <= 1):
        return RiskResult(drone.drone_id, RiskLevel.UNKNOWN, None, None, "HOLD_AND_REVIEW", ("INVALID_TELEMETRY",))
    if horizon_s < 0 or separation_m < 0:
        raise ValueError("Neplatný bezpečnostní horizont")

    speed = drone.velocity.length()
    distance = stopping_distance(speed, reaction_s=0.35, deceleration_m_s2=3.0)
    events: list[tuple[float, str]] = []

    for obstacle in obstacles:
        collision = time_to_aabb_collision(drone.position, drone.velocity, obstacle, horizon_s, collision_margin_m)
        if collision is not None:
            events.append((collision, f"OBSTACLE:{obstacle.obstacle_id}"))

    for other in other_drones:
        if other.drone_id == drone.drone_id:
            continue
        instant, minimum_distance = closest_approach(drone, other, horizon_s)
        if minimum_distance <= separation_m:
            events.append((instant, f"SEPARATION:{other.drone_id}"))

    events.sort(key=lambda event: event[0])
    ttc = events[0][0] if events else None
    reasons = [reason for _, reason in events[:3]]
    level = RiskLevel.LOW
    action = "ADVISORY"

    if ttc is not None and ttc <= 2:
        level, action = RiskLevel.CRITICAL, "ABORT_MISSION"
    elif ttc is not None and ttc <= 5:
        level, action = RiskLevel.HIGH, "ABORT_MISSION"
    elif ttc is not None and ttc <= horizon_s:
        level, action = RiskLevel.ELEVATED, "SLOW_DOWN"

    if not drone.motor_ok:
        level, action = RiskLevel.CRITICAL, "HOLD_AND_REVIEW"
        reasons.append("MOTOR_FAULT")

    if drone.battery_pct < 10:
        if level in (RiskLevel.LOW, RiskLevel.ELEVATED):
            level, action = RiskLevel.HIGH, "ABORT_MISSION"
        reasons.append("LOW_BATTERY")

    if drone.link_quality < 0.15:
        if level in (RiskLevel.LOW, RiskLevel.ELEVATED):
            level, action = RiskLevel.HIGH, "HOLD_AND_REVIEW"
        reasons.append("LINK_DEGRADED")

    return RiskResult(
        drone.drone_id,
        level,
        round(ttc, 3) if ttc is not None else None,
        round(distance, 3),
        action,
        tuple(reasons or ["NO_IMMINENT_RISK_IN_MODEL"]),
    )
