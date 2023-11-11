def score(prev_results, players):
    """
    """
    if prev_results == "success":
        players[0].score = players[0].score + 1  # I believe index would be at 1

    # Print the current scores for all players
    print("Present Score:")
    for player in players: 
        print(f"{player.name}: {player.score} points") # Name:ScoreXX