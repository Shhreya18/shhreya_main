# **Automated Testing**
Automate the testing for the commands being passed onto io_test1.py to improve the efficiency that would otherwise not be achieved had it been manually inputed 

##**The process**

What was provided:
- A base tester file titles io_test1.py (this was later editted to import the VirtualPort class from virtual.py)
- A folder containing txt files that had the commands that were to be automated into the test file

What was then created:
- virtual.py that acted as a virtual port
- txt.py file that acted as the main script to automate the testing 

##**Virtual.py**
Goal: 
1. Mock implementation of a serial port to simulate the behaviour of a real serial port
2. To test without hardware
3. Allow interface compatability 

Explanations: 
1. __init__() = intialises it to be open and creates an empty buffer to simulate response
2. write(self,data) = simulates sending data into the port
3. read(self,data) = simulates reading data from the port
4. close(self) = marks the port as closed and sends out message

##**Txt.py**

Goal:
1. Automate the txt files that were passed into io_test1.py as commands
2. Make sure they were passed on numerically (eg. 1_version_id) would be passed first
3. Upon the result of a test being outputted, users are presented a choice to move on to the next test or exit
4. By exiting, an text file titled output.txt is generated that creates a report with all the test results for each command

Explanations: 
1. Import os and subprocess
2. Give variables to the port, folder and test file
3. def extract_number(filename) = extracts the first part of the filename, which returns a number that is then used to ensure the files are run numerically
4. Loop through the folder and create a path for each file which is run on io_test1.py
5. Present the user with a choice
6. Depending on the choice, the next file is outputed or a report is generated. 
   


