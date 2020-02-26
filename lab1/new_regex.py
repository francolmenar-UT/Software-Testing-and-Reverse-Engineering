import sys, re
from os import path
import createClasses
import createMethods
import createProblemClass
import constants
from constants import *

types = dict()

# Global Variables
var_count, bool_count, str_count, method_count = 1, 1, 1, 1
main_found = False

first_bracket = False

# Set the path
file_path = sys.argv[1]
realpath = path.realpath(file_path)
assert (path.isfile(realpath))

original_file = realpath
inst_filename = 'inst' + path.basename(realpath)
instructed_file = path.join(path.dirname(realpath), inst_filename)

f = open(original_file, 'r')  # Open original file
out = open(instructed_file, 'w')  # Create instructed file to write into it
out.write("import java.util.Random;\n")
# method_out = open('IM.java', 'w')

# method_out.write("public void sub_method0(MyString input){\n")


for line in f.readlines():
    outline = line

    line = line.split("//", 1)[0]

    # if line.startswith("}") and first_bracket == True:
    # method_out.close()
    #    f2 = open('IM.java', 'r')
    #    for line2 in f2.readlines():
    #        out.write(line2)
    #    first_bracket = False
    # if line.startswith("}"):
    #    first_bracket = True
    # else:
    #    first_bracket = False

    if line.find("public static void main") != -1:  # Main statement
        createProblemClass.create_main_method(out, line)  # Create main method
        continue

    if line.find("while(true) {") != -1:  # While(true) statement
        createProblemClass.create_while_true(out, line)  # Create the inside of while(true)
        continue

    if line.find("stdin.readLine()") != -1:  # readLine() statement
        createProblemClass.create_readline(out)  # Create the readLine() code
        continue

    var_count, bool_count, str_count = 1, 1, 1  # Reset the variables
    createProblemClass.search_close_bracket(out, line)  # Search for close brackets

    m = re.findall(r'(' + typeIntRe + '|' + typeStringRe + '|' + typeBoolRe + ')',
                   line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                type = match[2]
                var = match[3]
                val = match[4]
                # print("type " + val + " = " + type)
                types[val] = type
                line = line.replace(type, "MyInt", 1)
            if len(match[5]) > 0:  # if first kind of condition
                text = match[5]
                type = match[6]
                var = match[7]
                val = match[8]
                # print("type " + val + " = " + type)
                types[val] = type
                line = line.replace(type, "MyString", 1)
            if len(match[9]) > 0:  # if first kind of condition
                text = match[9]
                type = match[10]
                var = match[11]
                val = match[12]
                # print("type " + val + " = " + type)
                types[val] = type
                line = line.replace(type, "MyBool", 1)

    m = re.findall(r'(' + booleanRe1 + '|' + booleanRe2 + '|' + stringRe + '|' + numberRe + ')',
                   line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        # print(line)
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(var, "new MyBool(" + var + ")", 1)
            if len(match[3]) > 0:  # if first kind of condition
                text = match[3]
                var = match[4]
                line = line.replace(var, "new MyBool(" + var + ")", 1)
            if len(match[5]) > 0:  # if first kind of condition
                text = match[5]
                var = match[6]
                # print(text)
                line = line.replace(var, "new MyString(" + var + ")", 1)
            if len(match[7]) > 0:  # if first kind of condition
                text = match[7]
                beg = match[8]
                var = match[9]
                end = match[10]
                # print(beg)
                # print(var)
                # print(end)
                line = line.replace(beg + var + end, beg + "new MyInt(" + var + ")" + end, 1)
        m = re.findall(r'(' + booleanRe1 + '|' + booleanRe2 + '|' + stringRe + '|' + numberRe + ')',
                       line)  # find all matching sub-patterns


    m = re.findall(
        r'(' + addRe + '|' + delRe + '|' + mulRe + '|' + divRe + '|' + modRe + '|' + indRe + '|' + varRe + ')',
        line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        # print(line)
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myAdd( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[4]) > 0:  # if second  kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myDel( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[7]) > 0:
                text = match[7]
                var = match[8]
                val = match[9]
                out.write("I.myMul( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[10]) > 0:
                text = match[10]
                var = match[11]
                val = match[12]
                out.write("I.myDiv( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[13]) > 0:
                text = match[13]
                var = match[14]
                val = match[15]
                out.write("I.myMod( I.var" + str(var_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.var" + str(var_count), 1)  # replace matched code with own function
                var_count += 1
            elif len(match[16]) > 0:
                text = match[16]
                var = match[17]
                val = match[18]
                # print(types)
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
        # print(line)
        m = re.findall(
            r'(' + addRe + '|' + delRe + '|' + mulRe + '|' + divRe + '|' + modRe + '|' + indRe + '|' + varRe + ')',
            line)  # find all matching


    m = re.findall(r'(' + equalsRe + '|' + isisRe + '|' + leRe + '|' + geRe + '|' + leqRe + '|' + geqRe + ')',
                   line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        # print(line)
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myEquals( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[4]) > 0:  # if second  kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myEquals( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[7]) > 0:  # if second  kind of condition
                text = match[7]
                var = match[8]
                val = match[9]
                out.write("I.myLess( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[10]) > 0:  # if second  kind of condition
                text = match[10]
                var = match[11]
                val = match[12]
                out.write("I.myGreater( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[13]) > 0:  # if second  kind of condition
                text = match[13]
                var = match[14]
                val = match[15]
                out.write("I.myLessEqual( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[16]) > 0:  # if second  kind of condition
                text = match[16]
                var = match[17]
                val = match[18]
                out.write("I.myGreaterEqual( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            bool_count += 1
        m = re.findall(r'(' + equalsRe + '|' + isisRe + '|' + leRe + '|' + geRe + '|' + leqRe + '|' + geqRe + ')',
                       line)  # find all matching sub-patterns

    m = re.findall(r'(' + andRe + '|' + orRe + '|' + notRe + '|' + boolRe + ')', line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        # print(line)
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if second  kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myAnd( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[4]) > 0:  # if second  kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myOr( I.bool" + str(bool_count) + "," + var + "," + val + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[7]) > 0:  # if second  kind of condition
                text = match[7]
                var = match[8]
                out.write("I.myNot( I.bool" + str(bool_count) + "," + var + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count),
                                    1)  # replace matched code with own                #print(match[2], match[3])
            elif len(match[9]) > 0:
                text = match[9]
                var = match[10]
                val = match[11]
                line = line.replace(text, var + val, 1)  # replace matched code with own function
                bool_count -= 1
            bool_count += 1
        m = re.findall(r'(' + andRe + '|' + orRe + '|' + notRe + '|' + boolRe + ')',
                       line)  # find all matching sub-patterns
        # print(line)

    m = re.findall(r'(' + assignRe + '|' + printRe + '|' + ifRe + ')', line)  # find all matching sub-patterns

    while len(m) > 0:  # if any matching items
        # print(line)
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
                line = line.replace(text, "I.myPrint", 1)
            if len(match[6]) > 0:  # if first kind of condition
                text = match[6]
                var = match[7]
                line = line.replace(text, "if(I.myIf(" + var + "))", 1)
        m = re.findall(r'(' + assignRe + '|' + printRe + '|' + ifRe + ')', line)  # find all matching sub-patterns

    m = re.findall(r'(' + mainRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        # print(line)
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(text, " inst" + var, 1)

    m = re.findall(r'(' + readRe + ')', line)  # find all matching sub-patterns
    if len(m) > 0:  # if any matching items
        # print(line)
        var, val, text = "", "", ""
        for match in m:  # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0:  # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(text, "new MyString(" + var + ", true)", 1)

    out.write(line)  # write updated code to file

reset_in = open(instructed_file, 'r')

createProblemClass.create_reset_method(out, reset_in)  # Create the Reset method
out.write("}\n")  # End of Problem Class

createClasses.create_all(out)  # Create all the classes
createMethods.create_all(out)  # Create all the methods

out.write("}\n")
