#!/usr/bin/env bash

pythonPath="./new_regex.py"      # Path to the Python file
seqPath="../../RERS/sequential/" # First Path

notWorking="../../RERS/sequential/TrainingSeqLtlRers2019/Problem1/Problem1.java"

declare -a arrFolders=() # Array for the folders to be executed
folder1="TrainingSeqLtlRers2019/"
folder2="SeqLtlRers2019/"
folder3="SeqReachabilityRers2019/"
folder4="TrainingSeqReachRers2019/"

fileType=".java" # File type

############## Reading inputs ##############
POSITIONAL=()
while [[ $# -gt 0 ]]; do # Reading inputs
  key="$1"

  case $key in
  -f | --folder) # Folder lab to be executed
    IFS=',' read -ra FOLDER <<<"$2" # Separate by ","
    shift                           # past argument
    shift                           # past value
    ;;
  -h | --help)                           # TODO Add a help command
    HELP="$2"
    shift # past argument
    shift # past value
    ;;
  *) # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift              # past argument
    ;;
  esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ -n $1 ]]; then
  echo "Last line of file specified as non-opt/last argument:"
  tail -1 "$1"
fi

############## Processing the parameters ##############
if [ ${#FOLDER[@]} -ge 1 ]; then
  for folder_i in "${FOLDER[@]}"; do
    case $folder_i in
    1 | ${folder1}) # Folder lab to be executed
      arrFolders+=("${folder1}")
      shift # past argument
      shift # past value
      ;;
    2 | ${folder2}) # Folder lab to be executed
      arrFolders+=("${folder2}")
      shift # past argument
      shift # past value
      ;;
    3 | ${folder3}) # Folder lab to be executed
      arrFolders+=("${folder3}")
      shift # past argument
      shift # past value
      ;;
    4 |${folder4}) # Folder lab to be executed
      arrFolders+=("${folder4}")
      shift # past argument
      shift # past value
      ;;
    esac
  done
else
  arrFolders+=("${folder1}" "${folder2}" "${folder3}" "${folder4}")
fi

############## Runing the RERS programs ##############
for arrFolder_i in "${arrFolders[@]}"; do
  # Construct the path
  newPath=${seqPath}${arrFolder_i}
  printf %"s\n\n" "${newPath}"

  # Check all the folders of the path
  for file in "${newPath}"*; do
    IFS='/' read -ra clean <<<"$file"   # Get the Problem name
    problem=${clean[${#clean[@]} - 1]}  # Get the name of the problem - Element after last "/"
    newFilePath="${newPath}${problem}/" # Path to the file's folder

    fileToRun=${problem}${fileType} # Next file to be executed

    # Check if the file exists
    if [ -f "${newFilePath}${fileToRun}" ] && [ "${newFilePath}${fileToRun}" != $notWorking ]; then
      echo "${newFilePath}${fileToRun}"
      python "${pythonPath}" "${newFilePath}${fileToRun}" # Run the file
    fi
  done
  printf "\n\n"
done
