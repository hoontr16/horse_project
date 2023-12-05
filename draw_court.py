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
         13 ^^::::::::::::::::::::::::::::::~:::::::::::::::::::^:::::::::::::::::::::::::::::::^:  """ #ASC II representation of court 
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

draw_court((6, 11))