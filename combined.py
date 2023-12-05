def draw_court(current_location):
    """Draws a court in ASCII characters and adds a marker based on
    the X and Y coordinate specified 
    
    Args:
        current_location (tuple): The current location on the court based on the 
        X and Y coordinates given. 
        
        Side effects: 
            Prints the court with the marker at a specified location
            to the terminal. 
    """
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
         13 ^^::::::::::::::::::::::::::::::~:::::::::::::::::::^:::::::::::::::::::::::::::::::^:  """ #ASC II representation of court 
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

#draw_court((3, 25))

from math import atan2, exp, pi
from random import choice, gauss

court_len, court_width = (20, 16)

def dist_prob(x):
    exponent = -7 * (-x + 0.6)
    return 1 / (1 + exp(exponent))

def angle_prob(theta):
    if theta < 0:
        #print(theta)
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
    for i in range(length):
        for j in range(width):
            coords.append(Coordinate(int(j - (width / 2)), i))
    return coords

def get_vals(locs):
    probs = {coord: coord.value() for coord in locs}
    return probs

styles = ('random', 'risky', 'safe', 'off-center')

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

def score(prev_results, players):
    """
    Adds the score after each shot, giving points to the given player, and print messages describing the round.
    
    Args:
        prev_results (str): Last round results, either "success" or "failure".
        players (list): List of the Player instances.
    """
    if prev_results == "success":
        # Increment the score of the player who made the shot
        for player in players:
            if player.shooter:
                player.score += 1

    # Print the current scores for all players
    print("Present Score:")
    for player in players:
        print(f"{player.name}: {player.score} points")
        
def do_outcome(player1, player2):
    if player2.shot == None:
        return
    elif player1.shot == False:
        return 'switch'
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
            self.loc = choice(list(probs.keys()))
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
    #print(d)
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

def shot_position(self):
    """Takes user input on the position of the next shot that they would 
        like to take and updates thier location
        
        Returns:
            self.loc(int): new location of player 
            """
    while True:
        x_cor = int(input("input the X coordinate you would like to shoot from"))
        y_cor = int(input("input the Y coordinate you would like to shoot from"))
        if 2 < x_cor < 39 and 13 < y_cor < 96:
            break
        else:
            print("out of bounds, try again")
    self.loc = x_cor, y_cor
    print(f" your current location is {x_cor},{y_cor}")
    return self.loc

