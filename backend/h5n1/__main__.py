"""Krátké spuštění deterministické simulace bez instalace webového API."""

from __future__ import annotations

import json

from .simulation import FleetSimulator


def main() -> None:
    simulator = FleetSimulator()
    simulator.set_scenario("near_building")
    print(json.dumps(simulator.snapshot(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
