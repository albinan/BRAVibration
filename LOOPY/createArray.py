import numpy as np

def createArray(fs, isFreqency):
    f_list = fs.split(";")
    f = []
    shift = 0
    for string in f_list:
        inval = [float(i) for i in string.split(",")]
        if isFreqency:
            shift = inval[2]
        if inval[0] == inval[1]:
            f.extend([inval[0]])
        else:
            tmp_interval = np.arange(inval[0]-shift, inval[1] + inval[2]/2, inval[2])
            f.extend(tmp_interval)
    f = np.asarray(f)
    return(f)
