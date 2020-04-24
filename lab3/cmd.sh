#!/usr/bin/env bash
#/bin/sh

python3 new_regex.py Problems/Problem1.java
cd Problems &&
  javac -cp commons-lang3-3.10.jar:. instProblem1.java &&
  java -ea -cp commons-lang3-3.10.jar:. instProblem1 log true > /dev/null
