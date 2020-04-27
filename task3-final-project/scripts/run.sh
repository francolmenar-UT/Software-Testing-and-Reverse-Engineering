#!/usr/bin/env bash
OUTPUT_FOLDER="output_astor/"

declare -a arr_problems=("Problem1_buggy" "Problem11_buggy" "m158_LTL_buggy")
declare -a arr_generations=("500" "750" "1000")
declare -a arr_populations=("20" "25" "30")

for arr_problems_i in "${arr_problems[@]}"; do # Go through all the Problem folders
  mkdir "${OUTPUT_FOLDER}${arr_problems_i}" # Create folder for the Problem

  for ((i = 0; i < ${#arr_generations[*]}; i++)); do # Go through all the different scenarios
    PROBLEM_FILE_OUT="${arr_problems_i}_G_${arr_generations[i]}_P_${arr_populations[i]}"
    FOLDER_EXE="${arr_problems_i}/${PROBLEM_FILE_OUT}/"
    mkdir "${OUTPUT_FOLDER}${FOLDER_EXE}" # Create folder for the Problem with the parameters

    { time -p java -cp target/astor-1.0.0-SNAPSHOT-jar-with-dependencies.jar fr.inria.main.evolution.AstorMain -mode jgenprog \
      -srcjavafolder /src/main/java/ -srctestfolder /src/test/java/ -binjavafolder /target/classes/ \
      -bintestfolder /target/test-classes/ -location /home/str/"$arr_problems_i" -dependencies /home/str/"${arr_problems_i}"/lib \
      -parameters maxGeneration:"${arr_generations[i]}":population:"${arr_populations[i]}" \
      -out "${OUTPUT_FOLDER}${FOLDER_EXE}" >"${OUTPUT_FOLDER}${FOLDER_EXE}${PROBLEM_FILE_OUT}-output.txt" \
      ;} 2>"${OUTPUT_FOLDER}${FOLDER_EXE}${PROBLEM_FILE_OUT}-time.txt"
  done
done
