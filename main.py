# import external libraries
import sys, os, re
# import my files
from analyzeFile import analyzeFile
from tsvPrint import tsvPrint
from textfield import textfield

def main(directory):
    files = os.listdir(directory)
    for fileName in files:
        if fileName.endswith(".wiki"):
            fileObject = analyzeFile(os.path.join(directory, fileName))
            tsvPrint(fileObject)

if __name__ == '__main__':
    #check command line arguments
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: ./main.py <directory of files for analysis>\n")