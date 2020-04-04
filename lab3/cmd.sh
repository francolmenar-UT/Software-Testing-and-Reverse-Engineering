#!/usr/bin/env bash
#/bin/sh


python3 new_regex.py Problems/Problem1.java
cd Problems &&
javac  instProblem1.java &&
java  instProblem1 > /dev/null
