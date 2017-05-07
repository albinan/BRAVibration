from reader import fscanf, fileImportDialog
import os.path
import numpy as np
import scipy

def main():
    # CSV or TXT file specifications
    regExp = r'\d+|\d+\.\d+'
    headerlines = 0

    dataFileLoc = fileImportDialog('*.csv') #Interactive file import
    dataFileName, extension = os.path.splitext(dataFileLoc)
    if extension == '.csv' or extension == '.txt':
        data, header = fscanf(dataFileLoc, regExp, headerlines = 2)

    fs = 12500000
    signal_in = data[:, 1]
    signal_out = data[:, 0]

    


if __name__ == '__main__':
    main()
