#!/usr/bin/env bash
folder="true"
scripts="true"
############## Reading inputs ##############
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
  -h | --help) # Help command
    echo "Usage: "
    echo "-s"
    echo "-f"
    shift
    shift
    exit 1
    ;;
  -f) # Copying only folder
    scripts="false"
    shift
    ;;
  -s) # Copying only scripts
    folder="false"
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

docker_id=$(docker ps -aqf "ancestor=str_container") # Get docker's id
echo

if [ "${folder}" == "true" ]; then
  # Copying the folders
  docker cp ../zip/m158_LTL_buggy.zip "$docker_id":/home/str/
  docker cp ../zip/Problem1_buggy.zip "$docker_id":/home/str/
  docker cp ../zip/Problem11_buggy.zip "$docker_id":/home/str/

fi
if [ "${scripts}" == "true" ]; then
  # Copying the scripts
  docker cp run.sh "$docker_id":/home/str/astor/
  docker cp unzip.sh "$docker_id":/home/str/astor/
fi
