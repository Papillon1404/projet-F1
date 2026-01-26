from pathlib import Path
from src.car import Car
from src.circuit import Circuit
from src.simulator import LapSimulator
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

car = Car()
circuit = Circuit(DATA / "circuit.json")

sim = LapSimulator(car, circuit)
x, v, lap_time, time_per_segment = sim.simulate()
v_min = np.min(v)
v_max = np.max(v)


# print 
print(f"Min speed: {v_min*3.6:.1f} km/h")
print(f"Max speed: {v_max*3.6:.1f} km/h")
print(f"Lap time: {lap_time:.2f} s")

# plot
plt.figure(figsize=(10,4))
plt.plot(x, v * 3.6)  # km/h
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.title("F1 Speed Profile Over Lap")
plt.grid(True)
plt.tight_layout()
plt.show()
