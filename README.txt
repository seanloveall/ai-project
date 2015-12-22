Written in Python. The first argument is a text file that contains a list of paths to images as well as an indicator of 0 or 1. The second argument is a text file that contains a list of paths to images. The third argument is the path to the output file. The fourth argument is a number that tells the application which algorithm to use.

Example of Command Line Execution

python.exe ai-project\Main.py C:/Python27/ai-project/input.txt C:/Python27/ai-project/input2.txt C:/Python27/ai-project/output.txt 2

Note - The implementation of all algorithms uses the python PIL library. 

Note - Although the executable will work on its own, in order to compile and successfully run algorithm #3, the additional following libraries are required:
	Numpy (>= 1.6.1)
	Scipy (>= 0.9)
	Scikit-learn
The libraries for Numpy and Scipy are attached. Scikit-learn can be aquired using the command "pip install scikit-learn"
