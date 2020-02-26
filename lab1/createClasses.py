def create_all(out):
    """
    Calls all the create_X methods
    :param out: destination file in which the code is written
    """
    create_fuzzer(out)
    create_myclasses(out)
    create_i(out)


def create_fuzzer(out):
    """
    Writes the Fuzzer class into out
    :param out: destination file in which the code is written
    """
    fuzzer_filename = "java_files/fuzzer.java"
    with open(fuzzer_filename, 'r') as fuzzer_file:
        for line in fuzzer_file:
            out.write(line)


def create_myclasses(out):
    """
    Writes the MyInt, MyBool and MyString classes into out
    :param out: destination file in which the code is written
    """
    classes_filename = "java_files/classes.java"
    with open(classes_filename, 'r') as classes_file:
        for line in classes_file:
            out.write(line)


def create_i(out):
    """
    Writes the I class into out
    :param out: destination file in which the code is written
    """
    i_filename = "java_files/I.java"
    with open(i_filename, 'r') as i_file:
        for line in i_file:
            if line.find("<insert_var>") != -1:
                for i in range(1, 50):
                    out.write("    public static MyInt var" + str(i) + " = new MyInt(0);\n")
                out.write("\n")
                for i in range(1, 50):
                    out.write("    public static MyBool bool" + str(i) + " = new MyBool(false);\n")
                for i in range(1, 50):
                    out.write("    public static MyString str" + str(i) + " = new MyString(\"\");\n")
                out.write("\n")
            else:
                out.write(line)
