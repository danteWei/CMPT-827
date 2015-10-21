CMPT 827 Assignment 3 Documentation
====
**Note: this README file is written in the format of markdown file, to receive the best reading experience, please view it in a markdown viewer or on my [GitHub] [2].**

This program implements a Quasigroup Completion Problem (QCP) instance to CNF converter. It reads in a QCP instance file and output a CNF formula file that represents the instance. 

The program is implemented in Python 2.7, thus can be executed in any machine that supports Python 2.7. The program provides three choices of CNF formula generations. They are the following (you can find the properties in detail in [Property] (#property) section):

1. QCP to CNF using properties (a), (c) and (d)
2. QCP to CNF using properties (b), (e) and (f)
3. QCP to CNF using properties (a), (b), (c) and (d)

All the codes are stored in the folder "Codes/". The CNF files for all three choices of all QCP instances are not included because the folder is several giga bytes large. The SAT results are stored in the folder "Results/". I used [_minisat_] [1] as a SAT solver to do the experiments.

----
##Usage:##

To use the program, open a command line tool and "cd" to the "Codes/" directory. Then use command `Python <file name> <QCP file> <output CNF file>` to involke the program. You can also use `Python <file name> help` to print out the help message. Here is what is in the help message:

	Basic useage: 
		$ python <Main/MainACD/MainBEF/MainABCD>.py qcp_file_path cnf_file_path
	Print helper message: 
		$ python <Main/MainACD/MainBEF/MainABCD>.py help
	Example:
		$ python MainACD.py ../instances/q_10_01.qcp ../cnfs/q_10_01.cnf
	Options:
		qcp_file_path: the file path to the QCP instance file, has to end with ".qcp"
		cnf_file_path: the file path where the output CNF file will be stored, has to end with ".cnf"
	Note:
		- The order of the arguments don't matter
		- Make sure the directory that will be sotring the cnf file already exists
		- If you want to execute Main.py, you don't need to give it any command line arguments

----

##Structure and Functions:##

The structure of the program is as follows:

- Main.py: The program that converts **all** QCP instances into all three different CNF formulas
	- ACD: The formulas that uses properties (a), (c) and (d) are stored in the folder "CNF/ACD/"
	- BEF: The formulas that uses properties (b), (e) and (f) are stored in the folder "CNF/BEF/"
	- ABCD: The formulas that uses properties (a), (b), (c) and (d) are stored in the folder "CNF/ABCD/"
	- The file naming 
is as follow: "q\_order\_number.qcp" will be named as "q\_order\_number\_tpye.cnf" in folder "CNF/type/"
		- e.g. q\_10\_01.qcp will be named as q\_10\_01\_ACD.cnf in "CNF/ACD/" folder
- MainACD.py: The program that converts a given QCP instance into CNF formula using properties (a), (c) and (d)

- MainBEF.py: The program that converts a given QCP instance into CNF formula using properties (b), (e) and (f)

- MainABCD.py: The program that converts a given QCP instance into CNF formula using properties (a), (b), (c) and (d)

- QCPHelper.py: The program that helps generate CNF formulas, the functions implemented are as follows:
	- helpMSG(): 
		- prints help message
	- checkArg(): 
		- check if the command line arguments are valid
	- createDir(): 
		- create desired directories
	- readFile(): 
		- read contents from a QCP instance file
	- convertToInt(): 
		- tries to convert a string to integer 
		- will raise an exception if failed
	- unitClauses(): 
		- returns a list of unit clauses
	- propertyA() - propertyF():
		- each one returns a list of clauses generated using one of the properties
	- cnfACD():
		- returns a list of clauses generated using properties (a), (c) and (d)
	- cnfBEF():
		- returns a list of clauses generated using properties (b), (e) and (f)
	- cnfABCD():
		- returns a list of clauses generated using properties (a), (b), (c) and (d)
	- writeToFile():
		- write the generated formulas to a CNF file


##Property:##
The following is a list of properties:

>(a). Each cell of the square contains a number in [n];

>(b). No cell contains two distinct numbers;

>(c). No row has two cells containing the same number;

>(d). No column has two cells containing the same number;
>(e). Every number in [n] appears in every row;
>(f). Every number in [n] appears in every column.

----

###Xinjing Wei###
###Oct. 20, 2015###


[1]: https://github.com/niklasso/minisat
[2]: https://github.com/danteWei/CMPT-827/tree/master/Assignment%203

