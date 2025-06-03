from abc import ABC, abstractmethod

class SearchBackend(ABC):
    """
    Minimal interface every optimiser must expose.
    Returns (solution_dict, cost).
    """
    @abstractmethod
    def optimise(self, params, λ=None):
        ...
