# Shubham Arya 1001650536
# CSE 5360 Artificial Intelligence 1, Spring 2023
# Assignment 1: Uninformed and informed search 

import sys
from enum import Enum
import copy
from datetime import date
import time
import numpy as np

class Node:
    def __init__(self, state, emptyTile, parentNode, depth: int, cost: int, move: str, heuristic: int = 0):
        self.state = state
        self.emptyTile = emptyTile
        self.parentNode = parentNode
        self.depth = depth
        self.cost = cost
        self.move = move
        self.heuristic = heuristic

class Method(Enum):
    bfs = "bfs"
    ucs = "ucs"
    dfs = "dfs"
    dls = "dls"
    ids = "ids"
    greedy = "greedy"
    aStar = "a*"

class DLS(Enum):
    soln = 0
    fail = 1
    cutoff = 2

nodesGenerated = 1
nodesExpanded = 0
nodesPopped = 0
maxFringeSize = 1

# Takes in the filename, opens it, parses it, and creates and returns a matrix
def createMatrix(filename):
    file = open(filename,'r')
    matrix=[]
    for line in file.readlines():
        if line == "END OF FILE":
            break
        matrix.append( [ int (x) for x in line.split(     ) ] )
    return matrix

# writes the input parameters to a file
def writeToFile(node, successors, fringe, visited, file):
    parentNode = node.parentNode
    if parentNode != None:
        file.write("Generating successors to <state = {}, action = '{}', depth = {}, g(n) = {}, f(n) = {}, Parent = {}>\n\n".format(node.state, node.move, node.depth, node.cost, node.heuristic, parentNode.state))
    else: 
        file.write("Generating successors to <state = {}, action = '{}', depth = {}, g(n) = {}, f(n) = {}, Parent = None>\n\n".format(node.state, node.move, node.depth, node.cost, node.heuristic))
    file.write("\t{} successors generated\n".format(len(successors)))
    file.write("\tNodes Generated: {}\n".format(nodesGenerated))
    file.write("\tNodes Expanded: {}\n".format(nodesExpanded))
    file.write("\tNodes Popped: {}\n".format(nodesPopped))
    file.write("\tFringe size: {}\n".format(len(fringe)))
    file.write("\tClosed: {}\n".format(visited))
    file.write("\tFringe: [\n")
    for node in fringe:
        file.write("\t<state = {}, action = '{}', depth = {}, g(n) = {}, f(n) = {}, Parent = {}>\n".format(node.state, node.move, node.depth, node.cost, node.heuristic, node.parentNode.state))
    file.write("\t]\n\n\n")

def breadthFirstSearch(start, goal, file=None):
    emptyTile = findEmptyTile(start)
    startNode = Node(start,emptyTile,None,0,0, "")
    global nodesGenerated, nodesExpanded, nodesPopped
    maxFringeSize = 1
    fringe = []
    fringe.append(startNode)
    visited = []
    while fringe:
        node = fringe.pop(0) # pops the first element of the fringe 
        nodesPopped += 1
        if node.state == goal:
            printOutput(node, nodesGenerated, nodesPopped, maxFringeSize, nodesExpanded, file)
            break

        if node.state not in visited: # perform actions only if the state has not been visited before
            visited.append(node.state) 
            successors = findSuccessor(node) # find successor to current node
            nodesExpanded += 1
            fringe+=successors # add these successors to the fringe
            nodesGenerated += len(successors)
            maxFringeSize = max(maxFringeSize, len(fringe))
            if file is not None:
                writeToFile(node, successors, fringe, visited, file)

def depthFirstSearch(start, goal, file=None):
    print("DFS is running. This may take a while.")
    emptyTile = findEmptyTile(start)
    startNode = Node(start,emptyTile,None,0,0, "")
    global nodesGenerated, nodesExpanded, nodesPopped
    maxFringeSize = 1
    fringe = []
    fringe.append(startNode)
    visited = []
    while fringe:
        node = fringe.pop() # pops the last element of the fringe
        nodesPopped += 1 
        if node.state == goal:
            printOutput(node, nodesGenerated, nodesPopped, maxFringeSize, nodesExpanded, file)
            break

        if node.state not in visited:
            visited.append(node.state)
            successors = findSuccessor(node)
            nodesExpanded += 1
            fringe+=successors
            nodesGenerated += len(successors)
            maxFringeSize = max(maxFringeSize, len(fringe))

            if file is not None:
                writeToFile(node, successors, fringe, visited, file)

def uniformCostSearch(start, goal, file=None):
    emptyTile = findEmptyTile(start)
    startNode = Node(start,emptyTile,None,0,0, "")
    global nodesGenerated, nodesExpanded, nodesPopped
    maxFringeSize = 1
    fringe = []
    fringe.append(startNode)
    visited = []
    while fringe: # loop goes until fringe is empty
        node = fringe.pop(0) # pops the first node out of the fringe
        nodesPopped += 1
        if node.state == goal: # if a goal state is reached
            printOutput(node, nodesGenerated, nodesPopped, maxFringeSize, nodesExpanded, file)
            break
        if node.state not in visited:
            visited.append(node.state) # added to nodes visited
            successors = findSuccessor(node) # finds the successors of the current node
            nodesExpanded += 1 
            fringe+=successors # adds the new node to the fring3
            fringe.sort(key=lambda x:x.cost) # sorts the fringe in ascending cost of the nodes
            nodesGenerated += len(successors) 
            maxFringeSize = max(maxFringeSize, len(fringe)) # finds the current max fringe size

            if file is not None:
                writeToFile(node, successors, fringe, visited, file)

def depthLimitedSearch(start, goal, limit, file=None):
    emptyTile = findEmptyTile(start)
    startNode = Node(start,emptyTile,None,0,0, "")
    global nodesGenerated, nodesExpanded, nodesPopped
    maxFringeSize = 1
    # print("Start G {} E {} P {} F {}".format(nodesGenerated, nodesExpanded, nodesPopped, maxFringeSize))
    fringe = []
    fringe.append(startNode)
    visited = []
    while fringe:
        node = fringe.pop() # pops the last element of the fringe
        nodesPopped += 1 
        if node.depth <= limit:
            if node.state == goal:
                printOutput(node, nodesGenerated, nodesPopped, maxFringeSize, nodesExpanded, file)
                return DLS.soln
            # check if a state was found at the same depth. if it was not, then can visit it again
            if [node.state, node.depth] not in visited:
                visited.append([node.state, node.depth])
                successors = findSuccessor(node)
                nodesExpanded += 1
                fringe+=successors
                nodesGenerated += len(successors)
                maxFringeSize = max(maxFringeSize, len(fringe))

                if file is not None:
                    writeToFile(node, successors, fringe,[], file)
    print("Cutoff reached at depth limit: ",limit)
    return DLS.cutoff
        
def iterativeDeepeningSearch(start, goal, file=None):
    global nodesGenerated, nodesExpanded, nodesPopped
    depth = 0
    while True:
        if file is not None:
            file.write("Depth limit: {}\n".format(depth))
        result = depthLimitedSearch(start, goal, depth, file)
        depth += 1
        if result == DLS.soln:
            break
        if result != DLS.cutoff:
            return result

# implements A* or Greedy dependng on the method as input. The method is used to select the appropriate heuristic
def informedSearch(start, goal, file, method):
    emptyTile = findEmptyTile(start)
    startNode = Node(start,emptyTile,None,0,0, "")
    global nodesGenerated, nodesExpanded, nodesPopped
    maxFringeSize = 1
    fringe = []
    fringe.append(startNode)
    visited = []
    while fringe:
        node = fringe.pop(0) # pop the front of the fringe
        nodesPopped += 1
        if node.state == goal:
            printOutput(node, nodesGenerated, nodesPopped, maxFringeSize, nodesExpanded, file)
            break
        
        if node.state not in visited:
            visited.append(node.state)
            successors = []
            successors = findSuccessor(node, goalState=goal, method=method)
            nodesExpanded += 1
            fringe+=successors # add successors to the fringe
            fringe.sort(key=lambda x:x.heuristic) # order all the successors in fringe in ascending values of their heuristic
            nodesGenerated += len(successors)
            maxFringeSize = max(maxFringeSize, len(fringe))
            if file is not None:
                writeToFile(node, successors, fringe, visited, file)

# heuristic for 8 puzzle problem
def heuristic(currentState, goalState):
    h = 0 # steps to move all tiles to goal state
    for i in range(3):
        for j in range(3):
            h += manhattanDistance(currentState, goalState, i, j)*currentState[i][j]
    return h

# calculates the manhattan distance to move a tile to its goal state
def manhattanDistance(currentState, goalState, r, c):
    for i in range(3):
        for j in range(3):
            if currentState[r][c] == goalState[i][j]:
                return abs(r-i) + abs(c-j)

# prints out the output after the program reaches the goal state.
def printOutput(node, nodesGenerated, nodesPopped, maxFringeSize, nodesExpanded, file=None):
    output = "Nodes popped: "+str(nodesPopped)+"\nNodes expanded: "+str(nodesExpanded)+"\nNodes Generated: "+str(nodesGenerated)+"\nMax Fringe Size: "+str(maxFringeSize)+"\nSolution Found at depth "+str(node.depth)+" with cost of "+str(node.cost)+""
    print(output)
    if file is not None:
        file.write(output)

    printStepsTakenToGoal(node, file)

# moves tiles to create next state for successor nodes
def moveTilesInPuzzle(state, original, emptyTile):
    rOrig, cOrig = original[0], original[1]
    r,c = emptyTile[0], emptyTile[1]
    tile = state[r][c]
    state[r][c] = state[rOrig][cOrig]
    state[rOrig][cOrig] = tile
    return state

# creates successor nodes
def createSuccessorNode(currentNode, newPos, method, goalState=None, direction="na"):
    emptyTile = currentNode.emptyTile
    row, col = emptyTile[0], emptyTile[1]
    newState = copy.deepcopy(currentNode.state)
    newState = moveTilesInPuzzle(newState, [row,col], [newPos[0], newPos[1]])
    h = 0
    if method == Method.greedy:
        h = heuristic(newState, goalState)
    elif method == Method.aStar:
        h = heuristic(newState, goalState) + currentNode.cost + currentNode.state[newPos[0]][newPos[1]]

    node = Node(newState, [newPos[0],newPos[1]], currentNode, currentNode.depth + 1, currentNode.cost + currentNode.state[newPos[0]][newPos[1]], "Move " + str(currentNode.state[newPos[0]][newPos[1]]) + " " +direction, h)
    return node

# finds and returns all the possible successor node from current node
def findSuccessor(currentNode: Node, goalState=None, method="None"):
    emptyTile = currentNode.emptyTile
    row, col = emptyTile[0], emptyTile[1]
    parentNode = currentNode.parentNode
    successorNodes = []
    # move down
    if row-1 >= 0 and col >= 0 and row-1 < 3 and col < 3 :
        successor = createSuccessorNode(currentNode, [row-1, col], method, goalState, direction="down")
        successorNodes.append(successor)

    # move right
    if row >= 0 and col-1 >= 0 and row < 3 and col-1 < 3 :
        successor = createSuccessorNode(currentNode, [row, col-1], method, goalState, direction="right")
        successorNodes.append(successor)

    # move up
    if row+1 >= 0 and col >= 0 and row+1 < 3 and col < 3 :
        successor = createSuccessorNode(currentNode, [row+1, col], method, goalState, direction="up")
        successorNodes.append(successor)

    # move left
    if row >= 0 and col+1 >= 0 and row < 3 and col+1 < 3 :
        successor = createSuccessorNode(currentNode, [row, col+1], method, goalState, direction="left")
        successorNodes.append(successor)

    return successorNodes

# this function prints steps to reach the goal state from start state
def printStepsTakenToGoal(lastNode:Node, file:None):
    output = []
    current = lastNode
    while current.parentNode != None:
        output.append(current.move)
        current = current.parentNode
    print("Steps: ")
    for move in reversed(output):
        print("\t",move)
        if file is not None:
            file.write("\n{}".format(move))
    if file is not None:
        print("Dump file with search trace is ready in sxa0536_assmt1 folder.")

# finds the tile with 0 on the matrix.
def findEmptyTile(matrix):
    for (i,row) in enumerate(matrix):
        for (j,tile) in enumerate(row):
            if tile == 0:
                return [i,j]

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    args = len(sys.argv)
    method = ""
    dumpFlag = ""
    if args == 3:
        method = "a*"
        dumpFlag = "false"
    elif args == 4:
        if sys.argv[3].lower() == "true" or sys.argv[3].lower() == "false":
            method = "a*"
            dumpFlag = sys.argv[3]
        else:
            dumpFlag = "false"
            method = sys.argv[3]
    elif args == 5:
        method, dumpFlag = sys.argv[3], sys.argv[4]
    else:
        print("Incorrect number of arguments.\nTry Run Command: python3 expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>")
        quit()

    startFile, goalFile = sys.argv[1], sys.argv[2]
    startState = createMatrix(startFile)
    goalState = createMatrix(goalFile)

    file = None
    if dumpFlag == "true":
        today = date.today()
        dateNow = today.strftime("%b-%d-%Y")
        currentTime = time.localtime()
        timeNow = time.strftime("%H:%M:%S",currentTime)
        file = open("trace-"+dateNow+"-"+timeNow, "w")
        file.write("Command-Line arguments: {} {} {} {}\n".format(startFile, goalFile, method, dumpFlag))
        file.write("Method selected: {}\nRunning {}\n\n".format(method, method))

    if method == Method.bfs.value:
        breadthFirstSearch(startState, goalState, file)
    elif method == Method.ucs.value:
        uniformCostSearch(startState, goalState, file)
    elif method == Method.dfs.value:
        depthFirstSearch(startState, goalState, file)
    elif method == Method.dls.value:
        limit = input('Enter Depth Limit: ')
        depthLimitedSearch(startState, goalState, int(limit), file)
    elif method == Method.ids.value:
        iterativeDeepeningSearch(startState, goalState, file)
    elif method == Method.greedy.value:
        informedSearch(startState,goalState,file, Method.greedy)
    else:
        informedSearch(startState,goalState,file, Method.aStar)

    if dumpFlag.lower == "true":
        file.close() 
