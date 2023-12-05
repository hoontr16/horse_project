def draw_court(current_location):
    """Draws a court in ASCII characters and adds a marker based on
    the X and Y coordinate specified 
    
    Args:
        current_location (tuple): The current location on the court based on the 
        X and Y coordinates given. 
    """
    court = """
            ::::::^::::::::::::::::::::::::::^::::::::::::::::::^::::::::::::::::::::::::::^::::::
            ~.    ~                         :^                  ::                         ~:   .^   
            ~.    ~                         .^    .:::^^^::.    :.                         ~.   .^
            ~.    ~                         .^       ^::~       :.                         ~.   .^    
            ~.    ~                         .^        ..        :.                         ~.   .^  
            ~.    ~                         .^                  :.                         ~.   .^    
            ~.    ~                         .^                  :.                         ~.   .^  
            ~.    ~                         .^                  :.                         ~.   .^    
            ~.    ~                         :^                  ::                         ~.   .^    
            ~.    ~                         :^                  ::                         ~.   .^    
            ~.    ~                         :^       .  .       ::                         ~.   .^    
            ~.    ~                         :^  .:. :.  .:. :.  ::                         ~.   .^    
            ~.    ^:                        .^  :.          .:  ::                        .~    .^    
            ~.     ^:                       .~^                ^^.                       .~     .^   
            ~.      ^:                      :~                  ^:                      :^      .^    
            ~.       :^.                    :!::::::::::::::::::~:                     ^:       .^    
            ~.        .^:                   .~                  ~.                   :^.        .^    
            ~.          .^:                  ^^                :^                  :^:          .^   
            ~.            .^:.                :^.            .^:                .:^:            .^    
            ~.              .:^:.               :^:...  ...:^:.              .:::.              .^    
            ~.                 .:::.              ...::::...              .:::.                 .^    
            ~.                    ..:::..                            ..::::.                    .^    
            ~.                         ..::::......        ......::::...                        .^    
            ~.                               .....::::::::::.....                               .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                                                                  .^    
            ~.                                     .......                                      .^  
            ~.                                 .:::.......::.                                   .^    
            ~.                                ::.           .::                                 .^    
            ~.                               ^.               .^                                .^    
            ~.                              ^.                 ::                               .^    
            ^^::::::::::::::::::::::::::::::~:::::::::::::::::::^:::::::::::::::::::::::::::::::^:  """
    new_court = " "
    marker = "X"
    counts = 0
    for line in court.split("\n"):
        counts += 1
        if counts == current_location[0]:
            if 2 < current_location[0] < 39 and 13 < current_location[1] < 96:
                new_line = line[:current_location[1]] + marker + line[current_location[1] + 1:]
                new_court += new_line + "\n"
            else:
                print("Out of bounds, please try again.")
                return
        else:
            new_court += line + "\n"
    
    print(new_court)

#draw_court((3, 25))

from math import atan, exp, pi
from random import choice, gauss

""" 
    Only get_loc and pick_location directly determine the AI, everything else
    was necessary for testing, and to determine whether the AI's personality
    styles actually worked.
"""

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
        quantiles.append(a / len(d))
        a += 1
    pick = gauss(mu = 0.5, sigma = 0.2)
    while pick > 1 or pick < 0:
        pick = gauss(mu = 0.5, sigma = 0.2)
    b = 0
    for j in quantiles:
        if pick < j:
            return d[b - 1]
        b += 1

def pick_location(probs, style, my_score, other_score):
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
    if my_score - other_score > 2:
        my_style = 'risky'
    elif my_score - other_score < -2:
        my_style = 'safe'
    else:
        my_style = style
    if my_style == 'risky':
        new_probs = {i: probs[i] * (1 - probs[i]) for i in probs if probs[i] * (1 - probs[i]) > 0.15}
        locs_sorted = sorted(new_probs, key = lambda c: new_probs[c] * (1 - new_probs[c]))
        return get_loc(locs_sorted)
    elif my_style == 'safe':
        new_probs = {i: probs[i] for i in probs if probs[i] > 0.67}
        locs_sorted = sorted(new_probs, key = lambda c: new_probs[c] * (1 - new_probs[c]))
        return get_loc(locs_sorted)
    elif my_style == 'off-center':
        new_probs = {i: probs[i] for i in probs if angle_prob(i.angle) < 0.67}
        locs_sorted = sorted(new_probs, key = lambda c: new_probs[c] * (1 - new_probs[c]))
        return get_loc(locs_sorted)
    else:
        return choice(list(probs.keys()))



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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = ((x ** 2) + (y ** 2)) ** 0.5
        self.pair = (x, y)
        if y == 0:
            if x < 0:
                self.angle = -pi / 2
            elif x > 0:
                self.angle = pi / 2
            else:
                self.angle = 0
        else:
            self.angle = atan(x / y)
        self.prob = 1
    
    def __str__(self):
        return f"{self.pair}"
    
    def __lt__(self, other):
        return True if self.h < other.h else False
    
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
    prev_results (str): The results of the last round.
    players (list): List of Player instances.
    """
    if prev_results == "success":
        players[0].score = players[0].score + 1  # index would be at 0

    # Print the current scores for all players
    print("Present Score:")
    for player in players: 
        print(f"{player.name}: {player.score} points") # Name:ScoreXX

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
    def pick_location(self):
        return ai_logic()

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

