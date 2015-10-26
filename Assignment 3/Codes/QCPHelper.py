# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 23:05:32 2015

@author: Xinjing Wei
@version: 1.10.2
"""


import sys                  # Needed for exit() function
import os                   # Required for path checking and directory creation
import os.path              # Required for path checking

'''
Print help message
'''
def helpMSG(mode = ""):
    print "\n"
    print " " * 15 + "*" * 5 + " Menu for QCP to CNF Program " + "*" * 5 + "\n"
    print "Basic usage: \n\t$ python " + mode + ".py qcp_file_path cnf_file_path"
    print "Print help message: \n\t$ python Main.py help"
    print "Example:\n\t$ python " + mode + ".py ../instances/q_10_01.qcp ../cnfs/q_10_01.cnf"
    print "Options:"
    print "\tqcp_file_path: the file path to the QCP instance file, has to end with \".qcp\""
    print "\tcnf_file_path: the file path where the output CNF file will be stored, has to end with \".cnf\""
    print "Note: \n\t- The order of the arguments don't matter"
    print "\t- Make sure the directory that will be sotring the cnf file already exists\n"
    print " " * 15 + "*" * 39 + "\n\n"
    sys.exit(0)

'''
Check command line arguments
'''
def checkArg(argv = [], mode = ""):
    if (len(argv) == 2) and (argv[1] == "help"):
        helpMSG(mode)
    elif len(argv) == 3:
        qcpFile = ""        # QCP instance file
        cnfFile = ""        # CNF file
        qcp = False         # Flag to check if the QCP file format is correct
        cnf = False         # Flag to check if the CNF file format is correct
        for i in range(1, len(argv)):
            if argv[i].endswith(".cnf"):
                cnf = True
                cnfFile = argv[i]
            if argv[i].endswith(".qcp"):
                qcp = True
                qcpFile = argv[i]

        if qcp and cnf:
            return (qcpFile, cnfFile)
    helpMSG(mode)


'''
Create Directories
'''
def createDir():
    try:
        if not os.path.exists("../CNF/ACD"):
            os.makedirs("../CNF/ACD")
        if not os.path.exists("../CNF/ABCD"):
            os.makedirs("../CNF/ABCD")
        if not os.path.exists("../CNF/BEF"):
            os.makedirs("../CNF/BEF")
    except OSError:
        if (not os.path.exists("../CNF/ACD")) or (not os.path.exists("../CNF/BEF")) or (not os.path.exists("../CNF/ABCD")):
            raise


'''
Read content from file

File content format:
order 3
1 2 *
* * 1
* * 2

'''
def readFile(fileName = ""):
    data = []
    if os.path.isfile(fileName) == False:
        sys.exit("No file \"" + fileName + "\" exists!\n")
    with open(fileName, "r") as f:
        data = [[str(n) for n in line.split()] for line in f]
    return data[1:]

'''
Convert string to integer if possible
'''
def convertToInt(i = 0, j = 0, s = ""):
    try:
        return int(s)
    except ValueError:
        sys.exit("Error, the element \"" + s + "\" in the cell (" + i + ", " + j + ") is not an integer\n")

'''
Unit clauses
'''
def unitClauses(data = []):
    unitClause = []         # Stores the unit clauses in the QCP instance
    qcpLen = len(data)      # The order of the QCP instance
    for i in range(0, qcpLen):
        for j in range(0, qcpLen):
            if not (data[i][j] == "."):
                n = convertToInt(i, j, data[i][j])
                unit = (i + 1) * 10000 + (j + 1) * 100 + n
                unitClause.append([unit])
    return unitClause

'''
Generate a set of clauses following property (a) based on the QCP's order.
Note that this is irrelavent to the content of the given QCP.
The CNF formula for (a) is as follow:
    AND(i,1,n)AND(j,1,n)OR(k,1,n)(C_{i,j,k})
'''
def propertyA(order = 0):
    propA = []              # Clauses for property (a)
    for i in range(1, order + 1):
        for j in range(1, order + 1):
            row = []
            for k in range(1, order + 1):
                row.append(i * 10000 + j * 100 + k)
            propA.append(row)
    return propA

'''
Generate a set of clauses following property (b) based on the QCP's order.
Note that this is irrelavent to the content of the given QCP.
The CNF formula for (b) is as follow:
    AND(i,1,n)AND(j,1,n)AND(k,1,n-1)AND(z,k+1,n)(-C_{i,j,k}, -C_{i,j,z})
'''
def propertyB(order = 0):
    propB = []              # Clauses for property (b)
    for i in range(1, order + 1):
        for j in range(1, order + 1):
            for k in range(1, order):
                for z in range(k + 1, order + 1):
                    negIJK = -(i * 10000 + j * 100 + k)
                    negIJZ = -(i * 10000 + j * 100 + z)
                    propB.append([negIJK, negIJZ])
    return propB

'''
Generate a set of clauses following property (c) based on the QCP's order.
Note that this is irrelavent to the content of the given QCP.
The CNF formula for (c) is as follow:
    AND(j,1,n)AND(k,1,n)AND(i,1,n-1)AND(z,j+1,n)(-C_{i,j,k}, C_{i,z,k})
'''
def propertyC(order = 0):
    propC = []              # Clauses for property (c)
    for j in range(1, order):
        for k in range(1, order + 1):
            for i in range(1, order + 1):
                for z in range(j + 1, order + 1):
                    negIJK = -(i * 10000 + j * 100 + k)
                    negIZK = -(i * 10000 + z * 100 + k)
                    propC.append([negIJK, negIZK])
    return propC

'''
Generate a set of clauses following property (d) based on the QCP's order.
Note that this is irrelavent to the content of the given QCP.
The CNF formula for (d) is as follow:
    AND(i,1,n)AND(k,1,n)AND(j,1,n-1)AND(z,i+1,n)(-C_{i,j,k}, C_{z,j,k})
'''
def propertyD(order = 0):
    propD = []              # Clauses for property (d)
    for i in range(1, order):
        for k in range(1, order + 1):
            for j in range(1, order + 1):
                for z in range(i + 1, order + 1):
                    negIJK = -(i * 10000 + j * 100 + k)
                    negZJK = -(z * 10000 + j * 100 + k)
                    propD.append([negIJK, negZJK])
    return propD

'''
Generate a set of clauses following property (e) based on the QCP's order.
Note that this is irrelavent to the content of the given QCP.
The CNF formula for (e) is as follow:
    AND(i,1,n)AND(k,1,n)OR(j,1,n)(C_{i,j,k})
'''
def propertyE(order = 0):
    propE = []              # Clauses for property (e)
    for i in range(1, order + 1):
        for k in range(1, order + 1):
            row = []
            for j in range(1, order + 1):
                row.append(i * 10000 + j * 100 + k)
            propE.append(row)
    return propE

'''
Generate a set of clauses following property (f) based on the QCP's order.
Note that this is irrelavent to the content of the given QCP.
The CNF formula for (f) is as follow:
    AND(j,1,n)AND(k,1,n)OR(i,1,n)(C_{i,j,k})
'''
def propertyF(order = 0):
    propF = []              # Clauses for property (f)
    for j in range(1, order + 1):
        for k in range(1, order + 1):
            row = []
            for i in range(1, order + 1):
                row.append(i * 10000 + j * 100 + k)
            propF.append(row)
    return propF


'''
CNF convertion of QCP using properties (a), (c) and (d)
'''
def cnfACD(data, dataLen):
    clauses = []              # Set of clauses for property (a),(c) and (d)
    clauses.extend(unitClauses(data))
    clauses.extend(propertyA(dataLen))
    clauses.extend(propertyC(dataLen))
    clauses.extend(propertyD(dataLen))
    return clauses

'''
CNF convertion of QCP using properties (a), (b), (c) and (d)
'''
def cnfABCD(data, dataLen):
    clauses = []              # Set of clauses for property (a),(b),(c) and (d)
    clauses.extend(unitClauses(data))
    clauses.extend(propertyA(dataLen))
    clauses.extend(propertyB(dataLen))
    clauses.extend(propertyC(dataLen))
    clauses.extend(propertyD(dataLen))
    return clauses

'''
CNF convertion of QCP using properties (b), (e) and (f)
'''
def cnfBEF(data, dataLen):
    clauses = []              # Set of clauses for property (b),(e) and (f)
    clauses.extend(unitClauses(data))
    clauses.extend(propertyB(dataLen))
    clauses.extend(propertyE(dataLen))
    clauses.extend(propertyF(dataLen))
    return clauses

'''
Write the given CNF formula to a file
'''
def writeToFile(clauses = [], qcpLen = 0, outputFileName = ""):
    with open(outputFileName, "w+") as outputFile:
        outputFile.write("p cnf " + str(qcpLen * 10101) + " " + str(len(clauses)) + "\n")
        for line in clauses:
            for element in line:
                outputFile.write(str(element) + " ")
            outputFile.write("0 ")
