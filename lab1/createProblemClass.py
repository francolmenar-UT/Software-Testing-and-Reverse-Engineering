import re
import constants
from constants import *
from timer import timerExec


def create_reset_method(out, reset_in):
    """
    Writes the Reset method into the file
    :param out: destination file in which the code is written
    :param reset_in:
    """
    out.write("public void reset(){\n")
    out.write('\
        //System.err.print("\\n\\nNumber of traits: ");\n\
        //System.err.println(I.trait_counter);\n\
        I.trait_counter = 0;\n')
    out.write("System.out.println(\"reset\");\n")
    for line in reset_in.readlines():
        line = line.replace(', I.stack.empty() ? false : I.stack.peek()', '')
        if line.find("public MyInt") != -1:  # MyInt  Array
            if line.find("{") != -1:
                out.write(line.split('=', 1)[0].split(' ', 2)[2])
                out.write(" = new MyInt[] ")
                out.write(line.split('=', 1)[1])
            else:
                out.write(line.strip().split(' ', 2)[2])
        if line.find("public MyBool") != -1:  # MyBool Array
            if line.find("{") != -1:
                out.write(line.split('=', 1)[0].split(' ', 2)[2])
                out.write(" = new MyBool[] ")
                out.write(line.split('=', 1)[1])
            else:
                out.write(line.strip().split(' ', 2)[2])
        if line.find("public MyString") != -1:  # MyString Array
            if line.find("{") != -1:
                out.write(line.split('=', 1)[0].split(' ', 2)[2])
                out.write(" = new MyString[] ")
                out.write(line.split('=', 1)[1])
            else:
                out.write(line.strip().split(' ', 2)[2])
    out.write("}\n")
    out.write("\n")


def create_main_method(out, line):
    """
    Writes the main method into the file
    :param out: destination file in which the code is written
    :param line: The current text line found
    """
    out.write(line)  # Write main statement
    out.write('Fuzzer fuzzer = new Fuzzer(args[0], args[1]);\n')  # Create the fuzzer
    out.write('_set_graph(fuzzer);\n')
    out.write("_set_fi_branch(fuzzer);\n")
    out.write("_set_visited_branches(fuzzer);\n")
    out.write("_set_rev_graph(fuzzer);\n")

    # Write SIGINT handler
    out.write("Signal.handle(new Signal(\"INT\"), new SignalHandler() {\n"
              "     public void handle(Signal sig) {\n"
              "         int counter = 0;\n"
              "         for (Boolean visit : fuzzer.visited_branches.values()) {\n"
              "             if (visit) counter++;\n"
              "         }\n"
              "         System.exit(counter);\n"
              "     }\n"
              "});\n")


def create_while_true(out, line):
    """
    Writes the while(true) code into the file
    :param out: destination file in which the code is written
    :param line: The current text line found
    """
    out.write(line)  # Write while statement
    out.write('if (resultFuzz != null)\n')
    out.write('\tfuzzer.after_execution(resultFuzz, I.trait_counter);\n')
    out.write("eca.reset();\n")  # Add a reset for the next iteration
    timerExec(out) # write timer check
    out.write('resultFuzz = fuzzer.fuzz(eca.inputs);\n')  # Run the fuzzer
    # Write the start of a for loop which will iterate through the fuzzed values
    out.write("for(MyInputIndex = 0; MyInputIndex < resultFuzz.myStr.length; MyInputIndex++){\n")
    out.write("int i = MyInputIndex;\n")  # Global auxiliary counter


def create_readline(out):
    """
    Writes the stdin.readLine() code into the file
    :param out: destination file in which the code is written
    """
    out.write("MyString input = resultFuzz.myStr[i];")


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
    if 'this_branch_id' in line:
        return line

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
    types[val] = type
    return line.replace(type, "MyBool", 1)


def search_new_string_bool(line):
    """
    Searches for the creation of strings and booleans
    :param line: The current text line found
    """
    m = re.findall(r'(' + booleanRe1 + '|' + booleanRe2 + '|' + stringRe + '|' + numberRe + ')',
                   line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # First Boolean creation
                text = match[1]
                var = match[2]
                line = line.replace(var, "new MyBool(" + var + ", I.stack.empty() ? false : I.stack.peek())", 1)
            if len(match[3]) > 0:  # Second Boolean creation
                text = match[3]
                var = match[4]
                line = line.replace(var, "new MyBool(" + var + ", I.stack.empty() ? false : I.stack.peek())", 1)
            if len(match[5]) > 0:  # First String creation
                text = match[5]
                var = match[6]
                line = line.replace(var, "new MyString(" + var + ", I.stack.empty() ? false : I.stack.peek())", 1)
            if len(match[7]) > 0:  # Second String creation
                text = match[7]
                beg = match[8]
                var = match[9]
                end = match[10]
                line = line.replace(beg + var + end,
                                    beg + "new MyInt(" + var + ", I.stack.empty() ? false : I.stack.peek())" + end, 1)
        m = re.findall(r'(' + booleanRe1 + '|' + booleanRe2 + '|' + stringRe + '|' + numberRe + ')',
                       line)  # find all matching sub-patterns
    return line


def search_math_operations(out, line, types, var_count, str_count, bool_count):
    """
    Searches for mathematical operations
    :param out: destination file in which the code is written
    :param line: The current text line found
    :param types:
    :param var_count:
    :param str_count:
    :param bool_count:
    """
    m = re.findall(
        r'(' + addRe + '|' + delRe + '|' + mulRe + '|' + divRe + '|' + modRe + '|' + indRe + '|' + varRe + ')',
        line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # Addition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myAdd( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[4]) > 0:  # Subtraction
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myDel( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[7]) > 0:  # Multiplication
                text = match[7]
                var = match[8]
                val = match[9]
                out.write("I.myMul( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[10]) > 0:  # Division
                text = match[10]
                var = match[11]
                val = match[12]
                out.write("I.myDiv( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[13]) > 0:  # Modulus
                text = match[13]
                var = match[14]
                val = match[15]
                out.write("I.myMod( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[16]) > 0:  # Array Assignments
                text = match[16]
                var = match[17]
                val = match[18]
                if var in types.keys() and (types[var] == "String" or types[var] == "String[]"):
                    out.write("I.myInd( I.str" + str(str_count) + "," + var + "," + val + ");\n")
                    line = line.replace(text, "I.str" + str(str_count), 1)  # replace matched code with own
                    str_count += 1
                elif var in types.keys() and types[var] == "boolean[]":
                    out.write("I.myInd( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                    line = line.replace(text, "I.bool" + str(bool_count), 1)  # replace matched code with own
                    bool_count += 1
                else:
                    out.write("I.myInd( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                    line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own
                    var_count += 1
            elif len(match[19]) > 0:
                text = match[19]
                var = match[20]
                val = match[21]
                line = line.replace(text, var + val, 1)  # replace matched code with own function
        m = re.findall(
            r'(' + addRe + '|' + delRe + '|' + mulRe + '|' + divRe + '|' + modRe + '|' + indRe + '|' + varRe + ')',
            line)  # find all matching
    return line, var_count, str_count, bool_count


def search_gos_comp(out, line, bool_count):
    """
    Searches for greater or lower comparisons
    :param out: destination file in which the code is written
    :param line: The current text line found
    :param bool_count:
    """
    m = re.findall(r'(' + equalsRe + '|' + isisRe + '|' + leRe + '|' + geRe + '|' + leqRe + '|' + geqRe + ')',
                   line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # Equals
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myEquals( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[4]) > 0:  # Equals ==
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myEquals( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[7]) > 0:  # Less
                text = match[7]
                var = match[8]
                val = match[9]
                out.write("I.myLess( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[10]) > 0:  # Greater
                text = match[10]
                var = match[11]
                val = match[12]
                out.write("I.myGreater( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[13]) > 0:  # Less Equal
                text = match[13]
                var = match[14]
                val = match[15]
                out.write("I.myLessEqual( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[16]) > 0:  # Greater equal
                text = match[16]
                var = match[17]
                val = match[18]
                out.write("I.myGreaterEqual( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            bool_count += 1
        m = re.findall(r'(' + equalsRe + '|' + isisRe + '|' + leRe + '|' + geRe + '|' + leqRe + '|' + geqRe + ')',
                       line)  # find all matching sub-patterns

    return line, bool_count


def search_and_or_not_comp(out, line, bool_count):
    """
    Searches for AND, OR and NOT comparisons
    :param out: destination file in which the code is written
    :param line: The current text line found
    :param bool_count:
    """
    m = re.findall(r'(' + andRe + '|' + orRe + '|' + notRe + '|' + boolRe + ')', line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # AND
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myAnd( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[4]) > 0:  # OR
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myOr( I.bool" + str(bool_count) + "," + var + "," + val + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[7]) > 0:  # NOT
                text = match[7]
                var = match[8]
                out.write("I.myNot( I.bool" + str(bool_count) + "," + var + ",resultFuzz);\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own
            elif len(match[9]) > 0:  # No idea??
                text = match[9]
                var = match[10]
                val = match[11]
                line = line.replace(text, var + val, 1)  # replace matched code with own function
                bool_count -= 1
            bool_count += 1
        m = re.findall(r'(' + andRe + '|' + orRe + '|' + notRe + '|' + boolRe + ')',
                       line)  # find all matching sub-patterns
    return line, bool_count


def search_print_assign_if(line):
    """
    Searches for printing, assigning and if statements
    :param line: The current text line found
    """
    m = re.findall(r'('+assignRe+'|'+assignPlusRe+'|'+assignMinRe+'|'+printRe+'|'+ifRe+'|'+ifCompactRe+'|'+ifCompactReP+'|'+ifCompactReM+')', line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                line = line.replace(text, var + " = I.myAssign(" + val + ");", 1)
            if len(match[4]) > 0:  # if first kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                #out.write("I.myAdd(" + var + "," + var + "," + val + ");")
                line = line.replace(text,var, 1)
            if len(match[7]) > 0: # if first kind of condition
                text = match[7]
                var = match[8]
                val = match[9]
	            #out.write("I.myMin(" + var + "," + var + "," + val + ");")
                line = line.replace(text, var, 1)
            if len(match[10]) > 0: # if first kind of condition
	            text = match[10]
	            var = match[11]
	            line = line.replace(text, "I.myPrint", 1)
            if len(match[12]) > 0: # if first kind of condition
	            text = match[12]
	            var = match[13]
	            line = line.replace(text, "if(I.myIf(" + var + "))", 1)
            if len(match[14]) > 0: # if first kind of condition
	            text = match[14]
	            var1 = match[15]
	            var2 = match[16]
	            var3 = match[17]
	            var4 = match[18]
	            #out.write("if(I.myIf(" + var2 + ")){ I.openIf(); " + var1 + " = I.myAssign(" + var3 + "); I.closeIf(); }\n")
	            #out.write("else { I.openIf(); " + var1 + " = I.myAssign(" + var4 + "); I.closeIf(); }\n")
	            line = line.replace(text, "", 1)
            if len(match[19]) > 0: # if first kind of condition
	            text = match[19]
	            var1 = match[20]
	            var2 = match[21]
	            var3 = match[22]
	            var4 = match[23]
	            #out.write("if(I.myIf(" + var2 + ")){ I.openIf(); I.myAdd(" + var1 + "," + var1 + "," + var3 + "); I.closeIf(); }\n")
	            #out.write("else { I.openIf(); I.myAdd(" + var1 + "," + var1 + "," + var4 + "); I.closeIf(); }\n")
	            line = line.replace(text, "", 1)
            if len(match[24]) > 0: # if first kind of condition
                text = match[24]
                var1 = match[25]
                var2 = match[26]
                var3 = match[27]
                var4 = match[28]
	            #out.write("if(I.myIf(" + var2 + ")){ I.openIf(); I.myDel(" + var1 + "," + var1 + "," + var3 + "); I.closeIf(); }\n")
                var4 = match[28]
                #out.write("if(I.myIf(" + var2 + ")){ I.openIf(); I.myDel(" + var1 + "," + var1 + "," + var3 + "); I.closeIf(); }\n")
                #out.write("else { I.openIf(); I.myDel(" + var1 + "," + var1 + "," + var4 + "); I.closeIf(); }\n")
                line = line.replace(text, "", 1)
        m = re.findall(r'('+assignRe+'|'+printRe+'|'+ifRe+')', line)  # find all matching sub-patterns
    return line


def search_main_problem(line):
    """
    Searches for ProblemX
    :param line: The current text line found
    """
    m = re.findall(r'(' + mainRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # ProblemX
                text = match[1]
                var = match[2]
                line = line.replace(text, " inst" + var, 1)
                if "class" in line:
                    line = line + "static int MyInputIndex;\n" + "static int lengthArr;\n" + "static MyInput resultFuzz;\n"
    return line


def search_stdin_readline(line):
    """
    Searches for stdin.readLine
    :param line: The current text line found
    """
    m = re.findall(r'(' + readRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(text, "new MyString(" + var + ", true)", 1)
    return line
