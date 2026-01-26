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
        F_max = 15_000  # N (ordre de grandeur)
        v = max(v, 1.0)
        F_power = self.power / v
        return min(F_max, F_power)

    def acceleration(self,v): 
        F_motor = self.engine_force(v)
        F_drag = self.drag_force(v)

        return (F_motor - F_drag)/self.mass


    def max_braking(self, v, mu=1.7, g=9.81):
        return mu * g * self.grip_factor(v)
    
    def grip_factor(self, v):
        return 1.0 + 0.002 * v**2

    

