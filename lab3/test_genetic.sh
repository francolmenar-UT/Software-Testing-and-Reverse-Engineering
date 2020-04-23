#!/usr/bin/env bash

declare -a pop_size=(5 10 20 50 100)
declare -a mutation=(0.01 0.05 0.1 0.2 0.5)

execution_time=3
repetitions=3

best=0
best_pop=0
best_mut=0

python3 new_regex.py Problems/Problem1.java
javac -cp commons-lang3-3.10.jar:. Problems/instProblem1.java 2> /dev/null > /dev/null

for size in "${pop_size[@]}"
do
   for mut in "${mutation[@]}"
   do
        echo "testing pop: ${size} mut: ${mut}"
        res=0
        for ((i=0;i<repetitions;i++)) do
            timeout --preserve-status -s INT ${execution_time}s java -cp commons-lang3-3.10.jar:Problems/ instProblem1 log true ${size} ${mut} > /dev/null 2>/dev/null
            ((res=res+$?))
        done
        ((res=${res}/${repetitions}))
        echo "score: ${res}"
        echo ""
        if [[ ${res} > ${best} ]]
        then
            best=${res}
            best_pop=${size}
            best_mut=${mut}
        fi
   done
done

echo "Best values"
echo "  Population size: ${best_pop}"
echo "  Best mutation: ${best_mut}"
echo "  Score: ${best}"
