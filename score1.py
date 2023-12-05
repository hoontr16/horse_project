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
        
# def create_player(): 