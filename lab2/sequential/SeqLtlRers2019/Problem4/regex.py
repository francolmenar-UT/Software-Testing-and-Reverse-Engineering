import sys, re

types = dict()

var_count = 1
bool_count = 1
str_count = 1
method_count = 1
main_found = False

first_bracket = False

f = open(sys.argv[1], 'r')
out = open('inst'+sys.argv[1], 'w')
out.write("import java.util.Random;\n")
#method_out = open('IM.java', 'w')

#method_out.write("public void sub_method0(MyString input){\n")


for line in f.readlines():
    outline = line

    line = line.split("//",1)[0]

    #if line.startswith("}") and first_bracket == True:
        #method_out.close()
    #    f2 = open('IM.java', 'r')
    #    for line2 in f2.readlines():
    #        out.write(line2)
    #    first_bracket = False
    #if line.startswith("}"):
    #    first_bracket = True
    #else:
    #    first_bracket = False

    if line.find("public static void main") != -1:
        out.write(line)
        continue

    if line.find("while(true) {") != -1:
        out.write(line)
        out.write("eca.reset();")
        out.write("MyString[] fuzzed_inputs = Fuzzer.fuzz(eca.inputs);")
        out.write("for(int i = 0; i < fuzzed_inputs.length; i++){")
        continue

    if line.find("stdin.readLine()") != -1:
        out.write("MyString input = fuzzed_inputs[i];")
        out.write("System.out.println(\"Fuzzing: \" + input.val);")
        continue

    if line.find("public  void") != -1:
        var_count = 1
        bool_count = 1
        str_count = 1

    typeIntRe = '((int)(\[?\]?)\s([\w\d]+))'
    typeStringRe = '((String)(\[?\]?)\s([\w\d]+))'
    typeBoolRe = '((boolean)(\[?\]?)\s([\w\d]+))'
    m = re.findall(r'('+typeIntRe+'|'+typeStringRe+'|'+typeBoolRe+')', line)  # find all matching sub-patterns
    if len(m) > 0 : # if any matching items
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                type = match[2]
                var = match[3]
                val = match[4]
                #print("type " + val + " = " + type)
                types[val] = type
                line = line.replace(type, "MyInt", 1)
            if len(match[5]) > 0: # if first kind of condition
                text = match[5]
                type = match[6]
                var = match[7]
                val = match[8]
                #print("type " + val + " = " + type)
                types[val] = type
                line = line.replace(type, "MyString", 1)
            if len(match[9]) > 0: # if first kind of condition
                text = match[9]
                type = match[10]
                var = match[11]
                val = match[12]
                #print("type " + val + " = " + type)
                types[val] = type
                line = line.replace(type, "MyBool", 1)

    booleanRe1 = '([\s\[\{\,](true)[\;\}\,])' # for a354505667.equals("e"
    booleanRe2 = '([\s\[\{\,](false)[\;\}\,])' # for a354505667.equals("e"
    stringRe = '([\s\[\{\,](\"\w*\")[\;\}\,])' # for a354505667.equals("e"
    numberRe = '(([\s\[\{\,])(-?\d+)([\;\}\,]))' # for a354505667.equals("e"
    m = re.findall(r'('+booleanRe1+'|'+booleanRe2+'|'+stringRe+'|'+numberRe+')', line)  # find all matching sub-patterns

    while len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(var, "new MyBool(" + var + ")", 1)
            if len(match[3]) > 0: # if first kind of condition
                text = match[3]
                var = match[4]
                line = line.replace(var, "new MyBool(" + var + ")", 1)
            if len(match[5]) > 0: # if first kind of condition
                text = match[5]
                var = match[6]
                #print(text)
                line = line.replace(var, "new MyString(" + var + ")", 1)
            if len(match[7]) > 0: # if first kind of condition
                text = match[7]
                beg = match[8]
                var = match[9]
                end = match[10]
                #print(beg)
                #print(var)
                #print(end)
                line = line.replace(beg+var+end, beg + "new MyInt(" + var + ")" + end, 1)
        m = re.findall(r'('+booleanRe1+'|'+booleanRe2+'|'+stringRe+'|'+numberRe+')', line)  # find all matching sub-patterns

    addRe = '((-?[\.\w\d]+)\s*\+\s*(-?[\.\w\d]+))'
    delRe = '((-?[\.\w\d]+)\s*\-\s*(-?[\.\w\d]+))'
    mulRe = '((-?[\.\w\d]+)\s*\*\s*(-?[\.\w\d]+))'
    divRe = '((-?[\.\w\d]+)\s*\/\s*(-?[\.\w\d]+))'
    modRe = '((-?[\.\w\d]+)\s*\%\s*(-?[\.\w\d]+))'
    indRe = '(([\.\w\d]+)\[([-*\.\w\d]+)\])'
    varRe = '(([\[\s\(])\(([\.\w\d]+)\))'

    m = re.findall(r'('+addRe+'|'+delRe+'|'+mulRe+'|'+divRe+'|'+modRe+'|'+indRe+'|'+varRe+')', line)  # find all matching sub-patterns
    if len(m) > 0 : # if any matching items
        #method_out.write("}\npublic void sub_method" + str(method_count) + "(MyString input){\n" )
        #out.write("sub_method" + str(method_count) + "(input);\n" )
        #method_count += 1;
        var_count = 1;
        bool_count = 1;
        str_count = 1;

    while len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myAdd( I.var" + str(var_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.var" + str(var_count), 1) # replace matched code with own function
                var_count += 1
            elif len(match[4]) > 0: # if second  kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myDel( I.var" + str(var_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.var" + str(var_count), 1) # replace matched code with own function
                var_count += 1
            elif len(match[7]) > 0:
                text = match[7]
                var = match[8]
                val = match[9]
                out.write("I.myMul( I.var" + str(var_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.var" + str(var_count), 1) # replace matched code with own function
                var_count += 1
            elif len(match[10]) > 0:
                text = match[10]
                var = match[11]
                val = match[12]
                out.write("I.myDiv( I.var" + str(var_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.var" + str(var_count), 1) # replace matched code with own function
                var_count += 1
            elif len(match[13]) > 0:
                text = match[13]
                var = match[14]
                val = match[15]
                out.write("I.myMod( I.var" + str(var_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.var" + str(var_count), 1) # replace matched code with own function
                var_count += 1
            elif len(match[16]) > 0:
                text = match[16]
                var = match[17]
                val = match[18]
                #print(types)
                if var in types.keys() and (types[var] == "String" or types[var] == "String[]"):
                    out.write("I.myInd( I.str" + str(str_count) + "," + var + "," + val +");\n")
                    line = line.replace(text, "I.str" + str(str_count), 1) # replace matched code with own
                    str_count += 1
                elif var in types.keys() and types[var] == "boolean[]":
                    out.write("I.myInd( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                    line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own
                    bool_count += 1
                else:
                    out.write("I.myInd( I.var" + str(var_count) + "," + var + "," + val +");\n")
                    line = line.replace(text, "I.var" + str(var_count), 1) # replace matched code with own
                    var_count += 1
            elif len(match[19]) > 0:
                text = match[19]
                var = match[20]
                val = match[21]
                line = line.replace(text, var + val, 1) # replace matched code with own function
        #print(line)
        m = re.findall(r'('+addRe+'|'+delRe+'|'+mulRe+'|'+divRe+'|'+modRe+'|'+indRe+'|'+varRe+')', line)  # find all matching

    equalsRe = '(([\.\w\d]+)\.equals\(("?[-*\.\w\d]+"?)\))' # for a354505667.equals("e"
    isisRe   = '(([-*\.\w\d]+)\s*==\s*([-*\.\w\d]+))' # for a1542761177 == 2
    leRe   = '(([-*\.\w\d]+)\s*<\s*([-*\.\w\d]+))' # for a1542761177 == 2
    geRe   = '(([-*\.\w\d]+)\s*>\s*([-*\.\w\d]+))' # for a1542761177 == 2
    leqRe   = '(([-*\.\w\d]+)\s*<=\s*([-*\.\w\d]+))' # for a1542761177 == 2
    geqRe   = '(([-*\.\w\d]+)\s*>=\s*([-*\.\w\d]+))' # for a1542761177 == 2
    andRe   = '(([\.\w\d]+)\s*\&\&\s*([\.\w\d]+))' # for a1542761177 == 2
    orRe   = '(([\.\w\d]+)\s*\|\|\s*([\.\w\d]+))' # for a1542761177 == 2
    notRe  = '(!([\.\w\d]+))' # for a1542761177 == 2
    boolRe = '(([\!\[\s\(])\(([\.\w\d]+)\))'
    m = re.findall(r'('+equalsRe+'|'+isisRe+'|'+leRe+'|'+geRe+'|'+leqRe+'|'+geqRe+')', line)  # find all matching sub-patterns

    if len(m) > 0 : # if any matching items
        #method_out.write("}\npublic void sub_method" + str(method_count) + "(MyString input){\n" )
        #out.write("sub_method" + str(method_count) + "(input);\n" )
        #method_count += 1;
        var_count = 1;
        bool_count = 1;
        str_count = 1;

    while len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myEquals( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[4]) > 0: # if second  kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myEquals( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[7]) > 0: # if second  kind of condition
                text = match[7]
                var = match[8]
                val = match[9]
                out.write("I.myLess( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[10]) > 0: # if second  kind of condition
                text = match[10]
                var = match[11]
                val = match[12]
                out.write("I.myGreater( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[13]) > 0: # if second  kind of condition
                text = match[13]
                var = match[14]
                val = match[15]
                out.write("I.myLessEqual( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[16]) > 0: # if second  kind of condition
                text = match[16]
                var = match[17]
                val = match[18]
                out.write("I.myGreaterEqual( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            bool_count += 1
        m = re.findall(r'('+equalsRe+'|'+isisRe+'|'+leRe+'|'+geRe+'|'+leqRe+'|'+geqRe+')', line)  # find all matching sub-patterns

    m = re.findall(r'('+andRe+'|'+orRe+'|'+notRe+'|'+boolRe+')', line)  # find all matching sub-patterns

    if len(m) > 0 : # if any matching items
        #method_out.write("}\npublic void sub_method" + str(method_count) + "(MyString input){\n" )
        #out.write("sub_method" + str(method_count) + "(input);\n" )
        #method_count += 1;
        var_count = 1;
        bool_count = 1;
        str_count = 1;

    while len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if second  kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                out.write("I.myAnd( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[4]) > 0: # if second  kind of condition
                text = match[4]
                var = match[5]
                val = match[6]
                out.write("I.myOr( I.bool" + str(bool_count) + "," + var + "," + val +");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[7]) > 0: # if second  kind of condition
                text = match[7]
                var = match[8]
                out.write("I.myNot( I.bool" + str(bool_count) + "," + var + ");\n")
                line = line.replace(text, "I.bool" + str(bool_count), 1) # replace matched code with own                #print(match[2], match[3])
            elif len(match[9]) > 0:
                text = match[9]
                var = match[10]
                val = match[11]
                line = line.replace(text, var + val, 1) # replace matched code with own function
                bool_count -=1
            bool_count += 1
        m = re.findall(r'('+andRe+'|'+orRe+'|'+notRe+'|'+boolRe+')', line)  # find all matching sub-patterns
        #print(line)
    assignRe = '(([\.\w\d]+)\s*=\s*(\"?[-*\.\w\d]+\"?)\s*;)' # for a354505667.equals("e"
    printRe = '((System.out.println))' # for a354505667.equals("e"
    ifRe = '(if\(([\.\w\d]+)\))' # for a354505667.equals("e"
    m = re.findall(r'('+assignRe+'|'+printRe+'|'+ifRe+')', line)  # find all matching sub-patterns

    while len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                var = match[2]
                val = match[3]
                line = line.replace(text, var + " = I.myAssign(" + val + ");", 1)
            if len(match[4]) > 0: # if first kind of condition
                text = match[4]
                var = match[5]
                line = line.replace(text, "I.myPrint", 1)
            if len(match[6]) > 0: # if first kind of condition
                text = match[6]
                var = match[7]
                line = line.replace(text, "if(I.myIf(" + var + "))", 1)
        m = re.findall(r'('+assignRe+'|'+printRe+'|'+ifRe+')', line)  # find all matching sub-patterns


    mainRe = '(\s(Problem[\d]+))' # for a354505667.equals("e"
    m = re.findall(r'('+mainRe+')', line)  # find all matching sub-patterns
    if len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(text, " inst"+var, 1)

    readRe = '((stdin.readLine\(\)))' # for a354505667.equals("e"
    m = re.findall(r'('+readRe+')', line)  # find all matching sub-patterns
    if len(m) > 0 : # if any matching items
        #print(line)
        var, val, text = "", "", ""
        for match in m: # for each submatch, extract the condition, the var and the val
            if len(match[1]) > 0: # if first kind of condition
                text = match[1]
                var = match[2]
                line = line.replace(text, "new MyString(" + var + ", true)", 1)

    out.write(line) # write updated code to file

reset_in = open('inst'+sys.argv[1], 'r')

out.write("public void reset(){\n")
out.write("System.out.println(\"reset\");")
for line in reset_in.readlines():
    if line.find("public MyInt") != -1:
        if line.find("{") != -1:
            out.write(line.split('=',1)[0].split(' ',2)[2])
            out.write(" = new MyInt[] ")
            out.write(line.split('=',1)[1])
        else:
            out.write(line.split(' ',2)[2])
    if line.find("public MyBool") != -1:
        if line.find("{") != -1:
            out.write(line.split('=',1)[0].split(' ',2)[2])
            out.write(" = new MyBool[] ")
            out.write(line.split('=',1)[1])
        else:
            out.write(line.split(' ',2)[2])
    if line.find("public MyString") != -1:
        if line.find("{") != -1:
            out.write(line.split('=',1)[0].split(' ',2)[2])
            out.write(" = new MyString[] ")
            out.write(line.split('=',1)[1])
        else:
            out.write(line.split(' ',2)[2])
out.write("}\n")
out.write("\n")


out.write("}\n")

out.write("class Fuzzer {\n")
out.write("public static MyString[] fuzz(MyString[] inputs){\n")
out.write("Random rand = new Random();\n")
out.write("int length = rand.nextInt(50) + 10;\n");
out.write("MyString[] result = new MyString[length];\n");
out.write("for(int i = 0; i < length; i++){\n");
out.write("int index = rand.nextInt(inputs.length);\n");
out.write("result[i] = new MyString(inputs[index].val, true);\n")
out.write("}\n")
out.write("return result;\n")
out.write("}\n")
out.write("}\n")


out.write("class MyInt {\n")
out.write("public int val = 0;\n")
out.write("public MyInt(int v){ this.val = v; }")
out.write("}\n")

out.write("class MyBool {\n")
out.write("public boolean val = false;\n")
out.write("public MyBool(boolean v){ this.val = v; }")
out.write("}\n")

out.write("class MyString {\n")
out.write("public String val = \"\";")
out.write("public boolean flow = false;")
out.write("public MyString(String v){ this.val = v; }")
out.write("public MyString(String v, boolean b){ this.val = v; this.flow = b; }")
out.write("}\n")

out.write("class I {\n")
out.write("\n")
for i in range(1,50):
    out.write("public static MyInt var" + str(i) + " = new MyInt(0);\n")
out.write("\n")
for i in range(1,50):
    out.write("public static MyBool bool" + str(i) + " = new MyBool(false);\n")
for i in range(1,50):
    out.write("public static MyString str" + str(i) + " = new MyString(\"\");\n")
out.write("\n")

out.write("public static void myAdd(MyInt a, MyInt b, MyInt c){ a.val = b.val+c.val; }\n")
out.write("public static void myDel(MyInt a, MyInt b, MyInt c){ a.val = b.val-c.val;  }\n")
out.write("public static void myMul(MyInt a, MyInt b, MyInt c){ a.val = b.val*c.val;  }\n")
out.write("public static void myDiv(MyInt a, MyInt b, MyInt c){ a.val = b.val/c.val;  }\n")
out.write("public static void myMod(MyInt a, MyInt b, MyInt c){ a.val = b.val%c.val;  }\n")
out.write("public static void myInd(MyInt a, MyInt[] b, MyInt c){ a.val = b[c.val].val; }\n")
out.write("public static void myInd(MyString a, MyString[] b, MyInt c){ a.val = b[c.val].val; }\n")

out.write("public static void myEquals(MyBool a, MyBool b, MyBool c){ a.val = (b.val == c.val); }\n")
out.write("public static void myEquals(MyBool a, MyInt b, MyInt c){ a.val = (b.val == c.val); }\n")
out.write("public static void myEquals(MyBool a, MyString b, MyString c){ a.val = (b.val.equals(c.val)); }\n")

out.write("public static void myLess(MyBool a, MyInt b, MyInt c){ a.val = (b.val < c.val); }\n")
out.write("public static void myGreater(MyBool a, MyInt b, MyInt c){ a.val = (b.val > c.val); }\n")
out.write("public static void myLessEqual(MyBool a, MyInt b, MyInt c){ a.val = (b.val <= c.val); }\n")
out.write("public static void myGreaterEqual(MyBool a, MyInt b, MyInt c){ a.val = (b.val >= c.val); }\n")

out.write("public static MyBool myAssign(MyBool b){ MyBool a = new MyBool(b.val); return a; }\n")
out.write("public static MyInt myAssign(MyInt b){ MyInt a = new MyInt(b.val); return a; }\n")
out.write("public static MyInt[] myAssign(MyInt[] b){ MyInt a[] = new MyInt[b.length]; for(int i = 0; i < b.length; i++) a[i] = new MyInt(b[i].val); return a; }\n")
out.write("public static MyString myAssign(MyString b){ MyString a = new MyString(b.val); return a; }\n")

out.write("public static void myAnd(MyBool a, MyBool b, MyBool c){ a.val = (b.val && c.val); }\n")
out.write("public static void myOr(MyBool a, MyBool b, MyBool c){ a.val = (b.val || c.val); }\n")
out.write("public static void myNot(MyBool a, MyBool b){ a.val = (!b.val); }\n")

out.write("public static void myPrint(MyString a){ System.out.println(\"\\n\"+a.val); }\n")
out.write("public static void myPrint(String a){ myPrint(new MyString(a)); }\n")
out.write("public static boolean myIf(MyBool a){ System.out.print(\"b\" + a.val + \" \"); return a.val; }\n")

out.write("public static void myAdd(MyInt a, MyInt b, int c){ myAdd(a,b,new MyInt(c)); }\n")
out.write("public static void myAdd(MyInt a, int b, MyInt c){ myAdd(a,new MyInt(b),c); }\n")
out.write("public static void myAdd(MyInt a, int b, int c){ myAdd(a,new MyInt(b),new MyInt(c)); }\n")
out.write("public static void myDel(MyInt a, MyInt b, int c){ myDel(a,b,new MyInt(c)); }\n")
out.write("public static void myDel(MyInt a, int b, MyInt c){ myDel(a,new MyInt(b),c); }\n")
out.write("public static void myDel(MyInt a, int b, int c){ myDel(a,new MyInt(b),new MyInt(c)); }\n")
out.write("public static void myMul(MyInt a, MyInt b, int c){ myMul(a,b,new MyInt(c)); }\n")
out.write("public static void myMul(MyInt a, int b, MyInt c){ myMul(a,new MyInt(b),c); }\n")
out.write("public static void myMul(MyInt a, int b, int c){ myMul(a,new MyInt(b),new MyInt(c)); }\n")
out.write("public static void myDiv(MyInt a, MyInt b, int c){ myDiv(a,b,new MyInt(c)); }\n")
out.write("public static void myDiv(MyInt a, int b, MyInt c){ myDiv(a,new MyInt(b),c); }\n")
out.write("public static void myDiv(MyInt a, int b, int c){ myDiv(a,new MyInt(b),new MyInt(c)); }\n")
out.write("public static void myMod(MyInt a, MyInt b, int c){ myMod(a,b,new MyInt(c)); }\n")
out.write("public static void myMod(MyInt a, int b, MyInt c){ myMod(a,new MyInt(b),c); }\n")
out.write("public static void myMod(MyInt a, int b, int c){ myMod(a,new MyInt(b),new MyInt(c)); }\n")
out.write("public static void myInd(MyInt a, MyInt[] b, int c){ myInd(a,b,new MyInt(c)); }\n")
out.write("public static void myInd(MyInt a, int[] b, int c){ myInd(a,I.myAssign(b),new MyInt(c)); }\n")
out.write("public static void myInd(MyString a, MyString[] b, int c){ myInd(a,b,new MyInt(c)); }\n")

out.write("public static void myEquals(MyBool a, MyBool b, boolean c){ myEquals(a, b, new MyBool(c)); }\n")
out.write("public static void myEquals(MyBool a, MyInt b, int c){ myEquals(a, b, new MyInt(c)); }\n")
out.write("public static void myEquals(MyBool a, MyString b, String c){ myEquals(a, b, new MyString(c)); }\n")
out.write("public static void myEquals(MyBool a, boolean b, MyBool c){ myEquals(a, new MyBool(b), c); }\n")
out.write("public static void myEquals(MyBool a, int b, MyInt c){ myEquals(a, new MyInt(b), c); }\n")
out.write("public static void myEquals(MyBool a, String b, MyString c){ myEquals(a, new MyString(b), c); }\n")
out.write("public static void myEquals(MyBool a, boolean b, boolean c){ myEquals(a, new MyBool(b), new MyBool(c)); }\n")
out.write("public static void myEquals(MyBool a, int b, int c){ myEquals(a, new MyInt(b), new MyInt(c)); }\n")
out.write("public static void myEquals(MyBool a, String b, String c){ myEquals(a, new MyString(b), new MyString(c)); }\n")

out.write("public static void myLess(MyBool a, MyInt b, int c){ myLess(a, b, new MyInt(c)); }\n")
out.write("public static void myGreater(MyBool a, MyInt b, int c){ myGreater(a, b, new MyInt(c)); }\n")
out.write("public static void myLessEqual(MyBool a, MyInt b, int c){ myLessEqual(a, b, new MyInt(c)); }\n")
out.write("public static void myGreaterEqual(MyBool a, MyInt b, int c){ myGreaterEqual(a, b, new MyInt(c)); }\n")
out.write("public static void myLess(MyBool a, int b, MyInt c){ myLess(a, new MyInt(b), c); }\n")
out.write("public static void myGreater(MyBool a, int b, MyInt c){ myGreater(a, new MyInt(b), c); }\n")
out.write("public static void myLessEqual(MyBool a, int b, MyInt c){ myLessEqual(a, new MyInt(b), c); }\n")
out.write("public static void myGreaterEqual(MyBool a, int b, MyInt c){ myGreaterEqual(a, new MyInt(b), c); }\n")
out.write("public static void myLess(MyBool a, int b, int c){ myLess(a, new MyInt(b), new MyInt(c)); }\n")
out.write("public static void myGreater(MyBool a, int b, int c){ myGreater(a, new MyInt(b), new MyInt(c)); }\n")
out.write("public static void myLessEqual(MyBool a, int b, int c){ myLessEqual(a, new MyInt(b), new MyInt(c)); }\n")
out.write("public static void myGreaterEqual(MyBool a, int b, int c){ myGreaterEqual(a, new MyInt(b), new MyInt(c)); }\n")

out.write("public static MyBool myAssign(boolean b){ return myAssign(new MyBool(b)); }\n")
out.write("public static MyInt myAssign(int b){ return myAssign(new MyInt(b)); }\n")
out.write("public static MyInt[] myAssign(int[] b){ MyInt a[] = new MyInt[b.length]; for(int i = 0; i < b.length; i++) a[i] = new MyInt(b[i]); return myAssign(a); }\n")
out.write("public static MyString myAssign(String b){ return myAssign(new MyString(b)); }\n")

out.write("}\n")
