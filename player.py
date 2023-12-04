class Player:
    def __init__(self, name, location):
        self.loc = location
        self.name = name
    
    def pick_location(self):
        return

class ComputerPlayer(Player):
    def pick_location(self):
        return ai_logic()