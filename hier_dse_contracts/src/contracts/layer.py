from abc import ABC, abstractmethod
from contracts.contract import Contract

class Layer(ABC):
    """
    Abstract base-class: every concrete layer must implement `search`.
    """
    def __init__(self, name: str, contract: Contract):
        self.name         = name
        self.contract     = contract     # current contract
        self.prev_contract: Contract | None = None
        self.cost: float  = float("inf") # layer-local objective value

    # ----- mandatory -----
    @abstractmethod
    def search(self) -> Contract:
        """
        Run the optimiser for this layer under the current assumptions.
        Must update self.contract and self.cost, then return the NEW contract.
        """

    # ----- generic helpers -----
    def mark_prev(self):
        self.prev_contract = Contract(
            A=self.contract.A.copy(),
            G=self.contract.G.copy(),
            hard=set(self.contract.hard),
            soft=set(self.contract.soft),
            penalty=self.contract.penalty,
        )

    def has_converged(self, eps: float = 1e-3) -> bool:
        if self.prev_contract is None:
            return False
        return self.contract.delta(self.prev_contract) < eps
