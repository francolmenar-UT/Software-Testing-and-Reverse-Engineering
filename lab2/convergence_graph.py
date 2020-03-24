import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel("time")
ax1.set_ylabel("visited branches")
ax1.set_title("Convergence Graph")

# Live animation of the convergence graph

def animate(i):
    getData = open(str(sys.argv),"r").read()
    dataArray = getData.split('\n')
    time = []
    visitedBr = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            time.append(int(x))
            visitedBr.append(int(y))
    ax1.clear()
    ax1.plot(time,visitedBr)
animateIt = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()