def create_all(out):
    """
    Calls all the create_X methods
    :param out: destination file in which the code is written
    """
    create_fuzzer(out)
    create_myint(out)
    create_mybool(out)
    create_mystring(out)
    create_i(out)


def create_fuzzer(out):
    """
    Writes the Fuzzer class into out
    :param out: destination file in which the code is written
    """
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


def create_myint(out):
    """
    Writes the MyInt class into out
    :param out: destination file in which the code is written
    """
    out.write("class MyInt {\n")
    out.write("public int val = 0;\n")
    out.write("public MyInt(int v){ this.val = v; }")
    out.write("}\n")


def create_mybool(out):
    """
    Writes the MyBool class into out
    :param out: destination file in which the code is written
    """
    out.write("class MyBool {\n")
    out.write("public boolean val = false;\n")
    out.write("public MyBool(boolean v){ this.val = v; }")
    out.write("}\n")


def create_mystring(out):
    """
    Writes the MyString class into out
    :param out: destination file in which the code is written
    """
    out.write("class MyString {\n")
    out.write("public String val = \"\";")
    out.write("public boolean flow = false;")
    out.write("public MyString(String v){ this.val = v; }")
    out.write("public MyString(String v, boolean b){ this.val = v; this.flow = b; }")
    out.write("}\n")


def create_i(out):
    """
    Writes the I class into out
    :param out: destination file in which the code is written
    """
    out.write("class I {\n")
    out.write("\n")
    for i in range(1, 50):
        out.write("public static MyInt var" + str(i) + " = new MyInt(0);\n")
    out.write("\n")
    for i in range(1, 50):
        out.write("public static MyBool bool" + str(i) + " = new MyBool(false);\n")
    for i in range(1, 50):
        out.write("public static MyString str" + str(i) + " = new MyString(\"\");\n")
    out.write("\n")
