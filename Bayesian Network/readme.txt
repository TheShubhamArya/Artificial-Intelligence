Shubham Arya 
1001650536

Python 3.10.9

Run Commands:
Locate the directory with bnet.py file in your terminal and then enter the following commands-
python3 bnet.py <training_data> <query variable values> [given <evidence variable values>]

Below are some examples to perform task 1,2, and 3.
    For TASK 1:
    Eg. python3 bnet.py training_data.txt

    For TASK 2:
    Eg. python3 bnet.py training_data.txt <Bt/Bf> <Gt/Gf> <Ct/Cf> <Ft/Ff>

    For TASK 3 with no given variables
    Eg. python3 bnet.py training_data.txt [<Bt/Bf> or <Gt/Gf> or <Ct/Cf> or <Ft/Ff>] 

    For TASK 3 with given variables
    Eg. python3 bnet.py training_data.txt [<Bt/Bf> or <Gt/Gf> or <Ct/Cf> or <Ft/Ff>] given [<Bt/Bf> or <Gt/Gf> or <Ct/Cf> or <Ft/Ff>]

Code Structure:
The code is structured into different function that perform specific functions. 

There is a function that converts file content into an array of integers.

There is function to find probabilities and conditional probabilities for B, C, G, and F that is named like findBTrue, findCTrue, findGTrue, findFTrue. These functions go through the file data and finds count of all instances with the a variable X being true given variable Y (optional). Each of these functions return the count of the instance where it was true and false. 

A function getBayesianNetwork calls the above functions, and stores them into an array called bayesianNetwork. Here, the 0th index stores B values, the 1st index stores C values, the 2nd index stores G valus, and the 3rd index stores F values. This function combines all the values and returns the bayesian network. Function getValuesFromNetwork, networkIndex and indexForG are support functions for getBayesianNetwork that have the knowledge of which index corresponds to what value in the network.

Function printTask1 prints the conditional probability distribution information for task 1.

Function find fixed variables looks for the variables that have been mentioned in the command line prompt. This gives the information about which variables to change and not change while doing inference by enumeration.

The calculateProbability function calculates probability given fixed variables. It enumerates over all the unknown variables, finds probability for each of those cases, and adds them up to give the final probability. 

The main function calls the above functions. It also separates the tasks (1, 2 or 3) and performs them.




