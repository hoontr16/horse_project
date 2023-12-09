from random import shuffle, choice, gauss, random
from math import atan2, exp, pi
import re
from time import sleep

class GameState:
    """ The current game, keeping track of the players and turn order.

    Attributes:
        players (list): the human and computer players.
        cp (int): which player is choosing the next location to shoot from,
            as an index into self.players. either 0 or 1
        p1 (Player): the player choosing the location to shoot from.
        p2 (Player): the player shooting second.
    """
    def __init__(self):
        """ Create Player objects and create their initial shooting order.
        
        Side effects:
            asks for input on the number of human and computer players
            sets appropriate attributes
        """
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
        """ Process a turn of shooting.
        
        Side effects:
            resets player and self attributes
            calls methods to pick the location and shoot
        """
        self.p1.shot, self.p2.shot = None, None
        self.p1 = self.players[self.cp]
        self.p2 = self.players[(self.cp + 1) % 2]
        self.p1.pick_location(grid, self.p2.score)
        self.p1.shoot()
        if self.outcome() == 'switch':      #if p1 misses their chosen shot
            self.p1 = self.players[self.cp]
            self.p2 = self.players[(self.cp + 1) % 2]            
            return
        self.p2.loc = self.p1.loc
        self.p2.shoot()
        self.outcome()

    def outcome(self):
        """ Determine points given and whether to switch the current player
                after a shot.
            
        Side effects:
            changes the current player if they missed the shot they picked
            gives a point when required
            
        Raises:
            ValueError: when the attributes of both players are in an invalid
                state.
                
        Returns:
            str: either 'switch', 'score', or 'pass', depending on what happened
            None: when only the first player has shot, and made it
        """
        if self.p1.shot == False:           # if p1 misses, switch the turn order
            self.cp = (self.cp + 1) % 2
            return 'switch'
        elif self.p2.shot == None:
            return
        elif self.p1.shot and not self.p2.shot: #if p2 misses, give them a point
            self.p2.score += 1                  #and keep the turn order
            return 'score'
        elif self.p1.shot and self.p2.shot: #if both shots are successful,
            return 'pass'                   #change nothing
        else:
            raise ValueError("Invalid game status")
        
    def check_win(self):
        if self.p1.score > 4:
            return self.p2
        elif self.p2.score > 4:
            return self.p1

class Player:
    """ A base class for both human and computer players.
    
    Attributes:
        score (int): the player's current score, between 0 - 5
        shot (bool, NoneType): whether the player's last shot was successful.
            Is None when they haven't shot yet that turn.
    """
    def __init__(self, pnum):
        """ Set attributes for any Player object.
        
        Arguments:
            pnum (int): the number of players already created. either 0 or 1.
                Only used in the subclasses of Player
                
        Side effects:
            Sets basic attributes
        """
        self.score = 0
        self.shot = None

    def shoot(self):
        """
        Prints the player's name and the shot attempt with a delay after calculated probability.

        Side-effects:
            Updates the shot attribute of the player object.

        Returns:
            None
        """     
         
        print(f"{self.name} is taking their shot...")
        sleep(0.5)
        
        probability = min(1.0, self.loc.prob)
        result = random() < probability
        
        if result:
            print(f"{self.name} made the shot!")
            self.shot = True
        else:
            print("Bad shot")
            self.shot = False
            
class HumanPlayer(Player):
    """ A subclass of Player for humans.
    
    Attributes:
        score (int): the player's current score, between 0 - 5.
            Inherited from Player
        shot (bool, NoneType): whether the player's last shot was successful.
            Is None when they haven't shot yet that turn. Inherited from Player
        name (str): the player's chosen name
        loc (Coordinate): where the player is currently shooting from.
    """
    def __init__(self, pnum):
        """ Initialize a human player.
        
        Arguments:
            pnum (int): the number of players already created. either 0 or 1
        
        Side effects:
            takes console input to set their name attribute
            calls the __init__ method of the parent class
        """
        self.name = input(f"Player {pnum}, what is your name? ")
        super().__init__(self)
    
    def pick_location(self, probs, other_score):
        """ Get a valid to shoot from from the player, and display their choice.
        
        Arguments: 
            probs (dict): coordinate objects and their shot probabilities.
                Only used by the ComputerPlayer class.
            other_score (int): the other player's current score. Only used by
                the ComputerPlayer class.
        
        Side effects:
            resets shot attribute of self
            calls draw_court to display the court and their chosen location
            recieve console input to determine the location
            find their choice as a Coordinate object in a preexisting grid
            set self.loc to that Coordinate
        """
        self.shot = None
        draw_court()
        a = input(f"{self.name}, where would you like to shoot from? ")
        r = r"^\(?(\d+)[\s,]+?(\d+)\)?$" #searches for 2 numbers, separated by
        match = re.search(r, a) #commas and/or spaces, optionally
        while not match:        #surrounded by parentheses
            print("Please enter in this format: x, y")
            a = input(f"{self.name}, where would you like to shoot from? ")
            match = re.search(r, a)
        c = find_coordinate(int(match[1]), int(match[2]))
        print("You will be shooting from the X below:")
        draw_court(c.pair)
        self.loc = c

class ComputerPlayer(Player):
    """ A subclass of Player, for a computer player.
    
    Attributes:
        score (int): the player's current score, between 0 - 5.
            Inherited from Player
        shot (bool, NoneType): whether the player's last shot was successful.
            Is None when they haven't shot yet that turn. Inherited from Player
        name (str): a string denoting which computer player they are
        style (str): the AI's preference for picking locations. Will be one of:
            risky: chooses shots with a greater than 15% chance of giving the 
                opponent a point.
            safe: chooses shots with at least a 67% chance of success.
            off-center: chooses locations where the angle from the net decreases
                shot probability by more than 33% (extreme angles).
            random: picks locations completely at random.
        loc (Coordinate): where the player is currently shooting from.    
    """
    def __init__(self, pnum):
        """ Initialize a computer player.
        
        Arguments:
            pnum (int): the number of players already created. either 0 or 1
        
        Side effects:
            sets the name to a string based on pnum
            chooses a random style as its self.style
            prints the chosen style
            calls the __init__ method of the parent class
        """
        super().__init__(self)
        self.name = f"Computer {pnum}"
        self.style = choice(styles)
        print(self.style)
        
    def pick_location(self, probs, other_score):
        """ Decide on a location for an AI player to shoot from, given the current
                game state.
        
        Arguments:
            probs (dict): coordinate objects and their shot probabilities.
            other_score (int): the other player's current score
        
        Side effects:
            sets player location to the chosen Coordinate object
            prints the chosen location and its shot probability
        """
        if self.score - other_score < -2:
            my_style = 'risky'
        elif self.score - other_score > 2:
            my_style = 'safe'
        else:
            my_style = self.style
        if my_style == 'risky': #calc the likelihood of scoring a point, don't go below 15%
            locs_sorted = sorted([i for i in probs if i.prob * (1 - i.prob) > 0.15],
                                 key=lambda c: c.prob * (1 - c.prob))
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
    quantiles = [] #assign each member of d a fraction of the numbers between
    for i in d:    #0 and 1, in order
        a += 1
        quantiles.append(a / len(d))
    pick = gauss(mu = 0.5, sigma = 0.2) #a normal distribution centered around
    while pick > 1 or pick < 0: #0.5, so very likely to be 0 < pick < 1 
        pick = gauss(mu = 0.5, sigma = 0.2)
    b = 0
    for j in quantiles: 
        if pick < j:        #if the random number is in the Coordinate's section
            return d[b - 1] #find and return it
        b += 1
        
styles = ('random', 'risky', 'safe', 'off-center')

court_len, court_width = (13, 22)

def dist_prob(x):
    """ Calculate the probability of making a shot based on distance, using a 
            logistic function. This decreases the changes in probability at short
            and long range, meaning small changes at either extreme have little
            effect on the probability.
            
    Arguments:
        x (int or float): the distance to the net.
    
    Returns:
        float: the calculated effect of distance on probability.
    """
    exponent = -7 * (-x + 0.6)     # a logistic function decreases the effects
    return 1 / (1 + exp(exponent)) # of change at the extremes, which we felt
                                   # was more realistic
def angle_prob(theta):
    """ Transform an angle from radians to a probability between 0 and 1.
    
    Arguments:
        theta (float): an angle in radians
        
    Returns:
        float: the effect of angle on probability, taking the sign into account.
    """
    if theta < 0:
        return (theta / pi) + 1
    return (-theta / pi) + 1 #if angle is not negative, make it negative

def normalize_dist(dist, length, width):
    """ Transforms a distance from the net into a probability between 0 and 1.
    
    Arguments:
        dist (int or float): the distance to transform.
        length (int): the length of the court
        width (int): the width of the court
        
    Returns:
        float: the ratio of the distance over the maximum distance
    """
    max_dist = ((0.25 * (width ** 2)) + (length ** 2)) ** 0.5 #calculating the maximum distance
    return dist / max_dist #turns it into a probability, making calculations easier

class Coordinate:
    """ An ordered pair on our court grid.
    
    Attributes:
        cx (int or float): the x value, modified to make the position of the 
            net (0, 0). used for calculations
        cy (int): the y value, transformed to start counting at 0. 
            used for calculations
        px (int): the x value as seen on the grid. used for printing, 
            representation and finding the object
        py (int):the y value, used for printing, representation and finding the
            object
        w (int): the width of the court, used for calculating cx
        h (float): the distance (or hypotenuse) from the point to the net
        pair (tuple): the ordered pair of x and y
        angle (int or float): the angle from the net
        prob (int or float): the likelihood of a shot from this location making it
        type (str): what type of shot this position is, used to further modify the
            probability
    """
    def __init__(self, x, y, width):
        self.cx = x - (width / 2)
        self.cy = y - 1
        self.px = x
        self.py = y
        self.w = width
        self.h = ((self.cx ** 2) + (self.cy ** 2)) ** 0.5
        self.pair = (x, y)
        if self.cy == 0:    #without this, we'd get a divide by zero error
            if self.cx < 0: #so we set the angle manually based on cx's sign
                self.angle = -pi / 2
            elif self.cx > 0:
                self.angle = pi / 2
            else:
                self.angle = 0
        else:
            self.angle = atan2(self.cy, self.cx)
        self.prob = 1
    
    def __str__(self):
        """ The string representation of the Coordinate, as an ordered pair.
        """
        return f"{self.pair}"
    
    def __repr__(self):
        """ The formal string representation, showing how to recreate the object.
        """
        return f"<Coordinate({self.px}, {self.py}, {self.w})>"
    
    def __lt__(self, other):
        """ Determine the order of two Coordinates by comparing probabilities.
        
        Arguments:
            other (Coordinate): the object to compare to.
        
        Returns:
            bool: whether self has a lower shot probability than other
        """
        return True if self.prob < other.prob else False
    

    def value(self):        
        """
        Calculates the probability after considering angle, distance, and type.
        
        Side-effects: 
            Sets relevant attributes for every type.
        
        Returns:
            Float:
                Calculated probability of making the shot, factoring in angle, distance, and type bonuses.     
        """
        
        self.prob1 = angle_prob(self.angle)
        self.prob2 = dist_prob(normalize_dist(self.h, court_len, court_width))
        self.prob = (self.prob1 * self.prob2)
        
        type_bonuses = {
            "lay-up": 0.10,
            "free-throw": 0.075,
            "three-pointer": -0.05,
            "two-pointer": 0.0
        }
        
        if self.h <=1:
            key = "lay-up"  
            self.type = key
            bonus = type_bonuses.get(key)
            self.prob += bonus     
        
        if self.py ==6 and self.px in range (9,15):
            key = "free-throw"  
            self.type = key
            bonus = type_bonuses.get(key)
            self.prob += bonus     
        
        if self.h >=9:
            key = "three-pointer"  
            bonus = type_bonuses.get(key)
            self.type = key
            self.prob += bonus  
        
        else:
            key = "two-pointer"  
            self.type = key
            bonus = type_bonuses.get(key)
            self.prob += bonus     
        
        return self.prob

def make_grid(length, width):
    """ Create a grid of Coordinate objects.
    
    Arguments:
        length (int): the court length
        width (int): the court width
        
    Side effects:
        calls the value method of each coordinate after creation
    
    Returns:
        list: a list of every Coordinate
    """
    coords = []
    for i in range(1, length + 1):
        for j in range(1, width + 1):
            coords.append(Coordinate(j, i, width))
    for c in coords:
        c.value()
    return coords

grid = make_grid(court_len, court_width)

def find_coordinate(x, y):
    """ Find the matching Coordinate object from an ordered pair.
    
    Arguments:
        x (int): the x value to match.
        y (int): the y value to match.
    
    Returns:
        Coordinate: the object with matching x and y values.
        None: if no object matches
    """
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
    """ Create and run the game.
    
    Side effects:
        print informative messages
    """
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