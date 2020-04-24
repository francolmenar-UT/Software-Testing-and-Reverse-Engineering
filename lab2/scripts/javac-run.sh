#!/usr/bin/env bash
# Addapt of run.sh to run just javac

seqPath="sequential/"       # First Path
fileType=".java"            # File type
# Files not to be executed
declare -a notWorking=("sequential/TrainingSeqLtlRers2019/Problem1/Problem1.java"
"sequential/SeqLtlRers2019/Problem4/Problem4.java" "sequential/SeqLtlRers2019/Problem5/Problem5.java" "sequential/SeqLtlRers2019/Problem6/Problem6.java" "sequential/SeqLtlRers2019/Problem7/Problem7.java" "sequential/SeqLtlRers2019/Problem8/Problem8.java" "sequential/SeqLtlRers2019/Problem9/Problem9.java"
"sequential/SeqReachabilityRers2019/Problem12/Problem12.java" "sequential/SeqReachabilityRers2019/Problem13/Problem13.java"  "sequential/SeqReachabilityRers2019/Problem14/Problem14.java"  "sequential/SeqReachabilityRers2019/Problem15/Problem15.java"  "sequential/SeqReachabilityRers2019/Problem16/Problem16.java"   "sequential/SeqReachabilityRers2019/Problem17/Problem17.java"    "sequential/SeqReachabilityRers2019/Problem18/Problem18.java"    "sequential/SeqReachabilityRers2019/Problem19/Problem19.java"
"sequential/TrainingSeqReachRers2019/Problem12/Problem12.java" "sequential/TrainingSeqReachRers2019/Problem13/Problem13.java")

declare -a arrFolders=() # Array for the folders to be executed
folder1="TrainingSeqLtlRers2019/"
folder2="SeqLtlRers2019/"
folder3="SeqReachabilityRers2019/"
folder4="TrainingSeqReachRers2019/"

verbose="false" # Print output or not

############## Reading inputs ##############
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
  -h | --help) # Help command
    echo "Usage: "
    echo "-f | --folder [ 1,2,3,4 || 1,3,4 || 1,2 ...]"
    echo "-v | --verbose"
    shift
    shift
    exit 1
    ;;
  -f | --folder) # Folder lab to be executed
    IFS=',' read -ra FOLDER <<<"$2" # Separate by ","
    shift                           # past argument
    shift                           # past value
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
    if [ -f "${newFilePath}${fileToRun}" ] && [[ ! " ${notWorking[@]} " =~ " ${newFilePath}${fileToRun} " ]]; then
      echo "> Compiling inst${fileToRun}"
      javac -cp com.microsoft.z3.jar:. "${newFilePath}inst${fileToRun}"
    fi
  done
  printf "\n\n"
done
