class TyreLifePredictor:
    def __init__(self, min_grip=0.2):
        self.min_grip = min_grip

    def predict_life(self, base_grip, wear_rate):
        if wear_rate <= 0:
            raise ValueError("Wear rate must be greater than zero.")
        return int((base_grip - self.min_grip) / wear_rate)

if __name__ == "__main__":
    predictor = TyreLifePredictor(min_grip=0.2)
    tyre_life = predictor.predict_life(base_grip=1.0, wear_rate=0.015)
    print(f"Predicted tyre life: {tyre_life} laps")
