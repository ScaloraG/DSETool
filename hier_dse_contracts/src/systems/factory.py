import yaml
from systems import PhysicalLayer, NetworkLayer, ApplicationLayer

MAP = {"Physical": PhysicalLayer,
       "Network":  NetworkLayer,
       "Application": ApplicationLayer}

def build(path: str):
    cfg = yaml.safe_load(open(path))

    # ── NEW: normalise [lo, hi] lists → (lo, hi) tuples ───────────────
    for layer_cfg in cfg["layers"]:
        contract = layer_cfg["contract"]
        # assumptions
        for k, v in contract.get("A", {}).items():
            contract["A"][k] = tuple(v)      # list → tuple
        # guarantees (if any were pre-set in YAML)
        for k, v in contract.get("G", {}).items():
            contract["G"][k] = tuple(v)
    # ──────────────────────────────────────────────────────────────────

    layers = [MAP[L["name"]](L["contract"]) for L in cfg["layers"]]
    conv   = cfg["convergence"]
    return layers, conv