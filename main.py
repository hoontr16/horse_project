from player import Player, ComputerPlayer
from random import choice
from draw_court import draw_court


def main():
    """ Create and run the game.
    """
    gs = GameState()
    n = 0
    while gs.check_win() is None:
        print(f"It's {gs.p1.name}'s turn to pick")
        gs.turn()
        n += 1
        print(f"It's turn {n}") if n % 10 == 0 else None
        gs.display_scores()
        a = input("Press Enter to continue  ")

    print(f"{gs.check_win().name} wins!")
        
        
    