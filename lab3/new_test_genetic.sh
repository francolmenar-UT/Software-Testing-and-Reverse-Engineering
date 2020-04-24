#!/usr/bin/env bash

pythonPath="./new_regex.py" # Path to the Python file
logPath="Logs/"             # Log folder
seqPath="sequential/"       # First Path
fileType=".java"            # File type
# Files not to be executed
notWorking="sequential/TrainingSeqLtlRers2019/Problem1/Problem1.java"

declare -a arrFolders=() # Array for the folders to be executed
folder1="TrainingSeqLtlRers2019/"
folder2="SeqLtlRers2019/"
folder3="SeqReachabilityRers2019/"
folder4="TrainingSeqReachRers2019/"

DEPTH="true" # True by default
timeout="3s" # 3 s of execution as default timeout

declare -a pop_size=(5 10 20 50 100)
declare -a mutation=(0.01 0.05 0.1 0.2 0.5)

repetitions=3
best=0
best_pop=0
best_mut=0

############## Reading inputs ##############
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -d | --depth) # DEPTH_FIRST_SEARCH input
    if [ "${2}" != "true" ] && [ "${2}" != "false" ]; then
      echo "Wrong usage of -d [ true || false ]"
      exit 1
    else
      DEPTH="$2"
    fi
    shift
    shift
    ;;
    -h | --help) # Help command
    echo "Usage: "
    echo "-d | --depth [ true || false ]"
    echo "-f | --folder [ 1,2,3,4 || 1,3,4 || 1,2 ...]"
    echo "-t | --timeout [0-9]+[smh]"
    shift
    shift
    exit 1
    ;;
  -f | --folder) # Folder lab to be executed
    IFS=',' read -ra FOLDER <<<"$2" # Separate by ","
    shift                           # past argument
    shift                           # past value
    ;;
  -t | --timeout)                           # Timeout
    if [ -z "$2" ] || ! [[ "$2" =~ ^[0-9]+[smh]$ ]]; then
      echo "Wrong usage of -t [0-9]+[smh]"
      exit 1
    else
      timeout="$2"
    fi
    shift
    shift
    ;;
  *) # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift
    ;;
  esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ -n $1 ]]; then
  echo "Last line of file specified as non-opt/last argument:"
  exit 1
fi

############## Processing the parameters ##############
####### RERS' Folders to be executed #######
if [ ${#FOLDER[@]} -ge 1 ]; then
  for folder_i in "${FOLDER[@]}"; do
    case $folder_i in
    1 | ${folder1}) # Folder to be executed
      arrFolders+=("${folder1}")
      shift
      shift
      ;;
    2 | ${folder2}) # Folder to be executed
      arrFolders+=("${folder2}")
      shift
      shift
      ;;
    3 | ${folder3}) # Folder to be executed
      arrFolders+=("${folder3}")
      shift
      shift
      ;;
    4 | ${folder4}) # Folder to be executed
      arrFolders+=("${folder4}")
      shift
      shift
      ;;
    *)
      echo "Wrong usage of -f [ 1,2,3,4 || 1,3,4 || 1,2 ...]"
      exit 1
      ;;
    esac
  done
else # By default all of the folders are executed
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
      echo "> Running new_regex.py"
      python "${pythonPath}" "${newFilePath}${fileToRun}" # Run the python file

      echo "> Compiling inst${fileToRun}"
      javac -cp commons-lang3-3.10.jar:. "${newFilePath}inst${fileToRun}" 2>/dev/null >/dev/null

      InslogPath=$logPath$(echo "${newFilePath}inst${problem}" | tr "/" -)"-log" # Create path to Log
      for size in "${pop_size[@]}"; do
        for mut in "${mutation[@]}"; do
          echo "testing pop: ${size} mut: ${mut}"
          res=0
          for ((i = 0; i < repetitions; i++)); do
            timeout --preserve-status -s INT "${timeout}" java -cp commons-lang3-3.10.jar:"${newFilePath}"  "inst${problem}" "$InslogPath" "${DEPTH}" ${size} ${mut} >/dev/null 2>/dev/null
            ((res = res + $?))
          done
          ((res = ${res} / ${repetitions}))
          echo "score: ${res}"
          echo ""
          if [[ ${res} > ${best} ]]; then
            best=${res}
            best_pop=${size}
            best_mut=${mut}
          fi
        done
      done

    fi
  done
  printf "\n\n"
done

echo "Best values"
echo "  Population size: ${best_pop}"
echo "  Best mutation: ${best_mut}"
echo "  Score: ${best}"
