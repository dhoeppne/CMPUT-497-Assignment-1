# import external libraries
import sys, os
# import my files
import analyzeFile

def main(directory):
    files = os.listdir(directory)
    for file in files:
        if file.endswith(".wiki"):
            newFile = analyzeFile(file)

if __name__ == '__main__':
    #check command line arguments
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: ./create_index.py <directory of files for analysis>\n")