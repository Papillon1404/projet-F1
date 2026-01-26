import json
from pathlib import Path
from math import pi

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


