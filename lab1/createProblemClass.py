import re
import constants


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
    m = re.findall(r'(' + constants.bracket_closeRe + ')', line)  # Search for close brackets
    while len(m) > 0:
        for match in m:
            if len(match[1]) > 0:  # Something more than a bracket
                text = match[1]
                line = line.replace(text, "", 1)  # Remove the bracket from line
                out.write("}\n")  # Write the bracket into the file
        m = re.findall(r'(' + constants.bracket_closeRe + ')', line)  # Search for more brackets
