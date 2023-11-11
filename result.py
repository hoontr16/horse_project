import random

class Player:
    def __init__(self, name, location, height, skill):
        self.loc = location
        self.name = name
        self.height = height
        self.skill = skill

    def result(self, angle, position):
        """Return True if the shot is made, False otherwise.

        args:
            angle (int): angle of the shot.
            position (str): position from which the shot is taken ("three-point", "mid-range", "lay-up", "free-throw").

        returns:
            bool: True if the shot is made, False otherwise.
        """
        base = 0.4

        position_bonuses = {
            "three-point": -0.05,
            "mid-range": 0.05,
            "lay-up": 1.0,
            "free-throw": 0.75
        }

        #gets the bonus based off of the position
        position_bonus = position_bonuses.get(position, 0.0)

        #bonus based on the player skill
        skill_bonus = 0 + self.skill 

        #total chance after considering factors
        total_probability = base + position_bonus + skill_bonus

        #adjusts probability based off of the angle
        if 40 <= angle <= 60:
            total_probability += 0.1
        else:
            total_probability += 0.0

        #ensures that the probability is between 0 and 1
        probability = min(1.0, total_probability)

        #if random float is less than probability, the result will be True, otherwise, it is false
        return random.random() < probability


