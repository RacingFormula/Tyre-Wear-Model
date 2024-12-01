import pandas as pd
import numpy as np


class TyreWearModel:
    def __init__(self, base_grip=1.0, wear_rate=0.02, track_roughness=1.0, temperature_effect=0.005):
        self.base_grip = base_grip
        self.wear_rate = wear_rate
        self.track_roughness = track_roughness
        self.temperature_effect = temperature_effect
        self.tyre_temperature = 25  # Default starting temperature in °C
        self.compound_properties = {
            "soft": {"grip": 1.2, "durability": 0.8, "temp_optimal": 85, "temp_range": (75, 95)},
            "medium": {"grip": 1.0, "durability": 1.0, "temp_optimal": 90, "temp_range": (80, 100)},
            "hard": {"grip": 0.8, "durability": 1.5, "temp_optimal": 95, "temp_range": (85, 105)},
        }

    def calculate_grip(self, lap, speed_factor, braking_factor, compound="medium"):
        compound_data = self.compound_properties[compound]
        compound_grip = compound_data["grip"]
        compound_durability = compound_data["durability"]

        # Adjust wear rate dynamically
        adjusted_wear_rate = (
            self.wear_rate * self.track_roughness * (1 + 0.1 * braking_factor) / compound_durability
        )

        # Simulate temperature effect
        temp_penalty = self.temperature_effect * abs(self.tyre_temperature - compound_data["temp_optimal"])

        # Non-linear degradation curve
        grip_loss = adjusted_wear_rate * (lap ** 0.8) + temp_penalty

        # Cooling during slower laps (safety car effect)
        if speed_factor < 0.7:
            self.tyre_temperature = max(self.tyre_temperature - 5, 25)
        else:
            self.tyre_temperature += 2  # Heat up during faster laps

        return max(self.base_grip * compound_grip - grip_loss, 0)

    def calculate_energy_loss(self, lap_speed, cornering_load):
        rolling_resistance = 0.015 * lap_speed
        lateral_loss = 0.05 * cornering_load * lap_speed
        return rolling_resistance + lateral_loss


def simulate_advanced_tyre_wear(
    laps, compound="medium", track_roughness=1.0, temperature_effect=0.005
):
    model = TyreWearModel(track_roughness=track_roughness, temperature_effect=temperature_effect)
    lap_data = {"Lap": [], "Grip": [], "Temperature": [], "Energy Loss (kJ)": []}

    for lap in range(1, laps + 1):
        speed_factor = np.random.uniform(0.8, 1.0)
        braking_factor = np.random.uniform(0.1, 0.5)
        cornering_load = np.random.uniform(0.5, 1.0)
        lap_speed = np.random.uniform(150, 220)  # Average lap speed in km/h

        grip = model.calculate_grip(lap, speed_factor, braking_factor, compound)
        temp = model.tyre_temperature
        energy_loss = model.calculate_energy_loss(lap_speed, cornering_load)

        lap_data["Lap"].append(lap)
        lap_data["Grip"].append(grip)
        lap_data["Temperature"].append(temp)
        lap_data["Energy Loss (kJ)"].append(energy_loss)

    return pd.DataFrame(lap_data)


if __name__ == "__main__":
    laps = 50
    results = simulate_advanced_tyre_wear(laps, compound="soft", track_roughness=1.2, temperature_effect=0.005)
    print(results)