import pandas as pd
import numpy as np

class TyreWearModel:
    def __init__(self, base_grip=1.0, wear_rate=0.02):
        self.base_grip = base_grip
        self.wear_rate = wear_rate

    def calculate_grip(self, laps):
        grip = max(self.base_grip - self.wear_rate * laps, 0)
        return grip

def simulate_tyre_wear(laps, base_grip=1.0, wear_rate=0.02):
    model = TyreWearModel(base_grip, wear_rate)
    lap_data = {"Lap": [], "Grip": []}

    for lap in range(1, laps + 1):
        lap_data["Lap"].append(lap)
        lap_data["Grip"].append(model.calculate_grip(lap))

    return pd.DataFrame(lap_data)

if __name__ == "__main__":
    laps = 50
    results = simulate_tyre_wear(laps, base_grip=1.0, wear_rate=0.015)
    print(results)
