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