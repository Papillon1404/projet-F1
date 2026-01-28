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

t, x, v, v_cible, lap_time, time_per_segment ,a , courbe_batterie, vitesses_au_cours_du_temps, rpm = sim.simulate()
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
fig, (ax_speed, ax_acc,ax_batt, ax_gear, ax_track) = plt.subplots(
    5, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [2, 2, 2, 2, 3]}
)


# vitesse
line_v, = ax_speed.plot([], [], lw = 2)
line_v_cible, = ax_speed.plot([], [], linestyle = "--",color="orange")
ax_speed.set_xlim(0, t[-1])
ax_speed.set_ylim(0, v.max()*3.6*1.1)
ax_speed.set_ylabel("Speed (km/h)")

# accélération
line_a, = ax_acc.plot([], [], color = "red")
ax_acc.set_xlim(0, t[-1])
ax_acc.set_ylim(-25, 25)
ax_acc.set_ylabel("Acceleration (m/s²)")

# batterie
line_b, = ax_batt.plot([], [], color = "green")
ax_batt.set_xlim(0, t[-1])
ax_batt.set_ylim(min(courbe_batterie) - 0.2 * max(courbe_batterie), max(courbe_batterie)*1.2)
ax_batt.set_ylabel("capacité de la batterie (Wh)")

# boite de vitesse
line_rapp, = ax_gear.plot([], [], color = "black")
ax_gear.set_xlim(0, t[-1])
ax_gear.set_ylim(0,9)
ax_gear.set_ylabel("vitesse")

ax_gear2 = ax_gear.twinx()
line_rpm, = ax_gear2.plot([], [], color = "red")
ax_gear2.set_xlim(0, t[-1])
ax_gear2.set_ylim(0, 3_000)
ax_gear2.set_ylabel("Rpm (tr/min)")



# circuit
ax_track.plot(X, Y, color="black")
car_dot, = ax_track.plot([], [], "ro", markersize=6)
ax_track.axis("equal")
ax_track.set_title("Circuit Layout")



def update(i):
    line_v.set_data(t[:i], v[:i]*3.6)
    line_v_cible.set_data(t[:i], v_cible[:i]*3.6)
    line_a.set_data(t[:i], a[:i])
    line_b.set_data(t[:i], courbe_batterie[:i])
    line_rapp.set_data(t[:i], vitesses_au_cours_du_temps[:i])
    line_rpm.set_data(t[:i], rpm[:i])

    car_dot.set_data([car_X[i]], [car_Y[i]])


    return line_v, line_v_cible, line_a, line_b, line_rapp, line_rpm, car_dot



### animation ######################################################################################

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


##### controle de bug #############################################################################

