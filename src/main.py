from pathlib import Path
from src.car import Car
from src.circuit import Circuit
from src.simulator import LapSimulator
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.animation import FuncAnimation



ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

car = Car()
circuit = Circuit(DATA / "circuit.json")

sim = LapSimulator(car, circuit)
t, x, v, lap_time, time_per_segment ,a = sim.simulate()
v_min = np.min(v)
v_max = np.max(v)


X, Y = circuit.compute_xy(ds=1.0)
# Distance curviligne du circuit
ds_geom = np.sqrt(np.diff(X)**2 + np.diff(Y)**2)
s_geom = np.insert(np.cumsum(ds_geom), 0, 0.0)



interp_X = interp1d(s_geom, X, fill_value="extrapolate")
interp_Y = interp1d(s_geom, Y, fill_value="extrapolate")

car_X = interp_X(x)
car_Y = interp_Y(x)



### plot ###########################################################################################
fig, (ax_speed, ax_acc, ax_track) = plt.subplots(
    3, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [2, 2, 3]}
)


# vitesse
line_v, = ax_speed.plot([], [], lw=2)
ax_speed.set_xlim(0, 500)
ax_speed.set_ylim(0, v.max()*3.6*1.1)
ax_speed.set_ylabel("Speed (km/h)")

# accélération
line_a, = ax_acc.plot([], [], color="red")
ax_acc.set_xlim(0, 10000)
ax_acc.set_ylim(a.min()*1.2, a.max()*1.2)
ax_acc.set_ylabel("Acceleration (m/s²)")

# circuit
ax_track.plot(X, Y, color="black")
car_dot, = ax_track.plot([], [], "ro", markersize=6)
ax_track.axis("equal")
ax_track.set_title("Circuit Layout")



def update(i):
    line_v.set_data(t[:i], v[:i]*3.6)
    line_a.set_data(t[:i], a[:i])

    car_dot.set_data([car_X[i]], [car_Y[i]])


    return line_v, line_a, car_dot



### animation ######################################################################################
from matplotlib.animation import FuncAnimation

ani = FuncAnimation(
    fig,
    update,
    frames=len(x),
    interval=20,   # ms → ~50 FPS
    blit=True
)

plt.tight_layout()
plt.show()




# print 

print(f"Min speed: {v_min*3.6:.1f} km/h")
print(f"Max speed: {v_max*3.6:.1f} km/h")
print(f"Lap time: {lap_time:.2f} s")
print(f"Time lost in slow zones: {np.sum(time_per_segment[v < 50]):.2f} s")

print(f":{float(t[0])}")