from collections import deque
from typing import List
from contracts.layer import Layer
from contracts.entail import intervals_entail

def repair(layers: List[Layer], start_idx: int) -> None:
    """
    Re-optimise starting at `start_idx` and propagate only
    to neighbours whose contracts are now violated.
    """
    Q = deque([start_idx])
    while Q:
        i = Q.popleft()
        layers[i].search()                 # local solve

        # ---- downward check ----
        if i + 1 < len(layers):
            A_child = layers[i+1].contract.A
            if not intervals_entail(layers[i].contract.G, A_child):
                layers[i+1].contract.A = layers[i].contract.G.copy()
                Q.append(i+1)

        # ---- upward check ----
        if i - 1 >= 0:
            if not intervals_entail(layers[i-1].contract.G,
                                     layers[i].contract.A):
                Q.append(i-1)

def iterate(layers: List[Layer], conv: dict):
    eps      = float(conv.get("eps", 1e-3))
    max_iter = int  (conv.get("max_iter", 10))
    hist: list[float] = []

    # initial global solve (all layers dirty)
    for idx in range(len(layers)):
        repair(layers, idx)

    for _ in range(max_iter):
        cost = sum(l.cost for l in layers)
        hist.append(cost)
        if all(l.has_converged(eps) for l in layers):
            break
    return hist
