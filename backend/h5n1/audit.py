"""Laboratorní audit řetězený přes SHA-256. Nenahrazuje důkazní úložiště."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _canonical(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


@dataclass
class AuditLog:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event_type: str, data: dict[str, Any]) -> dict[str, Any]:
        previous = self.entries[-1]["hash"] if self.entries else "GENESIS"
        body: dict[str, Any] = {
            "index": len(self.entries),
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "eventType": event_type,
            "data": data,
            "previousHash": previous,
        }
        record = {**body, "hash": hashlib.sha256(_canonical(body)).hexdigest()}
        self.entries.append(record)
        return record

    def verify(self) -> bool:
        previous = "GENESIS"
        for index, entry in enumerate(self.entries):
            body = {key: value for key, value in entry.items() if key != "hash"}
            if body["index"] != index or body["previousHash"] != previous:
                return False
            digest = hashlib.sha256(_canonical(body)).hexdigest()
            if digest != entry["hash"]:
                return False
            previous = digest
        return True
