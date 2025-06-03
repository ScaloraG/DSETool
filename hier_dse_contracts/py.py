
import pprint
from typing import List
from contracts.layer import Layer
from systems.factory import build
from drivers import iterate

# ---------- load layers ----------
layers: List[Layer]
layers, conv = build("configs/toy.yml")

print("First run -> cost history:")
print(iterate(layers, conv))

print("\nLayer contracts after first run:")
for l in layers:
    pprint.pprint((l.name, l.contract.A, l.contract.G))

# ---------- inject failure ----------
print("\nInjecting failure: tighten Physical 'lat' to (0, 5)")
print("Old A_Physical:", layers[0].contract.A)
layers[0].contract.A["lat"] = (0, 5)
print("New A_Physical:", layers[0].contract.A)

print("\nRepair run -> cost history:")
print(iterate(layers, conv))

print("\nLayer contracts after repair run:")
for l in layers:
    pprint.pprint((l.name, l.contract.A, l.contract.G))