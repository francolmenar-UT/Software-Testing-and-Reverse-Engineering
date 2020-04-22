#!/usr/bin/env bash

pythonPath="./new_regex.py" # Path to the Python file
seqPath="../../RERS/sequential/" # First Path
# Folders inside /sequential/
declare -a arrFolders=("SeqReachabilityRers2019/" "TrainingSeqReachRers2019/")
fileType=".java" # File type

for arrFolder_i in "${arrFolders[@]}"
do
  # Construct the path
  newPath=${seqPath}${arrFolder_i}

  printf %"s\n\n" "Going into ${newPath}"

  # Check all the folders of the path
  for file in "${newPath}"*;
  do
    IFS='/' read -ra clean <<< "$file" # Get the Problem name
    problem=${clean[${#clean[@]} - 1]} # Get the name of the problem - Element after last "/"
    newFilePath="${newPath}${problem}/" # Path to the file's folder

    echo ">>>> Path to the problem: ${newFilePath}"

    fileToRun=${problem}${fileType} # Next file to be executed

    # Check if the file exists
    if [ -f "${newFilePath}${fileToRun}" ]; then
      echo ">>>>>> Running ${fileToRun}"
      python "${pythonPath}" "${newFilePath}${fileToRun}" # Run the file
      printf %"s\n\n" ">>>>>> Done"
    fi
  done
done

# TrainingSeqReachRers2019 lab1
# SeqReachabilityRers2019 lab2, lab3