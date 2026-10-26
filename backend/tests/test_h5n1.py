"""Regresní testy deterministického jádra bez externích zařízení."""

import unittest

from h5n1.audit import AuditLog
from h5n1.identity import IdentityVerifier, sign_message
from h5n1.safety import (
    DroneState, Obstacle, RiskLevel, Vector3, closest_approach,
    evaluate_risk, stopping_distance, time_to_aabb_collision,
)
from h5n1.simulation import FleetSimulator
from h5n1.registry import module_catalog


class SafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.building = Obstacle("HOME", Vector3(20, -5, 0), Vector3(30, 5, 20))
        self.drone = DroneState("D1", "PRIMARY", Vector3(0, 0, 10), Vector3(5, 0, 0), 80, 1.0)

    def test_predicted_collision(self) -> None:
        ttc = time_to_aabb_collision(self.drone.position, self.drone.velocity, self.building, margin_m=0)
        self.assertAlmostEqual(ttc, 4)

    def test_no_collision_when_flying_away(self) -> None:
        away = Vector3(-5, 0, 0)
        self.assertIsNone(time_to_aabb_collision(self.drone.position, away, self.building))

    def test_collision_is_high_risk(self) -> None:
        outcome = evaluate_risk(self.drone, [self.building])
        self.assertEqual(outcome.level, RiskLevel.HIGH)
        self.assertEqual(outcome.action, "ABORT_MISSION")
        self.assertTrue(outcome.simulation)

    def test_stale_telemetry_is_unknown(self) -> None:
        old = DroneState("D1", "PRIMARY", self.drone.position, self.drone.velocity, 80, 1, 5)
        self.assertEqual(evaluate_risk(old, []).level, RiskLevel.UNKNOWN)

    def test_low_battery_raises_risk(self) -> None:
        empty = DroneState("D1", "PRIMARY", self.drone.position, self.drone.velocity, 4, 1)
        self.assertEqual(evaluate_risk(empty, []).level, RiskLevel.HIGH)

    def test_motor_fault_is_critical(self) -> None:
        failed = DroneState("D1", "PRIMARY", self.drone.position, self.drone.velocity, 80, 1, motor_ok=False)
        self.assertEqual(evaluate_risk(failed, []).level, RiskLevel.CRITICAL)

    def test_formation_proximity(self) -> None:
        another = DroneState("D2", "GUARDIAN", Vector3(0, 3, 10), Vector3(5, 0, 0), 90, 1)
        t, separation = closest_approach(self.drone, another)
        self.assertEqual(t, 0.0)
        self.assertEqual(separation, 3.0)
        self.assertEqual(evaluate_risk(self.drone, [], [another]).level, RiskLevel.CRITICAL)

    def test_stopping_distance_and_validation(self) -> None:
        self.assertAlmostEqual(stopping_distance(6, 0.5, 3), 9)
        with self.assertRaises(ValueError):
            stopping_distance(6, 0.5, 0)


class IdentityTests(unittest.TestCase):
    def test_signature_and_replay(self) -> None:
        key = b"test-secret-keep-in-lab-123456"
        payload = {"state": "ok"}
        timestamp = 100
        nonce = "nonce-1234567890"
        signature = sign_message(key, "D1", nonce, timestamp, payload)
        verifier = IdentityVerifier({"D1": key})
        self.assertTrue(verifier.verify("D1", nonce, timestamp, payload, signature, now=100).accepted)
        self.assertEqual(verifier.verify("D1", nonce, timestamp, payload, signature, now=100).reason, "REPLAY_BLOCKED")

    def test_tampering_and_unknown_identity(self) -> None:
        key = b"test-secret-keep-in-lab-123456"
        signature = sign_message(key, "D1", "nonce-1234567890", 100, {"state": "ok"})
        verifier = IdentityVerifier({"D1": key})
        self.assertEqual(verifier.verify("D1", "nonce-1234567890", 100, {"state": "bad"}, signature, now=100).reason, "INVALID_SIGNATURE")
        self.assertEqual(verifier.verify("D2", "nonce-1234567890", 100, {}, signature, now=100).reason, "UNKNOWN_DRONE")


class SimulationTests(unittest.TestCase):
    def test_scenario_and_preflight(self) -> None:
        simulation = FleetSimulator()
        simulation.set_scenario("near_building")
        state = simulation.snapshot()
        self.assertEqual(state["mode"], "SIMULATION")
        self.assertEqual(len(state["drones"]), 3)
        self.assertEqual(state["riskAssessments"][0]["risk"], "HIGH")
        simulation.set_scenario("motor_fault")
        self.assertFalse(simulation.preflight()["checks"]["PRIMARY-01"]["motorOk"])

    def test_tick_moves_virtual_fleet(self) -> None:
        simulation = FleetSimulator()
        before = simulation.drones["PRIMARY-01"].position.x
        simulation.tick(2)
        self.assertEqual(simulation.drones["PRIMARY-01"].position.x, before + 16)
        with self.assertRaises(ValueError):
            simulation.tick(7)

    def test_invalid_scenario(self) -> None:
        with self.assertRaises(ValueError):
            FleetSimulator().set_scenario("unknown")

    def test_audit_integrity(self) -> None:
        audit = AuditLog()
        audit.append("test", {"ok": True})
        self.assertTrue(audit.verify())
        audit.entries[0]["data"]["ok"] = False
        self.assertFalse(audit.verify())


if __name__ == "__main__":
    unittest.main()


class CatalogTests(unittest.TestCase):
    def test_all_requested_modules_have_unique_identity(self) -> None:
        catalog = module_catalog()
        self.assertEqual(catalog["count"], 56)
        entries = catalog["modules"]
        self.assertEqual(len({entry["code"] for entry in entries}), 56)
        self.assertTrue(catalog["simulation"])

    def test_no_modules_falsely_claim_live_hardware(self) -> None:
        catalog = module_catalog()
        self.assertNotIn("LIVE", catalog["summary"])
        self.assertEqual(set(catalog["summary"]), {"SIM", "PROTOTYPE", "PLANNED", "HW_REQUIRED"})
