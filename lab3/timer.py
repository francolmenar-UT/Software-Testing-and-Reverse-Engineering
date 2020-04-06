import sys, re
#fuction which adds a timer after which the program terminates
def timerInit(out):
    out.write("private long startTime = System.nanoTime();\n")
    out.write("private int endTime = 5;\n")

def timerExec(out):
    out.write("if ((System.nanoTime() - startTime) >= endTime * Math.pow(10,9)) {\n")
    out.write("System.out.println(\"Timer ended\" + endTime + \"minutes passed!\");\n")
    out.write("     return;\n")
    out.write("}\n")