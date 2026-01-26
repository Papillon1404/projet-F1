import math 

class Car :

    def __init__(self,
        mass=800,
        power=750_000,
        cd=0.9,
        area=1.5,
        rho=1.225
    ):
        self.mass = mass
        self.power = power
        self.cd = cd
        self.area = area
        self.rho = rho

    def drag_force(self,v):
        return 0.5 * self.rho * self.cd * self.area * v**2
    
    def engine_force(self, v):
        v = max(v,1.0) # éviter division par zéro
        return self.power / v

    def acceleration(self,v): 
        F_motor = self.engine_force(v)
        F_drag = self.drag_force(v)

        return (F_motor - F_drag)/self.mass
    

