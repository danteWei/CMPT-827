# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 02:19:35 2015

@author: dante
version: 1.0
"""

import sys                   # Needed for exit() function and arguments
import QCPHelper as qcph     # Needed for property clauses and other functions

''' Read in command line arguments '''
(inF, outF) = qcph.checkArg(sys.argv, "MainABCD")

''' Read QCP instance '''
data = qcph.readFile(inF)
qcpLen = len(data)

''' Generate CNF formula '''
clauses = qcph.cnfABCD(data, qcpLen)

''' Write the CNF formula to a file '''
qcph.writeToFile(clauses, qcpLen, outF)