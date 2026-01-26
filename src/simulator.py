import numpy as np
import math

class LapSimulator:
    
    def __init__(self,car,circuit,mu=1.7,g=9.81,dx_ref=1.0,dt_target=0.02):
        self.car = car
        self.circuit = circuit
        self.mu = mu
        self.g = g
        self.dx_ref = dx_ref
        self.dt_target = dt_target  # pas temporel cible

        self.x =[]
        self.v_max = []

        self._discreticize_circuit()

    
    def _discreticize_circuit(self):
        pos = 0.0

        for seg in self.circuit.segments :
            
            if seg["type"] == "Straight":
                n = int(seg["length"] / self.dx_ref)
                for _ in range(n):
                    self.x.append(pos)
                    self.v_max.append(np.inf)
                    pos+=self.dx_ref

            elif seg["type"] == "turn":
                arc = math.radians(seg["angle"]) * seg["radius"]
                n = int(arc /self.dx_ref)
                vmax_turn = math.sqrt(self.mu * self.g * seg["radius"])

                for _ in range(n):
                    self.x.append(pos)
                    self.v_max.append(vmax_turn)
                    pos += self.dx_ref

        self.x = np.array(self.x)
        self.v_max = np.array(self.v_max)

    def simulate(self):
        v = np.zeros(len(self.x))
        dt_list = np.zeros(len(self.x))
    
        # Passe avant : accélération
        for i in range(1, len(v)):
            a = self.car.acceleration(v[i-1])
            dx = max(v[i-1] * self.dt_target, 0.01)
            v_new = np.sqrt(max(0, v[i-1]**2 + 2 * a * dx))
            v[i] = min(v_new, self.v_max[i])
            dt_list[i] = dx / max(v[i], 1e-2)

        # Passe arrière : freinage
        for i in reversed(range(len(v)-1)):
            dx = max(v[i] * self.dt_target, 0.01)
            v_brake = np.sqrt(v[i+1]**2 + 2 * self.mu * self.g * dx)
            v[i] = min(v[i], v_brake)
            dt_list[i] = dx / max(v[i], 1e-2)

        t = np.cumsum(dt_list)
        total_time = t[-1]

        # Accélération
        dv = np.diff(v)
        dx_arr = np.diff(self.x)
        dx_arr = np.where(dx_arr == 0, 1e-6, dx_arr)
        a = np.zeros_like(v)
        a[:-1] = dv / dx_arr
        a[-1] = a[-2]

        return t, self.x, v, total_time, dt_list, a

