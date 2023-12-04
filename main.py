from player import Player, ComputerPlayer
from random import choice
from draw_court import draw_court

def main():
    """ The actual game loop.
    """
    players = []
    humans = input("How many human players?")
    comps = input("How many computer players?")
    for i in range(humans):
        players.append(Player(input(f"Player {len(players) + 1}, what is your name? "), (0, 0)))
    for j in range(comps):
        players.append(ComputerPlayer(f"Computer {j}", (0, 0)))
    cp = choice(players)
    while True:
        c = cp.pick_location()
        draw_court(c)
        cp.shoot()
        
    