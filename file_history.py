def history_to_file(self, filename):
    """Writes the shot history for each player to a file.

        Arguments:
            filename (str): The name of the file to write the shot history.
            """
    #opens and writes to file
    with open(filename, 'w') as f:
        for player in self.players:
            f.write(f"{player.name}'s shot history: {player.shot_history}\n"))
                                                    
    
    