from random import shuffle

class GameState:
    def __init__(self):
        self.players = []
        humans = input("How many human players?")
        comps = input("How many computer players?")
        for i in range(humans):
            self.players.append(Player(input(f"Player {len(self.players) + 1}, what is your name? "), (0, 0)))
        for j in range(comps):
            self.players.append(ComputerPlayer(f"Computer {j + 1}", (0, 0)))
        shuffle(self.players)
        self.cp = 0
    
    def turn(self):
        p1 = self.players[self.cp]
        p2 = self.players[(self.cp + 1) % 1]
        p1.pick_location()
        p1.shoot()
        if self.do_outcome(p1, p2) == 'switch':
            

    def do_outcome(self, player1, player2):
        if player1.shot == False:
            return 'switch'
        elif player2.shot == None:
            return
        elif player1.shot and not player2.shot:
            return 'score'
        elif player1.shot and player2.shot:
            return 'pass'
        else:
            raise ValueError("Invalid game status")



class Player:
    def __init__(self, name, location):
        self.loc = location
        self.name = name
    
    def shoot(self):
        if self.result(self.loc.a, self.loc):
            print("You made the shot!")
            do_outcome("some arguments")
        else:
            print("Bad shot")
            do_outcome("some arguments")
    
    def pick_location(self):
        return

class ComputerPlayer(Player):
    def pick_location(self):
        return ai_logic()