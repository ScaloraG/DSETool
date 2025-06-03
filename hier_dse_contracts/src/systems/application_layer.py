from contracts import Contract, Layer
from optim import app_pulp_backend

class ApplicationLayer(Layer):
    def __init__(self, contract_cfg):
        super().__init__("Application", Contract(**contract_cfg))
        self.backend = app_pulp_backend.PuLPBackend()

    def search(self):
        self.mark_prev()
        sol, cost = self.backend.optimise({"A": self.contract.A})
        G = {"lat": (0, sol["lat"])}
        self.contract = Contract(A=self.contract.A.copy(), G=G)
        self.cost = cost
        return self.contract
