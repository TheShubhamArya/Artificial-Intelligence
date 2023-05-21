Shubham Arya 1001650536
Python 3.10.9

Run Commands: 
Locate the folder in your terminal using the cd command. Once you are in the current directory, run the following: 
python3 red_blue_nim.py <num-red> <num-blue> <first-player> <depth>

The depth functionality is implemented.

Code Structure:
All of the code is structured in the red_blue_nim.py file. The main function first gets all the command line argument from the user and then calls the red_blue_num() function.

The red_blue_min function is called recursively until the game is over. This function decides which player should play depending on the previous player. If the previous player was computer, then the next player is human, so it will ask the human player for their input which is either 'red' or 'blue'. If the previous player was human, then next player is computer, which calls the alpha_beta_decision() function to decide which move to take. 

The alpha_beta_decision function calls the maxValue() function which returns the best possible move to take for the computer.

The maxValue and minValue functions are recursively called within each other to get to the best decision for the computer.

Depending on if the depth was given or not, the maxValue and the minValue functions are cut-off when the depth limit is reached. At this point, if it is not a temrinal state, then the evaluation function is called that evaluates the current situation and returns a utility for that state. ExtraCredit.txt has more information about this. 

Lastly, there are two helper functions is_game_over() and calculate_points() that check if the game is over and calculates the points when the game is over respectively.


Run command- python3 red_blue_nim.py <num-red> <num-blue> <first-player> <depth>
