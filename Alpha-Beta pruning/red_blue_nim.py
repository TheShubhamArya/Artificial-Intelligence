# Shubham Arya 1001650536
# CSE 5360 Artificial Intelligence 1, Spring 2023
# Assignment 2: Game Playing Problem
import sys

# game played recursively with players switching every turn until one of the bag is 0.
def red_blue_nim(red_stones, blue_stones, player, depth):
    previous_turn = "computer" if player == "human" else "human"
    print("------------------------------")
    print("RED: ", red_stones," BLUE: ", blue_stones)
    if is_game_over(red_stones, blue_stones):
        print() 
        print(player.upper()," won ", calculate_points(red_stones, blue_stones)," points")
    else:
        next_turn = previous_turn
        action = ""
        if player == "human":
            action = input("Enter stone to pick: ")
        else:
            action = alpha_beta_decision(red_stones, blue_stones, depth)
            print("Computer played: ", action)

        if action.lower() == "red":
            red_blue_nim(red_stones - 1, blue_stones, next_turn, depth)
        else:
            red_blue_nim(red_stones, blue_stones - 1, next_turn, depth)

# returns the action that would lead to the best possible outcome for computer.
def alpha_beta_decision(red_stones, blue_stones, depth):
    _, action = maxValue(red_stones, blue_stones, float('-inf'), float('inf'), depth)
    return action

# returns the utility and action taken by the computer
def maxValue(red_stones, blue_stones, alpha, beta, depth):
    
    if is_game_over(red_stones, blue_stones):
        v = calculate_points(red_stones, blue_stones)
        return v, ""
    
    if depth == 0:
        return evaluation_function(red_stones, blue_stones, "human"), ""

    v = float('-inf')
    action = ""

    # red as successor 
    v_min = minValue(red_stones - 1, blue_stones, alpha, beta, depth - 1)
    if v_min > v:
        v = v_min
        action = "red"

    if v >= beta:
        return v, action
    alpha = max(alpha, v)

    # blue as successor
    v_min = minValue(red_stones, blue_stones - 1, alpha, beta, depth - 1)
    if v_min > v:
        v = v_min
        action = "blue"

    if v >= beta:
        return v , action
    alpha = max(alpha, v)

    return v, action

# returns the lowest utility for computer given a optimal opponent
def minValue(red_stones, blue_stones, alpha, beta, depth):

    if is_game_over(red_stones, blue_stones):
        v = calculate_points(red_stones, blue_stones)*-1
        return v
    
    if depth == 0:
        return evaluation_function(red_stones, blue_stones, "computer")

    v = float('inf')

    # red as successor
    v_max, _ = maxValue(red_stones - 1, blue_stones, alpha, beta, depth - 1)
    v = min(v, v_max)
    if v <= alpha:
        return v
    beta = min(beta, v)

    # blue as successor
    v_max, _ = maxValue(red_stones, blue_stones-1, alpha, beta,  depth - 1)
    v = min(v, v_max)
    if v <= alpha:
        return v
    beta = min(beta, v)
    return v

# tells whether the game is over or not
def is_game_over(red_stones, blue_stones):
    return True if red_stones == 0 or blue_stones == 0 else False

# calculates points given that one of the bag is empty
def calculate_points(red_stones, blue_stones):
    return 3*blue_stones if red_stones == 0 else 2*red_stones

# evaluates a utility for the current state given a depth limit is reached
def evaluation_function(red_stones, blue_stones, player):
    utility = 2

    if player == "computer":
        if red_stones == 1:
            return 3*blue_stones
        elif blue_stones == 1:
            return 2*red_stones
        elif (red_stones % 2 == 0 and blue_stones % 2 == 0) or (red_stones % 2 != 0 and blue_stones % 2 != 0): # when red_st
            utility *= -1
        else:
            utility = -2
    elif player == "human":
        if red_stones == 1:
            return 3*blue_stones*-1
        elif blue_stones == 1:
            return 2*red_stones*-1
        elif (red_stones % 2 == 0 and blue_stones % 2 == 0) or (red_stones % 2 != 0 and blue_stones % 2 != 0):
            utility *= 1
        else:
            utility = 2
        
    return utility

if __name__ == "__main__":
    args = len(sys.argv)
    if args > 5 or args < 3:
        print("Error. Run command: python3 red_blue_nim.py [num-red] [num-blue] [player] [depth]")
        exit()
    player = "computer"
    depth = -1
    red_stones = int(sys.argv[1])
    blue_stones = int(sys.argv[2])
    if args >= 4:
        arg_i_3 = sys.argv[3].lower()
        if arg_i_3 == "computer" or arg_i_3 == "human":
            player = arg_i_3
        elif (arg_i_3 != "computer" or arg_i_3 != "human") and args == 4:
            depth = int(sys.argv[3])
        elif args == 5:
            depth = int(sys.argv[4])
            
    print("\nWhen it is your turn type:\n- red to pick red marbles\n- blue to pick blue marbles\n")
    red_blue_nim(red_stones, blue_stones, player, depth)
