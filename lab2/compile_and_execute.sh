#!/usr/bin/env bash

python3 new_regex.py Problems/Problem1.java &&
cd Problems &&
javac -cp com.microsoft.z3.jar:. instProblem1.java &&
java -cp com.microsoft.z3.jar:. instProblem1 Log true > /dev/null

