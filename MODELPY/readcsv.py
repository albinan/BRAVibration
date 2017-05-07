import numpy as np
import csv
import glob

def readcsv(csvFile, delim):
    print("readcsv(): Reading data from csv file" + csvFile)
    data = []
    with open(csvFile) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            a = [float(i) for i in row]
            data.append(a)
    data = np.asarray(data)
    return data


def readcsvDir(folderLoc, delim):
    print("readAll(): Looping through foler " + folderLoc)
    searchString = folderLoc + "\*.csv"
    print(searchString)
    csvfiles = glob.glob(searchString)
    print(csvfiles)
    data = []
    for f in enumerate(csvfiles):
        data.append(readcsv(f[1], delim))


    print("Data read")
    return data
