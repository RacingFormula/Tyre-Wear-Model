import unittest
from src.wear_simulation import TyreWearModel

class TestTyreWearModel(unittest.TestCase):
    def test_calculate_grip(self):
        model = TyreWearModel(base_grip=1.0, wear_rate=0.02)
        self.assertEqual(model.calculate_grip(0), 1.0)
        self.assertEqual(model.calculate_grip(10), 0.8)
        self.assertEqual(model.calculate_grip(50), 0.0)

if __name__ == "__main__":
    unittest.main()
