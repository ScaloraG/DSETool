from typing import Dict
from .contract import Interval

def intervals_entail(G: Dict[str, Interval], A: Dict[str, Interval]) -> bool:
    """
    Return True iff every guarantee interval fully contains
    the corresponding assumption interval.
    """
    if A.keys() != G.keys():
        return False
    for k in A:
        loA, hiA = A[k]
        loG, hiG = G[k]
        if loG > loA or hiG < hiA:
            return False
    return True
