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
            
            if seg["type"] == "straight":
                n = int(seg["length"] / self.dx)
                for _ in range(n):
                    self.x.append(pos)
                    self.v_max.append(304.0/3.6)   # vitesse max de 304 km/h obtenue après simulation
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
        v_cible = self.v_max
        v = np.zeros(n)
        v[0] = 0.0  
        courbe_batterie = n*[self.car.E_battery]


        # modèle accausal pour obtenir un profil de vitesse cible
        # Passe arrière : freinage
        for i in reversed(range(n-1)):
            v_brake = np.sqrt(self.v_max[i+1]**2 + 2 * self.mu * self.g * self.dx)
            v_cible[i] = min(self.v_max[i], v_brake)

        # 2e résolution prenant en compte puissance moteur
        for i in range(n-1):
            dv = v_cible[i+1]-v[i]

            if dv >= 0 :  # on ne va pas aussi vite que l'on voudrait
                a = self.car.acceleration(v[i])
                v[i+1] = np.sqrt(max(0, v[i]**2 + 2 * a * self.dx))
                
                # on met à jour les caractéristiques de la voiture
                self.car.vitesse = self.car.boite_vitesse(v[i])
                self.car.decharge_battery(v[i],ds=1.0)
                courbe_batterie[i] = self.car.E_battery

            else : # on souhaite ralentir
                v[i+1] = v[i] + dv # on suppose que l'on a la capacité de ralentir grâce à la passe arrière

                self.car.vitesse = self.car.boite_vitesse(v[i])
                self.car.charge_battery(v[i],dv,ds=1.0) # dans la fonction, dv peut etre positif et negatif, la valeur absolue l'ecrase
                courbe_batterie[i] = self.car.E_battery



        # Temps
        dt = self.dx / np.maximum(v, 1.0)   # vitesse minimale = 1 m/s
        t = np.cumsum(dt)
        total_time = t[-1]

        # Accélération
        a = np.zeros_like(v)
        a[1:] = (v[1:] - v[:-1]) / dt[1:]
        a[0] = a[1]

        return t, self.x, v, v_cible, total_time, dt, a, courbe_batterie

    
    