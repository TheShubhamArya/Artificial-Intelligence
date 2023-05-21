Shubham Arya 1001650536
Programming language used: Python 3.9.6

Code structure:
All the code is present in the expense_8_puzzle.py file. This file has 7 functions for each of the 5 uninformed search algorithms and the 2 informed search algorithm. Depending on the method that the user chooses, one of these functions is called to perform the method. There are other utility functions that are used to perform these search operations. 

Each state is represented by an instance of class Node. Each state has a node assigned to it, which also has a parent state assigned as well among other attributes. Any time a state's successor are found, their corresponding nodes are created. To find the path from the start state to goal state, all that is needed is to look at the parent node for every state until the first state is reached who has no parent. 

If the dumpFlag is true, then anytime a node is expanded, all the information is written into a file. This happens for all the 7 search algorithms. 

Run commands:
On your terminal, go to the folder where this readme file is located using cd command. Then type the following line to run it:
python3 expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>

