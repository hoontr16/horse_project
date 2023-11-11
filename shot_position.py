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

