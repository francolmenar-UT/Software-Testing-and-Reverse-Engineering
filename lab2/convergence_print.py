import matplotlib.pyplot as plt
import time
import sys

# Run this program like: python convergence_print.py log.txt
# Or: python convergence_print.py log1.txt log2.txt

fig = plt.figure()
ax1 = fig.add_subplot(111)

# set legend
legend1 = "Genetic" #name of argv[1]
legend2 = "SetSolver" #name of argv[2]

#set labels ans title
ax1.set_xlabel('time (s)')
ax1.set_ylabel("visited branches")
ax1.set_title("Convergence Graph")

# Print out the logfile
getData = open(str(sys.argv[1]),"r").read()
dataArray = getData.split('\n')
time = []
visitedBr = []
for eachLine in dataArray:
    if len(eachLine)>1 and "," in eachLine:
        x,y = eachLine.split(',')
        time.append(int(x)/10**9) #convert from nanoseconds to seconds
        visitedBr.append(int(y))

if(len(sys.argv) == 3):
    getData2 = open(str(sys.argv[2]),"r").read()
    dataArray2 = getData2.split('\n')
    time2 = []
    visitedBr2 = []
    for eachLine in dataArray:
        if len(eachLine)>1 and "," in eachLine:
            x2,y2 = eachLine.split(',')
            time2.append(int(x2)/10**9) #convert from nanoseconds to seconds
            visitedBr2.append(int(y2))

ax1.plot(time,visitedBr,'r', label = legend1)
if(len(sys.argv) == 3):
    ax1.plot(time2,visitedBr2,'b',label = legend2)

ax1.legend()
fig.savefig(str(sys.argv[1].split(".")[0])+'.png')