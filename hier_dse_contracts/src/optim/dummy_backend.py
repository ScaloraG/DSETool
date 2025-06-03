from typing import Dict, Tuple
from .base import SearchBackend

class DummyBackend(SearchBackend):
    """
    A no-math optimiser: it just shrinks every interval in `params["A"]`
    by 10 % and calls that its 'solution'.  Cost = total interval width.
    Perfect for wiring tests—replace later with PuLP / NSGA-II.
    """
    def optimise(self, params, λ=None):
        A: Dict[str, Tuple[float, float]] = params["A"]
        sol = {k: (v[0]*0.9, v[1]*0.9) for k, v in A.items()}
        cost = sum(v[1] - v[0] for v in sol.values())
        return sol, cost
