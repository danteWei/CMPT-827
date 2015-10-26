# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 23:05:32 2015

@author: Xinjing Wei
@version: 1.4
"""
import sys                   # Needed for exit() function and arguments
import QCPHelper as qcph     # Needed for property clauses and other functions

'''
(a) Each cell of the square contains a number in [n];
(b) No cell contains two distinct numbers;
(c) No row has two cells containing the same number;
(d) No column has two cells containing the same number;
(e) Every number in [n] appears in every row;
(f) Every number in [n] appears in every column.
'''

'''
Notice that if (a) and (c) are satisfied, then (b) and (e) is satisfied.
Similarly, if (a) and (d) are satisfied, then so is (b) and (f).

Therefore, we now have a minimal subset of the properties of (a) - (f):
(a) Each cell of the square contains a number in [n];
(c) No row has two cells containing the same number;
(d) No column has two cells containing the same number.
'''

arguments = sys.argv        # Stores command line arguments

''' Create desired directories for storing results '''
qcph.createDir()

''' Pre-stored orders of QCP instances '''
instanceOrder = [10, 16, 20, 24, 30, 32, 49]

''' Generate three CNF formulas for each of the QCP instances '''
for x in range(0, 7):
    for j in range(1, 5):
        clauses = []        # Stores all clauses of a given QCP instance
        
        qcpFile = "../instances/q_" + str(instanceOrder[x]) + "_0" + str(j) + ".qcp"
        
        data = qcph.readFile(qcpFile)       # QCP instance
        qcpLen = len(data)                  # Order of the QCP instance
        
        outputFileName = "../CNF/ACD/q_" + str(instanceOrder[x]) + "_0" + str(j) + "_ACD.cnf"
        clauses = qcph.cnfACD(data, qcpLen)
        qcph.writeToFile(clauses, qcpLen, outputFileName)
        
        outputFileName = "../CNF/ABCD/q_" + str(instanceOrder[x]) + "_0" + str(j) + "_ABCD.cnf"
        clauses = qcph.cnfABCD(data, qcpLen)
        qcph.writeToFile(clauses, qcpLen, outputFileName)
        
        outputFileName = "../CNF/BEF/q_" + str(instanceOrder[x]) + "_0" + str(j) + "_BEF.cnf"
        clauses = qcph.cnfBEF(data, qcpLen)
        qcph.writeToFile(clauses, qcpLen, outputFileName)
















