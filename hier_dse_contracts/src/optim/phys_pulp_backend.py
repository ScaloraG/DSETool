# src/optim/pulp_backend.py
import pulp
from optim.base import SearchBackend

class PuLPBackend(SearchBackend):
    """
    Shrinks the upper bound of 'lat' by 10 % each time.
    Cost = new interval width (hi - lo).
    """

    def optimise(self, params, λ=None):
        loA, hiA = params["A"]["lat"]

        # want  new_hi = 0.9 * hiA
        new_hi_target = 0.9 * hiA

        # LP: minimise deviation of hi - new_hi_target
        prob = pulp.LpProblem("shrink_lat", pulp.LpMinimize)
        new_hi = pulp.LpVariable("new_hi", lowBound=new_hi_target, upBound=hiA)
        prob += new_hi
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        sol  = {"lat": new_hi.value()}
        cost = sol["lat"] - loA            # interval width
        return sol, cost
