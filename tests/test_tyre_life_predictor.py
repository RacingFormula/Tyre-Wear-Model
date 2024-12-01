import unittest
from src.tyre_life_predictor import TyreLifePredictor


class TestTyreLifePredictor(unittest.TestCase):
    def setUp(self):
        # Create an instance of TyreLifePredictor with default min_grip
        self.predictor = TyreLifePredictor(min_grip=0.2)

    def test_predict_life_valid_input(self):
        # Test valid inputs for tyre life prediction
        self.assertEqual(
            self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="medium", temperature=90),
            40
        )
        self.assertEqual(
            self.predictor.predict_life(base_grip=0.8, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="medium", temperature=90),
            30
        )

    def test_predict_life_compound_specific(self):
        # Test compound-specific predictions
        self.assertGreater(
            self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="hard", temperature=90),
            self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="soft", temperature=90),
        )

    def test_predict_life_temperature_penalty(self):
        # Test for temperature effects on tyre life
        high_temp_life = self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="medium", temperature=110)
        optimal_temp_life = self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="medium", temperature=90)
        low_temp_life = self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="medium", temperature=70)

        self.assertLess(high_temp_life, optimal_temp_life)
        self.assertLess(low_temp_life, optimal_temp_life)

    def test_predict_life_invalid_wear_rate(self):
        # Test for invalid wear rate (should raise an exception)
        with self.assertRaises(ValueError):
            self.predictor.predict_life(base_grip=1.0, wear_rate=0, track_roughness=1.0, driving_style_factor=1.0, compound="medium", temperature=90)

    def test_predict_life_invalid_compound(self):
        # Test for an invalid compound name
        with self.assertRaises(ValueError):
            self.predictor.predict_life(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, driving_style_factor=1.0, compound="unknown", temperature=90)

    def test_lap_by_lap_analysis(self):
        # Test lap-by-lap grip degradation analysis
        grip_levels = self.predictor.lap_by_lap_analysis(
            laps=10,
            base_grip=1.0,
            wear_rate=0.02,
            track_roughness=1.0,
            driving_style_factor=1.0,
            compound="medium",
            temperature=90,
        )
        self.assertEqual(len(grip_levels), 10)
        self.assertTrue(all(g1 >= g2 for g1, g2 in zip(grip_levels, grip_levels[1:])))  # Ensure grip decreases each lap

    def test_grip_below_min(self):
        # Ensure the lap-by-lap simulation stops when grip is below minimum
        grip_levels = self.predictor.lap_by_lap_analysis(
            laps=50,
            base_grip=1.0,
            wear_rate=0.2,  # High wear rate to ensure rapid degradation
            track_roughness=1.0,
            driving_style_factor=1.0,
            compound="medium",
            temperature=90,
        )
        self.assertTrue(all(grip >= 0.2 for grip in grip_levels[:-1]))
        self.assertLess(grip_levels[-1], 0.2)  # Final lap should drop below min_grip

if __name__ == "__main__":
    unittest.main()
