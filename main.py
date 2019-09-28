# import external libraries
import sys, os, re, shutil
# import my files
from analyzeFile import analyzeFile
from tsvPrint import tsvPrint
from textfield import textfield

def main(directory):
    files = os.listdir(directory)

    #try to create extraction directory, remove it if it exists
    folderName = "A1_extraction"
    try:
	    shutil.rmtree(folderName)
	    os.mkdir(folderName)
    except:
	    os.mkdir(folderName)

    for fileName in files:
        if fileName.endswith(".wiki"):
            print("Processing " + fileName)
            print("\tGathering facts...")
            fileObject = analyzeFile(os.path.join(directory, fileName))
            print("\tGathering evidence...")
            textfield(os.path.join(directory, fileName), fileObject)
            print("\tCreating tsv file...")
            tsvPrint(fileObject, folderName)
            print("Done processing " + fileName + "\n")

if __name__ == '__main__':
    #check command line arguments
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: ./main.py <directory of files for analysis>\n")