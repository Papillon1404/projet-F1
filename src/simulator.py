import numpy as np
import math

class LapSimulator:
    
    def __init__(self,car,circuit,mu=1.7,g=9.81,dx=1.0):

        self.car = car
        self.circuit = circuit
        self.mu = mu
        self.g = g
        self.dx = dx


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

        n = len(self.x)
        v = np.zeros(n)
        v[0] = 1.0  # vitesse minimale réaliste

        # Passe avant : accélération
        for i in range(1, n):
            a = self.car.acceleration(v[i-1])
            v_new = np.sqrt(max(0, v[i-1]**2 + 2 * a * self.dx))
            v[i] = min(v_new, self.v_max[i])

        # Passe arrière : freinage
        for i in reversed(range(n-1)):
            v_brake = np.sqrt(v[i+1]**2 + 2 * self.mu * self.g * self.dx)
            v[i] = min(v[i], v_brake)

        # Temps
        dt = self.dx / np.maximum(v, 1.0)   # vitesse minimale = 1 m/s
        t = np.cumsum(dt)
        total_time = t[-1]

        # Accélération
        a = np.zeros_like(v)
        a[1:] = (v[1:] - v[:-1]) / dt[1:]
        a[0] = a[1]

        return t, self.x, v, total_time, dt, a

    
    