def draw_court(current_location):
    """Draws a court in ASCII characters and adds a marker based on
    the X and Y coordinate specified 
    
    Args:
        current_location (tuple): The current location on the court based on the 
        X and Y coordinates given. 
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
            ^^::::::::::::::::::::::::::::::~:::::::::::::::::::^:::::::::::::::::::::::::::::::^:  """
    new_court = " "
    marker = "X"
    counts = 0
    for line in court.split("\n"):
        counts += 1
        if counts == current_location[0]:
            if 2 < current_location[0] < 39 and 13 < current_location[1] < 96:
                new_line = line[:current_location[1]] + marker + line[current_location[1] + 1:]
                new_court += new_line + "\n"
            else:
                print("Out of bounds, please try again.")
                return
        else:
            new_court += line + "\n"
    
    print(new_court)

draw_court((3, 25))