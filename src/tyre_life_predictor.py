import numpy as np


class TyreLifePredictor:
    def __init__(self, min_grip=0.2):
        self.min_grip = min_grip
        self.compound_properties = {
            "soft": {"durability": 0.8, "temp_optimal": 85, "temp_range": (75, 95)},
            "medium": {"durability": 1.0, "temp_optimal": 90, "temp_range": (80, 100)},
            "hard": {"durability": 1.5, "temp_optimal": 95, "temp_range": (85, 105)},
        }

    def predict_life(
        self,
        base_grip,
        wear_rate,
        track_roughness=1.0,
        driving_style_factor=1.0,
        compound="medium",
        temperature=85,
    ):

        if wear_rate <= 0 or track_roughness <= 0 or driving_style_factor <= 0:
            raise ValueError("Wear rate, track roughness, and driving style factor must be greater than zero.")

        if compound not in self.compound_properties:
            raise ValueError(f"Unknown compound '{compound}'. Must be one of {list(self.compound_properties.keys())}.")

        # Get compound-specific properties
        compound_data = self.compound_properties[compound]
        durability = compound_data["durability"]
        temp_optimal = compound_data["temp_optimal"]
        temp_range = compound_data["temp_range"]

        # Adjust wear rate dynamically
        adjusted_wear_rate = wear_rate * track_roughness * driving_style_factor / durability

        # Penalty for being outside optimal temperature range
        if not (temp_range[0] <= temperature <= temp_range[1]):
            temp_penalty = 0.1 * abs(temperature - temp_optimal)
            adjusted_wear_rate += temp_penalty

        # Calculate tyre life
        predicted_life = (base_grip - self.min_grip) / adjusted_wear_rate

        # Introduce randomness to simulate variability
        stochastic_variation = np.random.uniform(0.95, 1.05)  # ±5% variation
        return int(predicted_life * stochastic_variation)

    def lap_by_lap_analysis(
        self,
        laps,
        base_grip,
        wear_rate,
        track_roughness=1.0,
        driving_style_factor=1.0,
        compound="medium",
        temperature=85,
    ):

        remaining_grip = base_grip
        grip_per_lap = []

        for lap in range(1, laps + 1):
            # Predict grip degradation for this lap
            lap_wear_rate = wear_rate * track_roughness * driving_style_factor / self.compound_properties[compound][
                "durability"
            ]

            # Apply temperature penalty
            if not (self.compound_properties[compound]["temp_range"][0] <= temperature <= self.compound_properties[compound]["temp_range"][1]):
                lap_wear_rate += 0.1 * abs(temperature - self.compound_properties[compound]["temp_optimal"])

            # Decrease grip and append
            remaining_grip -= lap_wear_rate
            remaining_grip = max(remaining_grip, 0)  # Ensure grip doesn't go below 0
            grip_per_lap.append(remaining_grip)

            # Break if grip drops below minimum
            if remaining_grip <= self.min_grip:
                break

        return grip_per_lap


if __name__ == "__main__":
    predictor = TyreLifePredictor(min_grip=0.2)

    tyre_life = predictor.predict_life(
        base_grip=1.0,
        wear_rate=0.015,
        track_roughness=1.2,
        driving_style_factor=1.1,
        compound="soft",
        temperature=90,
    )
    print(f"Predicted tyre life: {tyre_life} laps")

    lap_grip = predictor.lap_by_lap_analysis(
        laps=50,
        base_grip=1.0,
        wear_rate=0.015,
        track_roughness=1.2,
        driving_style_factor=1.1,
        compound="soft",
        temperature=90,
    )
    print("Lap-by-lap grip levels:")
    print(lap_grip)
