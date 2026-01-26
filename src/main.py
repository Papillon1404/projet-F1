from car import Car
from circuit import Circuit
from simulator import LapSimulator
import matplotlib.pyplot as plt

car = Car()
circuit = Circuit("/projet-F1/data/circuit.json")


sim = LapSimulator(car, circuit)
x, v, lap_time = sim.simulate()

print(f"Lap time: {lap_time:.2f} s")

plt.plot(x, v)
plt.xlabel("Distance (m)")
plt.ylabel("Speed (m/s)")
plt.title("Speed profile over lap")
plt.show()
