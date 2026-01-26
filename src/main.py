from pathlib import Path
from src.car import Car
from src.circuit import Circuit
from src.simulator import LapSimulator
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

car = Car()
circuit = Circuit(DATA / "circuit.json")

sim = LapSimulator(car, circuit)
x, v, lap_time = sim.simulate()

print(f"Lap time: {lap_time:.2f} s")

plt.plot(x, v)
plt.xlabel("Distance (m)")
plt.ylabel("Speed (m/s)")
plt.title("Speed profile over lap")
plt.show()
