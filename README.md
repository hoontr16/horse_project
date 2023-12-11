# horse_project
Our INST-326 group project is to implement HORSE in Python. Horse is a basketball game in which players will: 

Choose a location, 

The Player will shoot a shot from the location they chose,

If the first player misses the shot, the turn switches to the second player,

If the first player makes the shot then the second player has to shoot from that location,

If the second player misses they will get a letter starting with H and the first player chooses the location again,

If the second player makes it then the first player just chooses the location again,

The game will continue until one player accumulates all letters to make the word HORSE. 

## Purpose of each file in the repository 

horse_demo.py: Full code 

draw_court.py: To show Arvin's contribution to the draw_court function.

README.md: Documentation 

### Running the program
After running the horse_demo.py program, the terminal will ask you how you would like to play. You can play with two human players, 1 human player, and one computer player or two computer players. If you specify human players the terminal will ask you to enter your name. Whenever it is a human player's turn, they have to press the enter to continue, and an empty court representation will be shown in the terminal. Then they are asked to input a location in x, y format. Whenever it is a computer player's turn, click enter to continue. 

### Attribution

| Method/Function | Primary author | Techniques demonstrated |
|:----------------|:---------------|:------------------------|
|draw_court|Arvin Torabazari| Sequence Unpacking|
|check_win|Arvin Torabazari| Conditional Expressions| 
|display_shot_history| Arvin Torabazari| N/A|