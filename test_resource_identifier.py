import unittest
from resource_identifier import ResourceIdentifier

class TestResourceIdentifier(unittest.TestCase):
    def setUp(self):
        self.res_identifier = ResourceIdentifier()

    def test_derelict_ship(self):
        # For a signature that is exactly a multiple of derelict_ship (10000)
        result = self.res_identifier.identify_resource(20000, "Asteroid")
        self.assertEqual(result, [("Derelict Ship", 2, "")])

    def test_hull_plates(self):
        # For a signature that is a multiple of hull_plates (2000) but not derelict_ship
        result = self.res_identifier.identify_resource(12000, "Planet")
        self.assertEqual(result, [("Hull Plates", 6, "")])

    def test_gems(self):
        result = self.res_identifier.identify_resource(620, "Asteroid")
        gem_text = "\n".join(self.res_identifier.special_cases["gem_types"])
        self.assertEqual(result, [("Gems", 1, gem_text)])

    def test_invalid_mining_location(self):
        result = self.res_identifier.identify_resource(1700, "Moon")
        self.assertEqual(result, "Invalid mining location. Please specify 'Asteroid' or 'Planet'.")

    def test_unknown_signature(self):
        # Assuming an RS signature that does not match any known pattern
        result = self.res_identifier.identify_resource(1234, "Asteroid")
        self.assertEqual(result, "Unknown RS signature")

    def test_mixed_cluster_asteroid(self):
        # For asteroid, using RS signature 3420 = 1700 (C Type) + 1720 (S Type)
        result = self.res_identifier.identify_resource(3420, "Asteroid")
        # Expected combination (sorted alphabetically by rock type)
        expected = sorted([
            ("C Type", 1, self.res_identifier.asteroid_rock_values["C Type"][2]),
            ("S Type", 1, self.res_identifier.asteroid_rock_values["S Type"][2])
        ])
        self.assertEqual(result, expected)

    def test_mixed_cluster_planet(self):
        # For planet, using RS signature 3530 = 1800 (Atacamite) + 1730 (Shale)
        result = self.res_identifier.identify_resource(3530, "Planet")
        expected = sorted([
            ("Atacamite", 1, self.res_identifier.planet_rock_values["Atacamite"][2]),
            ("Shale", 1, self.res_identifier.planet_rock_values["Shale"][2])
        ])
        self.assertEqual(result, expected)

if __name__ == '__main__':
    # Run tests with verbosity 2
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestResourceIdentifier)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\nAll tests passed successfully!")
    else:
        print("\nSome tests failed!")
    input("Press Enter to exit...")
