#/bin/sh

# Find all files named Problem<number>.java in the directories TrainingSeqLtlRers2019
# and TrainingSeqReachRers2019 and execute the python script on them
find RERS/sequential/TrainingSeq*/*/Problem*.java -exec python3 new_regex.py {} \;
