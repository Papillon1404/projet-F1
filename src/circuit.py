import json
from pathlib import Path
from math import pi,cos,sin,radians
import numpy as np
import matplotlib as plt

class Circuit :

    def __init__(self,json_path) :
        self.json_path = Path(json_path)
        self.name = None
        self.segments = []

        self.load()
    
    def load(self) :
        with open(self.json_path,"r") as f :
            data = json.load(f)

            self.name = data["name"]
            self.segments = data["segments"]

    def total_length(self):
        length = 0.0
        for seg in self.segments : 
            if seg["type"] == "Straight" :
                length += seg["length"]
            elif seg["type"] == "Turn" :
                length += seg["radius"]*pi*seg["angle"]/180
        
        return length
    
    def describe(self) :
        print(f"Circuit : {self.name}")
        for i , seg in enumerate(self.segments):
            print(f" Segments {i+1}: {seg}")



    def compute_xy(self, ds=1.0):
        """
        Compute (X, Y) coordinates of the circuit centerline
        """

        x, y = 0.0, 0.0
        theta = 0.0  # orientation (rad)

        X = [x]
        Y = [y]

        for seg in self.segments:

            # =====================
            # STRAIGHT
            # =====================
            if seg["type"].lower() == "straight":
                length = seg["length"]
                n = int(length / ds)

                for _ in range(n):
                    x += ds * cos(theta)
                    y += ds * sin(theta)
                    X.append(x)
                    Y.append(y)

            # =====================
            # TURN
            # =====================
            elif seg["type"].lower() == "turn":
                R = seg["radius"]
                angle = radians(seg["angle"])  # total angle
                arc_length = abs(R * angle)
                n = int(arc_length / ds)

                dtheta = angle / n

                for _ in range(n):
                    theta += dtheta
                    x += ds * cos(theta)
                    y += ds * sin(theta)
                    X.append(x)
                    Y.append(y)

            else:
                raise ValueError(f"Unknown segment type: {seg['type']}")
            X.append(X[-1])
            Y.append(Y[-1])
        return np.array(X), np.array(Y)

