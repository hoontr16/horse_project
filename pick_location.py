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
        get_loc(locs_sorted)
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
    probs = {}
    for coord in locs:
        probs[coord] = coord.value()
    #s_probs = sorted(probs.items, key = probs.values, reverse=True)
    #median = s_probs[]
    return probs

styles = ('random', 'risky', 'safe', 'off-center')

if __name__ == '__main__':
    grid = make_grid(court_len, court_width)
    vals = get_vals(grid)
    x = 0
    while x < 20:
        a = pick_location(vals, 'safe', 0, 0)
        print(a, a.prob)
        x += 1