#!/usr/bin/env bash
output_folder="../../results/output_astor/"
aston_sufix="AstorMain-"
path_to_patches="src/"


declare -a arr_problems=("Problem1_buggy" "Problem11_buggy" "m158_LTL_buggy")
declare -a arr_generations=("500" "750" "1000")
declare -a arr_populations=("20" "25" "30")

for arr_problems_i in "${arr_problems[@]}"; do # Go through all the Problem folders

  for ((i = 0; i < ${#arr_generations[*]}; i++)); do # Go through all the different scenarios
    problem_file_out="${arr_problems_i}_G_${arr_generations[i]}_P_${arr_populations[i]}"

    folder_exe="${arr_problems_i}/${problem_file_out}/"

   count="$(ls ${output_folder}${folder_exe}${aston_sufix}${arr_problems_i}/${path_to_patches} | wc -l)"

    echo "${folder_exe}${aston_sufix}${arr_problems_i}/${path_to_patches}"
    echo ">>>> $(( count / 2 ))"
  echo
  done
  echo
done
