class Player:
    def __init__(self, name, location, height, skill):
        self.loc = location
        self.name = name
        self.height = height
        self.skill = skill
    
    def pick_location(self):
        return

class ComputerPlayer(Player):
    def pick_location(self):
        return ai_logic()