import constants
from constants import *


def create_all(out, var_count, bool_count, str_count):
    """
    Calls all the create_X methods
    :param out: destination file in which the code is written
    """
    create_genetic(out)
    create_fuzzer(out)
    create_myclasses(out)
    create_i(out, var_count, bool_count, str_count)


def create_genetic(out):
    """
    Writes the classes used for the geneti algorithm into out
    :param out: destination file in which the code is written
    """
    with open(genetic_filename, 'r') as genetic_file:
        for line in genetic_file:
            out.write(line)


def create_fuzzer(out):
    """
    Writes the Fuzzer class into out
    :param out: destination file in which the code is written
    """
    with open(fuzzer_filename, 'r') as fuzzer_file:
        for line in fuzzer_file:
            out.write(line)


def create_myclasses(out):
    """
    Writes the MyInt, MyBool and MyString classes into out
    :param out: destination file in which the code is written
    """
    with open(classes_filename, 'r') as classes_file:
        for line in classes_file:
            out.write(line)


def create_i(out, var_count, bool_count, str_count):
    """
    Writes the I class into out
    :param out: destination file in which the code is written
    """
    with open(i_filename, 'r') as i_file:
        for line in i_file:
            if line.find("<insert_var>") != -1:
                for i in range(1, var_count + 1):
                    out.write("    public static MyInt var" + str(i) + " = new MyInt(0, false, " + str(i) + ");\n")
                out.write("\n")
                for i in range(1, bool_count + 1):
                    out.write(
                        "    public static MyBool bool" + str(i) + " = new MyBool(false, false, " + str(i) + ");\n")
                for i in range(1, str_count + 1):
                    out.write(
                        "    public static MyString str" + str(i) + " = new MyString(\"\", false, " + str(i) + ");\n")
                out.write("\n")
            else:
                out.write(line)
