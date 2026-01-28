import math 

class Car :

    def __init__(self,
        mass=800,
        power_therm=400_000, # en W
        power_elec=350_000,  # en W
        cd=0.9,   # dépend de la voiture et du circuit mai autour de 1
        area=1.5,
        rho=1.225,
        capacity = 5_000, # en Wh
        tension = 9_000, # en V
        rendement_charge_decharge = 0.9, # 90 à 95%
        rendement_onduleur = 0.95,  # 95 à 98%
        w_pmax = 1100, # vitesse angulaire à partir de laquelle la puissance moteur elec chute (valeur prise pour englober une partie du plateau de puissance thermique)
        rayon = 0.720, #  rayon des pneus pirellis arriere e(n m)
        rapports = [14.0,11,9,7.5,6.3,5.4,4.7,4.1]
    ):
        self.mass = mass
        self.power_therm = power_therm
        self.power_elec = power_elec
        self.cd = cd
        self.area = area
        self.rho = rho
        self.capacity = capacity
        self.tension = tension
        self.rendement_charge_decharge = rendement_charge_decharge
        self.rendement_onduleur = rendement_onduleur
        self.w_pmax = w_pmax
        self.rayon = rayon

    
        self.E_battery = self.capacity # on initialise batterie chargée
        self.vitesse = 1 # premiere vitesse
        self.rapports = rapports
    
    
    
    # fonction modélisant la boite de vitesse
    def boite_vitesse(self,v):   
   
        w = v/(self.rayon * self.rapports[self.vitesse-1]) 
        
        # passe la vitesse supérieur
        if w >= 1257 and self.vitesse < 8:    # 12_000 tr/min
            return self.vitesse + 1 
        elif w <= 942 and self.vitesse > 1:   # # 9_000 tr/min
            return self.vitesse - 1
        else : 
            return self.vitesse 
            
        


    # évolution de la batterie

    def charge_battery(self, v, dv, ds=1.0):
        # dt = distance / vitesse
        dt = ds / max(v, 1.0)
        
        P = self.m * v * abs(dv)
        
        dE = + P * self.rendement_charge_decharge * dt/3600.0 # conversion en Wh
        self.E_battery = min(self.capacity, max(0, self.E_battery + dE))

    def decharge_battery(self, v, ds=1.0):
        # dt = distance / vitesse
        dt = ds / max(v, 1.0)

        P = self.P_MGU_K(v)

        dE = - P * self.rendement_charge_decharge * dt/3600.0 # conversion en Wh
        self.E_battery = min(self.capacity, max(0, self.E_battery + dE))


    # puissance electrique
    def P_MGU_K(self,v):
        w = v/(self.rayon * self.rapports[self.vitesse-1]) # on divise par le rapport de la boite de vitesse
        
        if self.E_battery > 0 :
            if w <= self.w_pmax :
                return self.power_elec
        
            else :
                return self.power_elec * self.w_pmax/w   # courbe inverse de w
        else :
            return 0

    # puissance thermique
    def P_ICE(self,v): 
        w = v/(self.rayon * self.rapports[self.vitesse-1]) 

        if w <= 1047 : # en rad/s equivaut à 10_000 tr/min
            return 0.5 * self.power_therm * (1+ w/1047) # fonction affine qui commence à 1/2 de P_max
        
        elif w <= 1257 : # en rad/s equivaut à 12_000 tr/min
            return self.power_therm     # puissance max entre 10 000 et 12 000 tr/min
        
        else :    # chute de puissance au delà du plateau
            return self.power_therm * 1257/w # courbe inverse de w





    # mécanique de la voiture

    def drag_force(self,v):
        return 0.5 * self.rho * self.cd * self.area * v**2
    
    def engine_force(self, v):
        power = self.P_ICE(v) + self.P_MGU_K(v)
        v = max(v, 1.0)
        F_power = power / v
        return F_power

    def acceleration(self,v): 
        F_motor = self.engine_force(v)
        F_drag = self.drag_force(v)

        return (F_motor - F_drag)/self.mass


    def max_braking(self, v, mu=1.7, g=9.81):
        return mu * g * self.grip_factor(v)
    
    def grip_factor(self, v):
        return 1.0 + 0.002 * v**2

    

