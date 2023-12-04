def draw_court(current_location):
    """Draws a court in ASCII characters and adds a marker based on
    the X and Y coordinate specified 
    
    Args:
        current_location (tuple): The current location on the court based on the 
        X and Y coordinates given. 
        
        Side effects: 
            Prints the court with the marker at a specified location
            to the terminal. 
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
            ^^::::::::::::::::::::::::::::::~:::::::::::::::::::^:::::::::::::::::::::::::::::::^:  """ #ASC II representation of court 
    new_court = " "
    marker = "X"
    counts = 0
    for line in court.split("\n"):
        counts += 1
        if counts == current_location[0]: # If counts is equivalent to index 0 of the current location (x-axis) then continue
            if 2 < current_location[0] < 39 and 13 < current_location[1] < 96: #Ensures that the location specified is within the boundaries of the court and continues if it is.
                new_line = line[:current_location[1]] + marker + line[current_location[1] + 1:] #splices through ther line and adds the marker on the specification of index 1 (y-axis)
                new_court += new_line + "\n" #adds the new line with the marker to the new court 
            else:
                print("Out of bounds, please try again.") 
                return
        else:
            new_court += line + "\n" #add the unchanged lines to the new court 
    
    print(new_court)

draw_court((3, 25))