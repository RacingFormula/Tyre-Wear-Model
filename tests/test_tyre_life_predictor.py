import unittest
from src.tyre_life_predictor import TyreLifePredictor

class TestTyreLifePredictor(unittest.TestCase):
    def setUp(self):
        # Create an instance of TyreLifePredictor with default min_grip
        self.predictor = TyreLifePredictor(min_grip=0.2)

    def test_predict_life_valid_input(self):
        # Test valid inputs for tyre life prediction
        self.assertEqual(self.predictor.predict_life(base_grip=1.0, wear_rate=0.02), 40)
        self.assertEqual(self.predictor.predict_life(base_grip=0.8, wear_rate=0.02), 30)
        self.assertEqual(self.predictor.predict_life(base_grip=1.0, wear_rate=0.05), 16)

    def test_predict_life_edge_case(self):
        # Test edge case where tyre is almost worn at start
        self.assertEqual(self.predictor.predict_life(base_grip=0.25, wear_rate=0.05), 1)

    def test_predict_life_invalid_wear_rate(self):
        # Test for invalid wear rate (should raise an exception)
        with self.assertRaises(ValueError):
            self.predictor.predict_life(base_grip=1.0, wear_rate=0)

    def test_predict_life_invalid_grip(self):
        # Test for invalid base_grip and min_grip combination
        self.predictor.min_grip = 1.1  # Set min_grip higher than base_grip
        with self.assertRaises(ValueError):
            self.predictor.predict_life(base_grip=1.0, wear_rate=0.02)

if __name__ == "__main__":
    unittest.main()
