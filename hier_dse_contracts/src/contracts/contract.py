from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple, Set

Interval = Tuple[float, float]          # (low, high)

def _scale(iv: Interval, factor: float) -> Interval:
    mid  = 0.5 * (iv[0] + iv[1])
    half = 0.5 * (iv[1] - iv[0]) * factor
    return (mid - half, mid + half)

@dataclass
class Contract:
    """
    Simple assume–guarantee contract where both A and G are
    numeric intervals keyed by some variable name.
    """
    A: Dict[str, Interval]              # assumptions
    G: Dict[str, Interval]              # guarantees
    hard: Set[str] = field(default_factory=set)
    soft: Set[str] = field(default_factory=set)
    penalty: float = 0.0                # weight for soft-constraint cost

    # ---------- helpers ----------
    def shrink(self, factor: float = 0.95) -> None:
        self.A = {k: _scale(v, factor) for k, v in self.A.items()}
        self.G = {k: _scale(v, factor) for k, v in self.G.items()}

    def widen(self, factor: float = 1.05) -> None:
        self.A = {k: _scale(v, factor) for k, v in self.A.items()}
        self.G = {k: _scale(v, factor) for k, v in self.G.items()}

    def delta(self, other: "Contract") -> float:
        """Relative L1 distance between this contract and *other*."""
        def _sum(d1, d2):
            keys = set(d1) | set(d2)           # union of keys
            return sum(
                abs((d1.get(k, (0, 0))[i]) - (d2.get(k, (0, 0))[i]))
                for k in keys for i in (0, 1)
            )

        num = _sum(self.A, other.A) + _sum(self.G, other.G)
        den = _sum(other.A, other.A) + _sum(other.G, other.G) + 1e-12
        return num / den

