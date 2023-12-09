from random import shuffle, choice, gauss, random
from math import atan2, exp, pi
import re
from time import sleep

class GameState:
    def __init__(self):
        self.players = []
        humans = int(input("How many human players? "))
        comps = int(input("How many computer players? "))
        for i in range(humans):
            self.players.append(HumanPlayer(len(self.players) + 1))
        for j in range(comps):
            self.players.append(ComputerPlayer(j + 1))
        shuffle(self.players)
        self.cp = 0
        self.p1 = self.players[self.cp]
        self.p2 = self.players[(self.cp + 1) % 2]        
    
    def turn(self):
        self.p1.shot, self.p2.shot = None, None
        self.p1 = self.players[self.cp]
        self.p2 = self.players[(self.cp + 1) % 2]
        self.p1.pick_location(grid, self.p2.score)
        self.p1.shoot()
        if self.outcome() == 'switch':
            self.p1 = self.players[self.cp]
            self.p2 = self.players[(self.cp + 1) % 2]            
            return
        self.p2.loc = self.p1.loc
        self.p2.shoot()
        self.outcome()

    def outcome(self):
        if self.p1.shot == False:
            self.cp = (self.cp + 1) % 2
            return 'switch'
        elif self.p2.shot == None:
            return
        elif self.p1.shot and not self.p2.shot:
            self.p2.score += 1
            return 'score'
        elif self.p1.shot and self.p2.shot:
            return 'pass'
        else:
            raise ValueError("Invalid game status")
        
    def check_win(self):
        if self.p1.score > 4:
            return self.p2
        elif self.p2.score > 4:
            return self.p1

class Player:
    def __init__(self, pnum):
        self.score = 0
        self.shot = None

    def shoot(self):
        print(f"{self.name} is taking their shot...")
        sleep(0.5)
        result = random() < self.loc.prob
        if result:
            print(f"{self.name} made the shot!")
            self.shot = True
        else:
            print("Bad shot")
            self.shot = False
            
class HumanPlayer(Player):
    def __init__(self, pnum):
        self.name = input(f"Player {pnum}, what is your name? ")
        super().__init__(self)
    
    def pick_location(self, probs, other_score):
        self.shot = None
        draw_court()
        a = input(f"{self.name}, where would you like to shoot from? ")
        r = r"^\(?(\d+)[\s,]+?(\d+)\)?$"
        match = re.search(r, a)
        while not match:
            print("Please enter in this format: x, y")
            a = input(f"{self.name}, where would you like to shoot from? ")
            match = re.search(r, a)
        c = find_coordinate(int(match[1]), int(match[2]))
        print("You will be shooting from here:")
        draw_court(c.pair)
        self.loc = c

class ComputerPlayer(Player):
    def __init__(self, pnum):
        super().__init__(self)
        self.name = f"Computer {pnum}"
        self.style = choice(styles)
        print(self.style)
        
    def pick_location(self, probs, other_score):
        """ Decide on a location for an AI player to shoot from, given the current
                game state.
        
        Arguments:
            probs (dict): coordinate objects and their shot probabilities.
            style (str): the AI's playing style
            my_score (int): the AI's current score
            other_score (int): the other player's current score
        
        Returns:
            Coordinate: the chosen position to shoot from.
        """
        if self.score - other_score < -2:
            my_style = 'risky'
        elif self.score - other_score > 2:
            my_style = 'safe'
        else:
            my_style = self.style
        if my_style == 'risky':
            locs_sorted = sorted([i for i in probs if i.prob * (1 - i.prob) > 0.15], key=lambda c: c.prob * (1 - c.prob))
            self.loc = get_loc(locs_sorted)
        elif my_style == 'safe':
            locs_sorted = sorted([i for i in probs if i.prob > 0.67])
            self.loc = get_loc(locs_sorted)
        elif my_style == 'off-center':
            locs_sorted = sorted([i for i in probs if angle_prob(i.angle) < 0.67])
            self.loc = get_loc(locs_sorted)
        else:
            self.loc = choice(probs)
        print(self.loc, self.loc.prob)
    
def get_loc(d):
    """ Pick a random coordinate from a set of coordinates using a Gaussian
            distribution.
            
    Arguments:
        d (list): the list of coordinates to pick from, sorted least to greatest
        
    Returns:
        Coordinate: the chosen coordinate.
    """
    a = 0
    quantiles = []
    for i in d:
        a += 1
        quantiles.append(a / len(d))
    pick = gauss(mu = 0.5, sigma = 0.2)
    while pick > 1 or pick < 0:
        pick = gauss(mu = 0.5, sigma = 0.2)
    b = 0
    for j in quantiles:
        if pick < j:
            return d[b - 1]
        b += 1
        
styles = ('random', 'risky', 'safe', 'off-center')

court_len, court_width = (13, 22)

def dist_prob(x):
    exponent = -7 * (-x + 0.6)
    return 1 / (1 + exp(exponent))

def angle_prob(theta):
    if theta < 0:
        return (theta / pi) + 1
    return (-theta / pi) + 1

def normalize_dist(dist, length, width):
    max_dist = ((0.25 * (width ** 2)) + (length ** 2)) ** 0.5
    return dist / max_dist

class Coordinate:
    def __init__(self, x, y, width):
        self.cx = x - (width / 2)
        self.cy = y
        self.px = x
        self.py = y
        self.w = width
        self.h = ((self.cx ** 2) + (self.cy ** 2)) ** 0.5
        self.pair = (x, y)
        if self.cy == 0:
            if self.cx < 0:
                self.angle = -pi / 2
            elif self.cx > 0:
                self.angle = pi / 2
            else:
                self.angle = 0
        else:
            self.angle = atan2(self.cy, self.cx)
        self.prob = 1
    
    def __str__(self):
        return f"{self.pair}"
    
    def __repr__(self):
        return f"<Coordinate({self.px}, {self.py}, {self.w})>"
    
    def __lt__(self, other):
        return True if self.prob < other.prob else False
    
    def value(self):
        self.prob1 = angle_prob(self.angle)
        self.prob2 = dist_prob(normalize_dist(self.h, court_len, court_width))
        self.prob = self.prob1 * self.prob2
        return self.prob

def make_grid(length, width):
    coords = []
    for i in range(1, length + 1):
        for j in range(1, width + 1):
            coords.append(Coordinate(j, i, width))
    for c in coords:
        c.value()
    return coords

grid = make_grid(court_len, court_width)

def find_coordinate(x, y):
    for coord in grid:
        if coord.px == x and coord.py == y:
            return coord

court = """
             1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22
            ::::::^::::::::::::::::::::::::::^::::::::::::::::::^::::::::::::::::::::::::::^::::::
         1  ~.    ~                         :^                  ::                         ~:   .^   
            ~.    ~                         .^    .:::^^^::.    :.                         ~.   .^
            ~.    ~                         .^       ^::~       :.                         ~.   .^    
         2  ~.    ~                         .^        ..        :.                         ~.   .^  
            ~.    ~                         .^                  :.                         ~.   .^    
            ~.    ~                         .^                  :.                         ~.   .^  
         3  ~.    ~                         .^                  :.                         ~.   .^    
            ~.    ~                         :^                  ::                         ~.   .^    
            ~.    ~                         :^                  ::                         ~.   .^    
         4  ~.    ~                         :^       .  .       ::                         ~.   .^    
            ~.    ~                         :^  .:. :.  .:. :.  ::                         ~.   .^    
            ~.    ^:                        .^  :.          .:  ::                        .~    .^    
         5  ~.     ^:                       .~^                ^^.                       .~     .^   
            ~.      ^:                      :~                  ^:                      :^      .^    
            ~.       :^.                    :!::::::::::::::::::~:                     ^:       .^    
         6  ~.        .^:                   .~                  ~.                   :^.        .^    
            ~.          .^:                  ^^                :^                  :^:          .^   
            ~.            .^:.                :^.            .^:                .:^:            .^    
         7  ~.              .:^:.               :^:...  ...:^:.              .:::.              .^    
            ~.                 .:::.              ...::::...              .:::.                 .^    
            ~.                    ..:::..                            ..::::.                    .^    
         8  ~.                         ..::::......        ......::::...                        .^    
            ~.                               .....::::::::::.....                               .^    
            ~.                                                                                  .^    
         9  ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
         10 ~.                                                                                  .^        
            ~.                                                                                  .^    
            ~.                                                                                  .^
         11 ~.                                                                                  .^      
            ~.                                     .......                                      .^  
            ~.                                 .:::.......::.                                   .^    
         12 ~.                                ::.           .::                                 .^    
            ~.                               ^.               .^                                .^    
            ~.                              ^.                 ::                               .^    
         13 ^^::::::::::::::::::::::::::::::~:::::::::::::::::::^:::::::::::::::::::::::::::::::^:  """
         
def draw_court(current_location = None):
    """Draws a court in ASCII characters and adds a marker based on
    the X and Y coordinate specified 
    
    Args:
        current_location (tuple): The current location on the court based on the 
        X and Y coordinates given. 
        
        Side effects: 
            Prints the court with the marker at a specified location
            to the terminal. 
    """
    if current_location == None:
        new_court = court
    else:
        new_court = " "
        marker = "X"
        counts = 0
        x, y = current_location #unpacking the current location sequence into x and y variables.
        line_number = 3 * (y) + 1
        if not (0 < y < 14 and 0 < x < 23): #Ensures that the location specified is within the boundaries of the court and continues if it is.
            print("Out of bounds, please try again.") 
            return
        for line in court.split("\n"):
            counts += 1
            if counts == line_number: # If counts is equivalent to index 0 of the current location (x-axis) then continue
                index = 4 * x + 9 
                new_line = line[:index] + marker + line[index + 1:] #splices through ther line and adds the marker on the specification of index 1 (y-axis)
                new_court += new_line + "\n" #adds the new line with the marker to the new court 
            else:
                new_court += line + "\n" #add the unchanged lines to the new court 
    print(new_court)
    
def main():
    gs = GameState()
    n = 0
    while gs.check_win() == None:
        print(f"It's {gs.p1.name}'s turn to pick")
        gs.turn()
        n += 1
        if n % 10 == 0:
            print(f"It's turn {n}")
        print(f"Scores:\n{gs.players[0].name}: {gs.players[0].score}\n{gs.players[1].name}: {gs.players[1].score}")
        a = input("Press Enter to continue  ")
    print(f"{gs.check_win().name} wins!")
        
if __name__ == '__main__':
    grid = make_grid(court_len, court_width)
    main()