import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

class ResourceIdentifier:
    def __init__(self, config_file='resources.json'):
        try:
            with open(config_file, 'r') as file:
                self.config = json.load(file)
            logging.info("Configuration loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            raise e

        # Build dictionaries from the configuration.
        self.asteroid_rock_values = {
            rock: (data["value"], data["color"], data["resources"])
            for rock, data in self.config["asteroid_rock_values"].items()
        }
        self.planet_rock_values = {
            rock: (data["value"], data["color"], data["resources"])
            for rock, data in self.config["planet_rock_values"].items()
        }
        self.special_cases = self.config["special_cases"]

    def validate_rs_signature(self, rs_signature):
        if not isinstance(rs_signature, int) or rs_signature < 0:
            raise ValueError("RS signature must be a non-negative integer")
        return True
## Add color to certain text. This just selects the text. 
## Define the color in style.css under Resource Color Classes
    def colorize_resources(self, text):
        """Wrap specific resource names in HTML span tags for colorization."""
        replacements = {
            "Quantanium": "<span class='quantanium'>Quantanium</span>",
            "Taranite": "<span class='taranite'>Taranite</span>",
            "Bexalite": "<span class='bexalite'>Bexalite</span>",
            "Hadanite": "<span class='hadanite'>Hadanite</span>",
            "Gold": "<span class='gold'>Gold</span>"
        }
        for original, colored in replacements.items():
            text = text.replace(original, colored)
        return text

    def identify_resource(self, rs_signature, mining_location):
        """Identify the resource(s) based on the RS signature and mining location."""
        try:
            self.validate_rs_signature(rs_signature)
        except ValueError as ve:
            logging.error(f"Validation error: {ve}")
            return str(ve)

        if mining_location == 'Asteroid':
            rock_values = self.asteroid_rock_values
        elif mining_location == 'Planet':
            rock_values = self.planet_rock_values
        else:
            return "Invalid mining location. Please specify 'Asteroid' or 'Planet'."

        # Special cases
        if rs_signature % self.special_cases["derelict_ship"] == 0:
            logging.info("Identified as Derelict Ship(s).")
            result = [("Derelict Ship", rs_signature // self.special_cases["derelict_ship"], "")]
        elif rs_signature % self.special_cases["hull_plates"] == 0:
            logging.info("Identified as Hull Plates.")
            result = [("Hull Plates", rs_signature // self.special_cases["hull_plates"], "")]
        elif rs_signature % self.special_cases["gems"] == 0:
            num_gems = rs_signature // self.special_cases["gems"]
            gem_list = "\n".join(self.special_cases["gem_types"])
            logging.info("Identified as Gems.")
            result = [("Gems", num_gems, gem_list)]
        else:
            # Check for single rock type clusters
            result = None
            for rock_name, (rock_value, color, resources) in rock_values.items():
                if rs_signature % rock_value == 0:
                    num_rocks = rs_signature // rock_value
                    logging.info(f"Identified as {rock_name} (single type).")
                    result = [(rock_name, num_rocks, resources)]
                    break
            if result is None:
                # Check for mixed clusters (simple version)
                possible_rock_combinations = []
                seen_combinations = set()
                for rock_name1, (rock_value1, color1, resources1) in rock_values.items():
                    for rock_name2, (rock_value2, color2, resources2) in rock_values.items():
                        if rock_name1 != rock_name2:
                            for num_rock1 in range(1, rs_signature // rock_value1 + 1):
                                remaining_rs = rs_signature - (num_rock1 * rock_value1)
                                if remaining_rs % rock_value2 == 0:
                                    num_rock2 = remaining_rs // rock_value2
                                    combo = sorted([
                                        (rock_name1, num_rock1, resources1),
                                        (rock_name2, num_rock2, resources2)
                                    ])
                                    combo_key = tuple(combo)
                                    if combo_key not in seen_combinations:
                                        seen_combinations.add(combo_key)
                                        possible_rock_combinations.append(combo)
                                    break
                    if possible_rock_combinations:
                        break  # Exit early if a valid combination is found
                if possible_rock_combinations:
                    logging.info("Identified mixed rock cluster.")
                    result = possible_rock_combinations[0]
                else:
                    logging.warning("RS signature did not match any known pattern.")
                    result = "Unknown RS signature"

        # If the result is a list, colorize the resource text
        if isinstance(result, list):
            new_result = []
            for rock_name, num_rocks, resources in result:
                colored_resources = self.colorize_resources(resources)
                new_result.append((rock_name, num_rocks, colored_resources))
            return new_result

        return result

if __name__ == "__main__":
    ri = ResourceIdentifier()
    print(ri.identify_resource(3400, "Asteroid"))
