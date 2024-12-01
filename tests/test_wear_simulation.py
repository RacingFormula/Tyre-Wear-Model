import unittest
from src.wear_simulation import TyreWearModel


class TestTyreWearModel(unittest.TestCase):
    def setUp(self):
        # Create an instance of TyreWearModel with default parameters
        self.model = TyreWearModel(base_grip=1.0, wear_rate=0.02, track_roughness=1.0, temperature_effect=0.005)

    def test_calculate_grip_no_wear(self):
        # Test grip calculation with no wear
        grip = self.model.calculate_grip(lap=0, speed_factor=1.0, braking_factor=0.0, compound="medium")
        self.assertAlmostEqual(grip, 1.0, places=3)

    def test_calculate_grip_with_wear(self):
        # Test grip calculation after 10 laps
        grip = self.model.calculate_grip(lap=10, speed_factor=1.0, braking_factor=0.2, compound="medium")
        self.assertLess(grip, 1.0)  # Grip should decrease

    def test_calculate_grip_with_temperature_penalty(self):
        # Test grip calculation with temperature penalty
        self.model.tyre_temperature = 110  # Overheat scenario
        grip = self.model.calculate_grip(lap=5, speed_factor=1.0, braking_factor=0.2, compound="medium")
        self.assertLess(grip, 1.0)  # Grip should be reduced due to high temperature

    def test_calculate_grip_below_minimum(self):
        # Test grip doesn't go below zero
        grip = self.model.calculate_grip(lap=100, speed_factor=1.0, braking_factor=0.5, compound="medium")
        self.assertEqual(grip, 0.0)

    def test_calculate_grip_with_different_compounds(self):
        # Test grip calculation for different compounds
        soft_grip = self.model.calculate_grip(lap=5, speed_factor=1.0, braking_factor=0.2, compound="soft")
        hard_grip = self.model.calculate_grip(lap=5, speed_factor=1.0, braking_factor=0.2, compound="hard")
        self.assertGreater(soft_grip, hard_grip)  # Soft tyres should provide more grip

    def test_invalid_compound(self):
        # Test invalid compound input
        with self.assertRaises(KeyError):
            self.model.calculate_grip(lap=5, speed_factor=1.0, braking_factor=0.2, compound="invalid")

    def test_calculate_energy_loss(self):
        # Test energy loss calculation
        energy_loss = self.model.calculate_energy_loss(lap_speed=200, cornering_load=0.5)
        self.assertGreater(energy_loss, 0)  # Energy loss should be positive
        self.assertAlmostEqual(energy_loss, 12.5)  # 0.015 * 200 (rolling resistance) + 0.05 * 0.5 * 200 (lateral loss)

    def test_temperature_cooling_effect(self):
        # Test cooling effect during slow laps
        self.model.tyre_temperature = 90  # Initial temperature
        self.model.calculate_grip(lap=5, speed_factor=0.5, braking_factor=0.2, compound="medium")  # Slow lap
        self.assertLess(self.model.tyre_temperature, 90)  # Tyre temperature should decrease

    def test_temperature_heating_effect(self):
        # Test heating effect during fast laps
        self.model.tyre_temperature = 25  # Initial temperature
        self.model.calculate_grip(lap=5, speed_factor=1.0, braking_factor=0.2, compound="medium")  # Fast lap
        self.assertGreater(self.model.tyre_temperature, 25)  # Tyre temperature should increase


if __name__ == "__main__":
    unittest.main()
