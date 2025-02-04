## Lab 3

This is the code regarding to the implementation of Lab 3.

## Building the code - Usage of `scripts/`

The folder `scripts/` contain all the needed scripts for running the python regex, compiling 
the java code and running the resulting instrumented code.

A brief guide of how to use the different scripts is going to be outlined.

### python-comp.sh

It runs `new_regex.py` in the original java files. The parameters accepted by it are:
  
- `-f` : Indicates which RERS folders are going to be considered. The corresponding folders for the different input 
values for `-f` are the following:

    - [1] : TrainingSeqLtlRers2019/
    - [2] : SeqLtlRers2019/
    - [3] : SeqReachabilityRers2019/
    - [4] : TrainingSeqReachRers2019/

It accepts values from 1 to 4 which can be introduced in the following format.
```
./python-comp.sh -f 1,2,4
``` 

If no `-f` flag is provided, all the folders are chosen.




- `-h` : Prints a message explaining the usage of the script.

```
Usage:
-f | --folder [ 1,2,3,4 || 1,3,4 || 1,2 ...] 
```

### javac-run.sh

It compiles the generated java code from `new_regex.py`. The parameters accepted by it are:
- `-f` : Indicates which RERS folders are going to be considered.
- `-v` : Specifies if the full output is going to be displayed or not on the terminal. It does not take any parameter as input.
As a default the output is not printed.


```
.\javac-run.sh -v
```

- `-h` : Prints a message explaining the usage of the script.


 ### java-run.sh

It runs the compiled code generated from `javac` command. The parameters accepted by it are:
- `-d` : Set Depth or Breath search. It can take as value `true` or `false` being the first for Depth and the 
last for Breath search. As default it is set to true. Its usage is as follows.

```
.\java-run.sh -d true
```


- `-f` : Indicates which RERS folders are going to be considered.

- `-t` : Sets the maximum amount of time assigned to the execution of the file. The input can be introduced in minutes, seconds 
or hours, but it must be specified by `s`, `m` or `h`. As a default it is set to one minute.


```
.\java-run.sh -t 2m
```
    
- `-v` : Specifies if the full output is going to be displayed or not on the terminal.


- `-h` : Prints a message explaining the usage of the script.
    
    
    
 ### run.sh
 
 It performs all the previous described actions. It runs the `new_regex.py`, `javac` and finally the `java` command. The parameters accepted by it are:
 - `-d` : Set Depth or Breath search.
  - `-e` : Changes the output location for the `Log` files for further utilization for creating graphs. 
  It is development oriented. It does not receive any input.
  
 ```
 .\run.sh -e
 ```

 - `-f` : Indicates which RERS folders are going to be considered.
 - `-m` : Specifies the mutation rate to be used. The default value is `0.1`
 ```
 .\run.sh -m 0.5
 ```
 - `-s` : Indicates the size of the population to be used. By default it is set to `5`.
  ```
  .\run.sh -s 8
  ```  
 - `-t` : Sets the maximum amount of time assigned to the execution of the file.
 - `-v` : Specifies if the full output is going to be displayed or not on the terminal.
 - `-h` : Prints a message explaining the usage of the script. The output is the following.

```
-d | --depth [ true || false ]
-e | --export
-f | --folder [ 1,2,3,4 || 1,3,4 || 1,2 ...]
-m | --mutation <number>.<number>
-s | --size [0-9]+
-t | --timeout [0-9]+[smh]
-v | --verbose
```

### createGraph.py
It is specifically written for the final lab. It creates graphs of all provided RERS problems. Where one graph includes the results of alll the algorithms to one specific problem. The parameters accepted by it are:
- `-src1`: the path of the test results of the first lab
- `-src2`: the path of the test results of the second lab
- `-src3`: the path of the test results of the third lab

```
 python createGraph.py -src1 \path-to-log-files\ -src2 \path-to-log-files\ -src3 \path-to-log-files\
```

- `-h` : Prints a message explaining the usage of the script. The output is the following:
```
-src1 SOURCE1 path of the logfiles of the first lab
-src2 SOURCE2 path of the logfiles of the second lab
-src3 SOURCE3 path of the logfiles of the third lab
```