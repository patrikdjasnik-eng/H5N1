"""HMAC identita zpráv vlastních uzlů výhradně pro laboratorní testy.

Produkční systém vyžaduje bezpečné ukládání klíčů a silnější lifecycle.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any


def canonical_message(drone_id: str, nonce: str, sent_at: int, payload: dict[str, Any]) -> bytes:
    return json.dumps(
        {"droneId": drone_id, "nonce": nonce, "sentAt": sent_at, "payload": payload},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def sign_message(secret: bytes, drone_id: str, nonce: str, sent_at: int, payload: dict[str, Any]) -> str:
    if len(secret) < 16:
        raise ValueError("Testovací klíč musí mít nejméně 16 bajtů")
    return hmac.new(secret, canonical_message(drone_id, nonce, sent_at, payload), hashlib.sha256).hexdigest()


@dataclass(frozen=True)
class AuthResult:
    accepted: bool
    reason: str


class IdentityVerifier:
    def __init__(self, keys: dict[str, bytes], ttl_s: int = 30) -> None:
        if ttl_s <= 0:
            raise ValueError("TTL musí být kladné")
        self.keys = dict(keys)
        self.ttl_s = ttl_s
        self.used_nonces: dict[tuple[str, str], int] = {}

    def verify(
        self,
        drone_id: str,
        nonce: str,
        sent_at: int,
        payload: dict[str, Any],
        signature: str,
        now: int | None = None,
    ) -> AuthResult:
        current = int(time.time()) if now is None else now
        self.used_nonces = {key: timestamp for key, timestamp in self.used_nonces.items()
                            if current - timestamp <= self.ttl_s}
        secret = self.keys.get(drone_id)
        if secret is None:
            return AuthResult(False, "UNKNOWN_DRONE")
        if not nonce or len(nonce) < 12:
            return AuthResult(False, "INVALID_NONCE")
        if abs(current - sent_at) > self.ttl_s:
            return AuthResult(False, "EXPIRED_MESSAGE")
        expected = sign_message(secret, drone_id, nonce, sent_at, payload)
        if not hmac.compare_digest(expected, signature):
            return AuthResult(False, "INVALID_SIGNATURE")
        key = (drone_id, nonce)
        if key in self.used_nonces:
            return AuthResult(False, "REPLAY_BLOCKED")
        self.used_nonces[key] = current
        return AuthResult(True, "ACCEPTED")
