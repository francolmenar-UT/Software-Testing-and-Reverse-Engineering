import sys, re
from os import path
import createClasses
import createProblemClass
import constants
from constants import *
from branch import analyze_branches, write_graph
from timer import timerInit

import functions

types = dict()

# Global Variables
var_count, bool_count, str_count, method_count, scope_depth = 1, 1, 1, 1, 0
main_found = False

first_bracket = False

# Set the path
file_path = sys.argv[1]
realpath = path.realpath(file_path)
assert (path.isfile(realpath))

# Open original file
original_file = realpath
f = open(original_file, 'r')

temp_filename = 'temp' + path.basename(realpath)
temp_file = path.join(path.dirname(realpath), temp_filename)
out = open(temp_file, 'w')

graph = analyze_branches(f, out)
out.close()
f.close()

f = open(temp_file, 'r')

inst_filename = 'temp2' + path.basename(realpath)
instructed_file = path.join(path.dirname(realpath), inst_filename)
out = open(instructed_file, 'w')  # Create instructed file to write into it
out.write("import java.util.*;\n")
out.write("import java.lang.Math;\n")
out.write("import java.io.BufferedWriter;\n")
out.write("import java.io.FileWriter;\n")
out.write("import java.io.IOException;\n")
out.write("import java.io.PrintWriter;\n")
out.write("import java.util.Date;\n")
out.write("import java.util.Random;\n")
var_count, bool_count, str_count, scope_depth = 1, 1, 1, 0  # Reset the variables

for line in f.readlines():
    outline = line

    line = line.split("//", 1)[0]

    line = line.replace('System.err', 'System.out')

    if line.find("public static void main") != -1:  # Main statement
        createProblemClass.create_main_method(out, line)  # Create main method
        # Write graph
        write_graph(out, graph)
        timerInit(out)
        continue

    if line.find("while(true) {") != -1:  # While(true) statement
        createProblemClass.create_while_true(out, line)  # Create the inside of while(true)
        continue

    if line.find("stdin.readLine()") != -1:  # readLine() statement
        createProblemClass.create_readline(out)  # Create the readLine() code
        continue

    # if the line contains `resultFuzz` it is an instrumented line and we can just copy it without doing anything
    if 'resultFuzz' in line:
        out.write(line)
        continue

    if 'this_branch_id' in line:
        out.write(line)
        continue

    bracket_openRe = '({)'
    m = re.findall(r'('+bracket_openRe+')', line)
    if len(m) > 0:
        for match in m:
            scope_depth += 1

    bracket_closeRe = '(})'
    m = re.findall(r'('+bracket_closeRe+')', line)
    if len(m) > 0:
        for match in m:
            scope_depth -= 1

    bracket_closeRe = '(^\s*})'
    m = re.findall(r'('+bracket_closeRe+')', line)
    while len(m) > 0:
        for match in m:
            if len(match[1]) > 0:
                text = match[1]
                line = line.replace(text, "", 1)
                if scope_depth >= 2:
                    out.write("I.closeIf();}\n")
                else:
                    out.write("}\n")
        m = re.findall(r'('+bracket_closeRe+')', line)

    line = createProblemClass.search_close_bracket(out, line)  # Search for close brackets

    line = createProblemClass.search_int_string_bool(line, types)  # Search for Int, String and Boolean

    line = createProblemClass.search_new_string_bool(line)  # Search for the creation of strings and booleans

    # Search for mathematical operations
    line, var_count, str_count, bool_count = createProblemClass.search_math_operations(out, line, types, var_count,
                                                                                       str_count, bool_count)
    # Search for Greater or Lower comparisons
    line, bool_count = createProblemClass.search_gos_comp(out, line, bool_count)

    # Search for AND, OR and NOT comparisons
    line, bool_count = createProblemClass.search_and_or_not_comp(out, line, bool_count)

    # Search for printing, assigning and if statements
    line = createProblemClass.search_print_assign_if(line, out)

    # Searches for ProblemX
    line = createProblemClass.search_main_problem(line)

    # Searches for stdin.readLine
    line = createProblemClass.search_stdin_readline(line)
    out.write(line)  # write updated code to file

    bracket_openRe = '({\s*$)'
    m = re.findall(r'('+bracket_openRe+')', line)
    if len(m) > 0:
        for match in m:
            if len(match[1]) > 0:
                text = match[1]
                line = line.replace(text, "", 1)
                if scope_depth >= 3:
                    out.write("I.openIf();\n")

reset_in = open(instructed_file, 'r')

createProblemClass.create_reset_method(out, reset_in)  # Create the Reset method
out.write("}\n")  # End of Problem Class

# instruct if
out.close()
re_in = open(instructed_file, 'r')

if_filename = 'inst' + path.basename(realpath)
if_file = path.join(path.dirname(realpath), if_filename)
out2 = open(if_file, 'w')

functions.if_stack_pop(re_in, out2)

createClasses.create_all(out2, var_count, bool_count, str_count)  # Create all the classes
