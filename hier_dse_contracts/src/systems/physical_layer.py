from contracts import Contract, Layer
from optim import phys_pulp_backend

class PhysicalLayer(Layer):
    def __init__(self, contract_cfg):
        super().__init__("Physical", Contract(**contract_cfg))
        self.backend = phys_pulp_backend.PuLPBackend()

    def search(self):
        self.mark_prev()
        sol, cost = self.backend.optimise({"A": self.contract.A})
        # Guarantee = we promise the network layer the same latency
        G = {"lat": (0, sol["lat"])}
        self.contract = Contract(A=self.contract.A.copy(), G=G)
        self.cost = cost
        return self.contract
