import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
import os
import re

#class for parsing input arguments
class Arguments:
    pass

def getFiles(path):
    directories = ["",""]
    files = ["",""]
    obj = os.scandir(path)
    count = 0
    for entry in obj : 
        if entry.is_dir():
            #get name of directory
            directories[count] = entry.name
            #get all filenames in the directory
            files[count] = glob.glob(path + "\\" + entry.name + '\*.txt')
            count +=1
    return directories, files

def readfiles(files):
    data = []
    c1 = "Elapsed Time"
    c2 = "Covered Branches"
    for file in files:
        data_tmp = pd.read_csv(file, sep=",", header=None, names=[c1, c2])
        #round numbers and convert them to ms
        data_tmp[c1] = round(data_tmp[c1].astype(float) / 1e6) 
        # insert zero in both columns at index 1
        line = pd.DataFrame({c1: 0, c2: 0}, index=[0])
        data_tmp = pd.concat([data_tmp.iloc[:0], line, data_tmp.iloc[0:]]).reset_index(drop=True)
        data.append(data_tmp)
    return data

def getProblemNameandRersType(files):
    problems=[]
    #find the RERS type and the problem number
    for file in files:
        problems.append([re.search('2-(.*)2019-',file).group(1),re.search('inst(.*)-log.txt',file).group(1)])
    return problems

def createPlots(type,problem, data, numberlabs):
    #sample_rate = 1
    #data = data.iloc[::sample_rate, :] #reduces the number of datapoints
    fig, ax = plt.subplots()
    labels = [" (rndm-gen)", " (conc/symb)", " (gener)"]
    #plot the data
    for i in range(0,numberlabs):
        for j in range(0,len(data[i])):
            search = "BFS"
            if (type[i][j] == "dTrue"):
                search = "DFS"
            ax.plot(data[i][j]["Elapsed Time"], data[i][j]["Covered Branches"], label=search + labels[i], linewidth=0.7)
        # set plot ticks to be a timestamp and that there are always 7 ticks (7 fits well to the plot size)
        #plt.xticks(np.arange(0, data.shape[0], step=(data.shape[0]/6)-1),data["Elapsed Time"])

    #set title and axis labels
    ax.set_title(problem[1] + " " + problem[0])
    ax.legend()
    ax.set_ylabel("Branches")
    ax.set_xlabel("time (ms)")
    fig.savefig("graphs/"+ problem[1] + "_" + problem[0] + ".png")

parser = argparse.ArgumentParser(description='Create graphs of test results.')
parser.add_argument('-src1', help="path of the logfiles of the first lab", required=True, nargs=1, dest="source1")
parser.add_argument('-src2', help="path of the logfiles of the second lab", required=True, nargs=1, dest="source2")
parser.add_argument('-src3', help="path of the logfiles of the third lab", required=True, nargs=1, dest="source3")

parser.parse_args(namespace=Arguments)

# variables for the data directories
path1 = Arguments.source1[0]
path2 = Arguments.source2[0]
path3 = Arguments.source3[0]

# get files and the name of the folder where they are stored
# dir = the different options (BFS or DFS)
dir1, fil1 = getFiles(path1)
dir2, fil2 = getFiles(path2)
dir3, fil3 = getFiles(path3)

# get the problem name and the corresponding RERS type
# problems = the problems and their type
problems1Type1 = getProblemNameandRersType(fil1[0])
problems1Type2 = getProblemNameandRersType(fil1[1])

problems2Type1 = getProblemNameandRersType(fil2[0])
problems2Type2 = getProblemNameandRersType(fil2[1])

problems3Type1 = getProblemNameandRersType(fil3[0])
problems3Type2 = getProblemNameandRersType(fil3[1])

#read files of the different labs/directories
data11 = readfiles(fil1[0])
data12 = readfiles(fil1[1])

data21 = readfiles(fil2[0])
data22 = readfiles(fil2[1])

data31 = readfiles(fil3[0])
data32 = readfiles(fil3[1])

# create a graph for every problem
for i in range(0, len(fil1[0])):
    tdata = [[data11[i], data12[i]],[data21[i], data22[i]], [data31[i], data32[i]]]
    createPlots([dir1,dir2,dir3],problems1Type1[i],tdata,3)