import re
import constants
from constants import *



def create_reset_method(out, reset_in):
    """
    Writes the Reset method into the file
    :param out: destination file in which the code is written
    :param reset_in:
    """
    out.write("public void reset(){\n")
    out.write("System.out.println(\"reset\");")
    for line in reset_in.readlines():
        if line.find("public MyInt") != -1:
            if line.find("{") != -1:
                out.write(line.split('=', 1)[0].split(' ', 2)[2])
                out.write(" = new MyInt[] ")
                out.write(line.split('=', 1)[1])
            else:
                out.write(line.split(' ', 2)[2])
        if line.find("public MyBool") != -1:
            if line.find("{") != -1:
                out.write(line.split('=', 1)[0].split(' ', 2)[2])
                out.write(" = new MyBool[] ")
                out.write(line.split('=', 1)[1])
            else:
                out.write(line.split(' ', 2)[2])
        if line.find("public MyString") != -1:
            if line.find("{") != -1:
                out.write(line.split('=', 1)[0].split(' ', 2)[2])
                out.write(" = new MyString[] ")
                out.write(line.split('=', 1)[1])
            else:
                out.write(line.split(' ', 2)[2])
    out.write("}\n")
    out.write("\n")


def create_main_method(out, line):
    """
    Writes the main method into the file
    :param out: destination file in which the code is written
    :param line: The current text line found
    """
    out.write(line)  # Write main statement


def create_while_true(out, line):
    """
    Writes the while(true) code into the file
    :param out: destination file in which the code is written
    :param line: The current text line found
    """
    out.write(line)  # Write while statement
    out.write("eca.reset();")  # Add a reset for the next iteration
    out.write("MyString[] fuzzed_inputs = Fuzzer.fuzz(eca.inputs);")  # Add fuzzed values
    # Write the start of a for loop which will iterate through the fuzzed values
    out.write("for(int i = 0; i < fuzzed_inputs.length; i++){")


def create_readline(out):
    """
    Writes the stdin.readLine() code into the file
    :param out: destination file in which the code is written
    """
    out.write("MyString input = fuzzed_inputs[i];")
    out.write("System.out.println(\"Fuzzing: \" + input.val);")


def search_close_bracket(out, line):
    """
    Writes the while(true) code into the file
    :param out: destination file in which the code is written
    :param line: The current text line found
    """
    m = re.findall(r'(' + bracket_closeRe + ')', line)  # Search for close brackets
    while len(m) > 0:
        for match in m:
            if len(match[1]) > 0:  # Something more than a bracket
                text = match[1]
                line = line.replace(text, "", 1)  # Remove the bracket from line
                out.write("}\n")  # Write the bracket into the file
        m = re.findall(r'(' + bracket_closeRe + ')', line)  # Search for more  brackets
    return line


def search_int_string_bool(line, types):
    """
    Searches for integers, string and booleans
    :param line: The current text line found
    :param types:
    """
    m = re.findall(r'(' + typeIntRe + '|' + typeStringRe + '|' + typeBoolRe + ')',
                   line)  # find all matching sub-patterns

    if len(m) > 0:  # if any matching items
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                line = replace_int(line, match, types)
            if len(match[5]) > 0:  # if second kind of condition
                line = replace_string(line, match, types)
            if len(match[9]) > 0:  # if third kind of condition
                line = replace_boolean(line, match, types)
    return line


def replace_int(line, match, types):
    """
    Replaces a found Integer
    :param line: The current text line found
    :param match:
    :param types:
    """
    var, val, text = "", "", ""
    text = match[1]
    type = match[2]
    var = match[3]
    val = match[4]
    # print("type " + val + " = " + type)
    types[val] = type
    return line.replace(type, "MyInt", 1)


def replace_string(line, match, types):
    """
    Replaces a found String
    :param line: The current text line found
    :param match:
    :param types:
    """
    var, val, text = "", "", ""
    text = match[5]
    type = match[6]
    var = match[7]
    val = match[8]
    # print("type " + val + " = " + type)
    types[val] = type
    return line.replace(type, "MyString", 1)


def replace_boolean(line, match, types):
    """
    Replaces a found Boolean
    :param line: The current text line found
    :param match:
    :param types:
    """
    var, val, text = "", "", ""
    text = match[9]
    type = match[10]
    var = match[11]
    val = match[12]
    # print("type " + val + " = " + type)
    types[val] = type
    return line.replace(type, "MyBool", 1)
