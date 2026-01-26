import numpy as np
import math

class LapSimulator:
    
    def __init__(self,car,circuit,mu=1.7,g=9.81,dt_target=0.02):
        self.car = car
        self.circuit = circuit
        self.mu = mu
        self.g = g
        self.dt_target = dt_target  # pas temporel cible

        self.x =[]
        self.v_max = []

        self._discreticize_circuit()

    
    def _discreticize_circuit(self):
        pos = 0.0

        for seg in self.circuit.segments :
            
            if seg["type"] == "Straight":
                n = int(seg["length"] / self.dx)
                for _ in range(n):
                    self.x.append(pos)
                    self.v_max.append(np.inf)
                    pos+=self.dx

            elif seg["type"] == "turn":
                arc = math.radians(seg["angle"]) * seg["radius"]
                n = int(arc /self.dx)
                vmax_turn = math.sqrt(self.mu * self.g * seg["radius"])

                for _ in range(n):
                    self.x.append(pos)
                    self.v_max.append(vmax_turn)
                    pos += self.dx

        self.x = np.array(self.x)
        self.v_max = np.array(self.v_max)

    def simulate(self):
        x_sim = [0.0]           # position curviligne
        v_sim = [1.0]           # vitesse initiale 1 m/s pour éviter dt énorme
        dt_list = [0.0]         # temps cumulé initial
        a_list = []             # accélération

        
        v = np.zeros(len(self.x))

        #Passe avant : accélération
        for i in range(1,len(v)):
            a = self.car.acceleration(v[i-1])
            dx = max(v[i-1] * self.dt_target, 0.01)
            v[i] = np.sqrt(max(0,v[i-1]**2 + 2 * a * dx))
            v[i] = min(v[i], self.v_max[i])
        

        #Passe arriere : freinage
        for i in reversed(range(len(v)-1)):
            dx = max(v[i-1] * self.dt_target, 0.01)
            v_brake = np.sqrt(v[i+1]**2 + 2 * self.mu * self.g * self.dx)
            v[i] = min(v[i], v_brake)

        dt = self.dx / np.maximum(v, 1e-3)
        total_time = np.sum(dt)


        time_per_segment = dx / np.maximum(v, 1e-3)
        t = np.cumsum(np.concatenate([[0], time_per_segment]))
        a = np.gradient(v, time_per_segment)

        return t, self.x, v, total_time, time_per_segment, a
    
    