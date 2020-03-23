#!/usr/bin/env bash
cd Problems &&
javac -cp com.microsoft.z3.jar:. instProblem1.java &&
java -cp com.microsoft.z3.jar:. instProblem1 > /dev/null