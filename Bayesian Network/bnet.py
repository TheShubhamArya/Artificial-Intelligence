# Shubham Arya 1001650536
# CSE 5360 Artificial Intelligence 1
# Assignment 3 Bayesian Networks
import sys

def getFileData(filename):
    file = open(filename,'r')
    file_data= []
    for line in file.readlines():
        if line == "END OF FILE":
            break
        file_data.append([int(x) for x in line.split()])
    return file_data

def findBTrue(fileData):
    bTrue = 0
    for data in fileData:
        if data[0] == 1:
            bTrue += 1
    return bTrue

def findCTrue(fileData):
    cTrue = 0
    for data in fileData:
        if data[2] == 1:
            cTrue += 1
    return cTrue

def findGTrue(fileData):
    g_bTrue = 0 # G true, given B true
    gF_bTrue = 0 # G false, given B true
    g_bFalse = 0 # G true, given B false
    gF_bFalse = 0 # G false, given B false
    for data in fileData:
        if data[0] == 1:
            if data[1] == 1:
                g_bTrue += 1
            else:
                gF_bTrue += 1
        elif data[0] == 0:
            if data[1] == 1:
                g_bFalse += 1
            else: 
                gF_bFalse += 1
    return g_bTrue, gF_bTrue, g_bFalse, gF_bFalse

def findFTrue(fileData):
    f_gTrue_cTrue, fF_gTrue_cTrue = 0, 0
    f_gTrue_cFalse, fF_gTrue_cFalse = 0, 0
    f_gFalse_cTrue, fF_gFalse_cTrue = 0, 0
    f_gFalse_cFalse, fF_gFalse_cFalse = 0, 0
    for data in fileData:
        if data[1] == 1 and data[2] == 1:
            if data[3] == 1:
                f_gTrue_cTrue += 1
            else: 
                fF_gTrue_cTrue += 1
        elif data[1] == 1 and data[2] == 0:
            if data[3] == 1:
                f_gTrue_cFalse += 1
            else:
                fF_gTrue_cFalse += 1
        elif data[1] == 0 and data[2] == 1:
            if data[3] == 1:
                f_gFalse_cTrue += 1
            else: 
                fF_gFalse_cTrue += 1
        elif data[1] == 0 and data[2] == 0: 
            if data[3] == 1:
                f_gFalse_cFalse += 1
            else: 
                fF_gFalse_cFalse += 1
    return f_gTrue_cTrue, fF_gTrue_cTrue, f_gTrue_cFalse, fF_gTrue_cFalse, f_gFalse_cTrue, fF_gFalse_cTrue, f_gFalse_cFalse, fF_gFalse_cFalse

def getBayesianNetwork(fileData):
    bTrue = findBTrue(fileData)
    bayesianNetwork.append([bTrue/365, (365 - bTrue)/365])

    cTrue = findCTrue(fileData)
    bayesianNetwork.append([cTrue/365, (365 - cTrue)/365])

    g_bTrue, gF_bTrue, g_bFalse, gF_bFalse = findGTrue(fileData)
    G_bTrue = g_bTrue + gF_bTrue
    G_bFalse = g_bFalse + gF_bFalse
    bayesianNetwork.append([[g_bTrue/G_bTrue ,gF_bTrue/G_bTrue], [g_bFalse/G_bFalse, gF_bFalse/G_bFalse]])

    f_gTrue_cTrue, fF_gTrue_cTrue, f_gTrue_cFalse, fF_gTrue_cFalse, f_gFalse_cTrue, fF_gFalse_cTrue, f_gFalse_cFalse, fF_gFalse_cFalse = findFTrue(fileData)
    bayesianNetwork.append([
        [f_gTrue_cTrue/(f_gTrue_cTrue + fF_gTrue_cTrue), fF_gTrue_cTrue/(f_gTrue_cTrue + fF_gTrue_cTrue)],
        [f_gTrue_cFalse/(f_gTrue_cFalse + fF_gTrue_cFalse), fF_gTrue_cFalse/(f_gTrue_cFalse + fF_gTrue_cFalse)],
        [f_gFalse_cTrue/(f_gFalse_cTrue + fF_gFalse_cTrue), fF_gFalse_cTrue/(f_gFalse_cTrue + fF_gFalse_cTrue)],
        [f_gFalse_cFalse/(f_gFalse_cFalse + fF_gFalse_cFalse), fF_gFalse_cFalse/(f_gFalse_cFalse + fF_gFalse_cFalse)]
        ])
    return bayesianNetwork

def printTask1(bayesianNetwork):
    print("               P(b)            P(not b)")
    print("P(B): ", bayesianNetwork[0][0],"   ", bayesianNetwork[0][1])

    print("\n--------------------------------------------------------------\n")
    print("               P(c)            P(not c)")
    print("P(C): ", bayesianNetwork[1][0],"   ", bayesianNetwork[1][1])

    print("\n--------------------------------------------------------------\n")
    print("             P(g|b)            P(not g|b)")
    print("B=T: ", bayesianNetwork[2][0][0],"   ", bayesianNetwork[2][0][1])
    print("B=F: ", bayesianNetwork[2][1][0],"   ", bayesianNetwork[2][1][1])

    print("\n--------------------------------------------------------------\n")
    print("                 P(f|g,c)            P(not f|g,c)")
    print("G=T | F=T: ", bayesianNetwork[3][0][0],"   ", bayesianNetwork[3][0][1])
    print("G=T | F=F: ", bayesianNetwork[3][1][0],"   ", bayesianNetwork[3][1][1])
    print("G=F | F=T: ", bayesianNetwork[3][2][0],"   ", bayesianNetwork[3][2][1])
    print("G=F | F=F: ", bayesianNetwork[3][3][0],"   ", bayesianNetwork[3][3][1])
    print("\n")

def networkIndex(text):
    return 0 if text == "t" else 1
    
def indexForG(text):
    if text == "tt":
        return 0
    elif text == "tf":
        return 1
    elif text == "ft":
        return 2
    elif text == "ff":
        return 3
    
def getValuesFromNetwork(bayesianNetwork, B, C, G, F):
    # bayesianNetwork[0] is B, bayesianNetwork[1] is C, bayesianNetwork[2] is G|B, bayesianNetwork[3] is F|G,C
    P_b = bayesianNetwork[0][networkIndex(B)]
    P_c = bayesianNetwork[1][networkIndex(C)]
    P_g_b = bayesianNetwork[2][networkIndex(B)][networkIndex(G)]
    P_f_g_c = bayesianNetwork[3][indexForG(G+C)][networkIndex(F)]
    return P_b, P_c, P_g_b, P_f_g_c

def calculateProbability(bayesianNetwork, b, g, c, f):#, bPresent, gPresent, cPresent, fPresent):
    # Gets the binary numbers from 0 to total combinations possible
    # converts the 1s to 't' and 0 to 'f', where numbers range from 0000 to 1111, so they go from ffff to tttt.
    # The digits correspond to B, G, C, F going from left to right, giving all combinations for 4 variables.
    # Then a check is done to see if the variable is provided in the command line argument, and if it is equal
    # if it is, then it means that the combination is used for probability distribution calculation.
    sum = 0
    number_of_combinations = pow(2, len(bayesianNetwork))
    for i in range(number_of_combinations):
        binary_num = bin(i)[2:].zfill(len(bayesianNetwork)) # gets binary for number and makes it of size 4.
        B, G, C, F = ''.join(['t' if digit == '1' else 'f' for digit in binary_num]) 
        if (b is not None and b != B) or (g is not None and g != G) or (c is not None and c != C) or (f is not None and f != F):
            continue
    
        P_b, P_c, P_g_b, P_f_g_c = getValuesFromNetwork(bayesianNetwork=bayesianNetwork, B=B, C=C, G=G, F=F)
        P = P_b * P_c * P_g_b * P_f_g_c
        sum += P
    return sum

# finds the fixed variable, i.e., variables that are known or given by the user.
def findFixedVariable(array):
    b, c, g, f = None, None, None, None
    givenList = []
    conflict = False # this variable checks if the query variables and evidence have conflicts like P(Bt | Bf) = 0
    for arr in array:
        if givenList:
            givenList.append(arr.lower())
            if (b is not None and "b" == arr[0].lower() and b != arr[-1].lower()) or (c is not None and "c" == arr[0].lower() and c != arr[-1].lower()) or (g is not None and "g" == arr[0].lower() and g != arr[-1].lower()) or (f is not None and "f" == arr[0].lower() and f != arr[-1].lower()):
                conflict = True
                return b, c, g, f, givenList, conflict
        
        if "b" == arr[0].lower():
            b = arr[-1].lower()
        elif "c" == arr[0].lower():
            c = arr[-1].lower()
        elif "f" == arr[0].lower():
            f = arr[-1].lower()
        elif "given" in arr:
            givenList.append('empty')
        elif "g" == arr[0].lower():
            g = arr[-1].lower()

    return b, c, g, f, givenList, conflict

if __name__ == "__main__":
    args = len(sys.argv)
    bayesianNetwork = []

    if args >= 2:
        print("TASK 1\n")
        filename = sys.argv[1]
        fileData = getFileData(filename)
        bayesianNetwork = getBayesianNetwork(fileData)
        printTask1(bayesianNetwork)

    if args == 6 and not 'given' in sys.argv: 
        b, c, g, f, _, _ = findFixedVariable(sys.argv[2:])
        P_b, P_c, P_g_b, P_f_g_c = getValuesFromNetwork(bayesianNetwork=bayesianNetwork, B=b, C=c, G=g, F=f)
        P = P_b * P_c * P_g_b * P_f_g_c # P(B, G, C, F) = P(B)*P(G|B)*P(C)*P(F|G,C)
        print("TASK 2:\nP(B=",b,", C=",c,", G=",g,", F=",f,")= ", P_b," x ",P_c," x ", P_g_b, " x ", P_f_g_c)
        print("P(B=",b,", C=",c,", G=",g,", F=",f,")= ", P)
    elif args > 2 or 'given' in sys.argv: 
        b, c, g, f, givenList, conflict = findFixedVariable(sys.argv[2:])
        if conflict:
            print("TASK 3\nP = 0")
        else:
            P_numerator = calculateProbability(bayesianNetwork, b, g, c, f)
            B, C, G, F, _, conflict= findFixedVariable(givenList)
            P_denominator = calculateProbability(bayesianNetwork, B, G, C, F)
            P = P_numerator / P_denominator
            print("TASK 3\nP = ",P_numerator," / ",P_denominator," = ", P)
    