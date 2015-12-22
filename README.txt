The program was written in python, and converted to an executable so no additional libraries will need to be installed. The executable can only run properly using command prompt as there is no GUI provided. The program was developed using Python 2.7 on Windows 10.

In order to run the executable please use the following format:

Main.exe [file-path] [file-path] [file-path] #

[file-path] refers to the path of the file to a text file. The first [file-path] should be an input file that contains two datasets of known photos with the following format:

C:/Python27/photos/accordion/image_0001.jpg 0
C:/Python27/photos/accordion/image_0002.jpg 0
C:/Python27/photos/brain/image_0001.jpg 1
C:/Python27/photos/brain/image_0002.jpg 1

The second [file-path] should be an input file that contains a list of unknown photos with the following format:

C:/Python27/photos/unknown/image_0051.jpg
C:/Python27/photos/unknown/image_0052.jpg
C:/Python27/photos/unknown/image_0053.jpg
C:/Python27/photos/unknown/image_0054.jpg


The third [file-path] should be a blank text file where the program will be writing the results to. The last argument # is a number that should be 1, 2, or 3. The number refers to which algorithm that you would like the program to run.

Here's an example of calling the executable on command line:

ai-project\dist\Main.exe C:/Python27/ai-project/input.txt C:/Python27/ai-project/input2.txt C:/Python27/ai-project/output.txt 1



--------------------------------------------------------------

Written in Python. The first argument is a text file that contains a list of paths to images as well as an indicator of 0 or 1. The second argument is a text file that contains a list of paths to images. The third argument is the path to the output file. The fourth argument is a number that tells the application which algorithm to use.

Example of Command Line Execution

python.exe ai-project\Main.py C:/Python27/ai-project/input.txt C:/Python27/ai-project/input2.txt C:/Python27/ai-project/output.txt 2

Note - The implementation of all algorithms uses the python PIL library. 

Note - Although the executable will work on its own, in order to compile and successfully run algorithm #3, the additional following libraries are required:
	Numpy (>= 1.6.1)
	Scipy (>= 0.9)
	Scikit-learn
The libraries for Numpy and Scipy are attached. Scikit-learn can be aquired using the command "pip install scikit-learn"
