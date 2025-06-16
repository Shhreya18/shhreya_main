# **Automated Testing**
Automate the testing of commands for io_test1.py to improve efficiency and eliminate manual input.

##**The process**

__What was provided:__
- io_test1.py: The base tester file (later modified to import VirtualPort from virtual.py)
- /commands/: Folder containing .txt files, each with a set of commands to be tested

__What was then created:__
- virtual.py that acted as a virtual port
- txt.py file that acted as the main script to automate the testing 

##**Virtual.py**

__Goal:__
1. Mock implementation of a serial port to simulate the behaviour of a real serial port
2. To test without hardware
3. Allow interface compatability 

__Explanations:__
1. __init__() = intialises it to be open and creates an empty buffer to simulate response
2. write(self,data) = simulates sending data into the port
3. read(self,data) = simulates reading data from the port
4. close(self) = marks the port as closed and sends out message

##**Txt.py**

__Goal:__
1. Automate running .txt command files through io_test1.py
2. Ensure files are processed in numerical order (e.g., 1_version_id.txt before 2_status.txt)
3. Prompt the user to continue or exit after each test
4. Generate a summary report (output.txt) if the user chooses to exit 

__Explanations:__
1. Import os and subprocess
2. Give variables to the port, folder and test file
3. def extract_number(filename) = extracts the first part of the filename, which returns a number that is then used to ensure the files are run numerically
4. Loop through the folder and create a path for each file which is run on io_test1.py
5. Present the user with a choice
6. Depending on the choice, the next file is outputed or a report is generated. 
   


