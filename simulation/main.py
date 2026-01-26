from circuit import Circuit

circuit = Circuit("/projet-F1/data/circuit.json")
circuit.describe()
print(f"Total length: {circuit.total_length():.1f} m")
