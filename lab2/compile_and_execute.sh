#!/usr/bin/sh

python3 new_regex.py Problems/Problem1.java &&
cd Problems &&
javac -cp com.microsoft.z3.jar:. instProblem1.java &&
java -cp com.microsoft.z3.jar:. instProblem1 > /dev/null

