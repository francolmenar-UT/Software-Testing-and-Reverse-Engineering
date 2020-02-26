def create_all(out):
    """
    Calls all the create_X methods
    :param out: destination file in which the code is written
    """
    create_math_method(out)
    create_arr_assign_method(out)
    create_eq_comp_method(out)
    create_gos_comp_method(out)
    create_mybool_assign_method(out)
    create_and_or_not_method(out)
    create_printing_method(out)
    create_new_math_method(out)
    create_new_eq_comp_method(out)
    create_new_gos_comp_method(out)
    create_new_mybool_assign_method(out)


def create_math_method(out):
    """
    Writes the Mathematical methods into the file
    :param out: destination file in which the code is written
    """
    out.write("public static void myAdd(MyInt a, MyInt b, MyInt c){ a.val = b.val+c.val; }\n")
    out.write("public static void myDel(MyInt a, MyInt b, MyInt c){ a.val = b.val-c.val;  }\n")
    out.write("public static void myMul(MyInt a, MyInt b, MyInt c){ a.val = b.val*c.val;  }\n")
    out.write("public static void myDiv(MyInt a, MyInt b, MyInt c){ a.val = b.val/c.val;  }\n")
    out.write("public static void myMod(MyInt a, MyInt b, MyInt c){ a.val = b.val%c.val;  }\n")


def create_arr_assign_method(out):
    """
    Writes the assignments methods regarding arrays into the file
    :param out: destination file in which the code is written
    """
    out.write("public static void myInd(MyInt a, MyInt[] b, MyInt c){ a.val = b[c.val].val; }\n")
    out.write("public static void myInd(MyString a, MyString[] b, MyInt c){ a.val = b[c.val].val; }\n")


def create_eq_comp_method(out):
    """
    Writes the Equal comparison methods into the file
    :param out: destination file in which the code is written
    """
    out.write("public static void myEquals(MyBool a, MyBool b, MyBool c){ a.val = (b.val == c.val); }\n")
    out.write("public static void myEquals(MyBool a, MyInt b, MyInt c){ a.val = (b.val == c.val); }\n")
    out.write("public static void myEquals(MyBool a, MyString b, MyString c){ a.val = (b.val.equals(c.val)); }\n")


def create_gos_comp_method(out):
    """
    Writes the Greater or smaller comparison  methods into the file
    It only takes MyInt
    :param out: destination file in which the code is written
    """
    out.write("public static void myLess(MyBool a, MyInt b, MyInt c){ a.val = (b.val < c.val); }\n")
    out.write("public static void myGreater(MyBool a, MyInt b, MyInt c){ a.val = (b.val > c.val); }\n")
    out.write("public static void myLessEqual(MyBool a, MyInt b, MyInt c){ a.val = (b.val <= c.val); }\n")
    out.write("public static void myGreaterEqual(MyBool a, MyInt b, MyInt c){ a.val = (b.val >= c.val); }\n")


def create_mybool_assign_method(out):
    """
    Writes the assignments methods regarding MyBool into the file
    :param out: destination file in which the code is written
    """
    out.write("public static MyBool myAssign(MyBool b){ MyBool a = new MyBool(b.val); return a; }\n")
    out.write("public static MyInt myAssign(MyInt b){ MyInt a = new MyInt(b.val); return a; }\n")
    out.write(
        "public static MyInt[] myAssign(MyInt[] b){ MyInt a[] = new MyInt[b.length]; for(int i = 0; i < b.length; i++) a[i] = new MyInt(b[i].val); return a; }\n")
    out.write("public static MyString myAssign(MyString b){ MyString a = new MyString(b.val); return a; }\n")


def create_and_or_not_method(out):
    """
    Writes the And, Or & Not Logic operations methods into the file
    :param out: destination file in which the code is written
    """
    out.write("public static void myAnd(MyBool a, MyBool b, MyBool c){ a.val = (b.val && c.val); }\n")
    out.write("public static void myOr(MyBool a, MyBool b, MyBool c){ a.val = (b.val || c.val); }\n")
    out.write("public static void myNot(MyBool a, MyBool b){ a.val = (!b.val); }\n")


def create_printing_method(out):
    """
    Writes the printing methods into the file
    There is a different method for MyBool, MyInt and MyString)
    :param out: destination file in which the code is written
    """
    out.write("public static void myPrint(MyString a){ System.out.println(\"\\n\"+a.val); }\n")
    out.write("public static void myPrint(String a){ myPrint(new MyString(a)); }\n")
    out.write("public static boolean myIf(MyBool a){ System.out.print(\"b\" + a.val + \" \"); return a.val; }\n")


def create_new_math_method(out):
    """
    Writes the Mathematical methods into the file
    A new MyInt is created
    :param out: destination file in which the code is written
    """
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


def create_new_eq_comp_method(out):
    """
    Writes the Equal comparison methods into the file
    A new MyBool is created
    :param out: destination file in which the code is written
    """
    out.write("public static void myEquals(MyBool a, MyBool b, boolean c){ myEquals(a, b, new MyBool(c)); }\n")
    out.write("public static void myEquals(MyBool a, MyInt b, int c){ myEquals(a, b, new MyInt(c)); }\n")
    out.write("public static void myEquals(MyBool a, MyString b, String c){ myEquals(a, b, new MyString(c)); }\n")
    out.write("public static void myEquals(MyBool a, boolean b, MyBool c){ myEquals(a, new MyBool(b), c); }\n")
    out.write("public static void myEquals(MyBool a, int b, MyInt c){ myEquals(a, new MyInt(b), c); }\n")
    out.write("public static void myEquals(MyBool a, String b, MyString c){ myEquals(a, new MyString(b), c); }\n")
    out.write(
        "public static void myEquals(MyBool a, boolean b, boolean c){ myEquals(a, new MyBool(b), new MyBool(c)); }\n")
    out.write("public static void myEquals(MyBool a, int b, int c){ myEquals(a, new MyInt(b), new MyInt(c)); }\n")
    out.write(
        "public static void myEquals(MyBool a, String b, String c){ myEquals(a, new MyString(b), new MyString(c)); }\n")


def create_new_gos_comp_method(out):
    """
    Writes the Greater or smaller comparison  methods into the file
    It only takes MyInt
    A new MyInt is created
    :param out: destination file in which the code is written
    """
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
    out.write(
        "public static void myGreaterEqual(MyBool a, int b, int c){ myGreaterEqual(a, new MyInt(b), new MyInt(c)); }\n")


def create_new_mybool_assign_method(out):
    """
    Writes the assignments methods regarding MyBool into the file
    A new MyBool is created
    :param out: destination file in which the code is written
    """
    out.write("public static MyBool myAssign(boolean b){ return myAssign(new MyBool(b)); }\n")
    out.write("public static MyInt myAssign(int b){ return myAssign(new MyInt(b)); }\n")
    out.write(
        "public static MyInt[] myAssign(int[] b){ MyInt a[] = new MyInt[b.length]; for(int i = 0; i < b.length; i++) a[i] = new MyInt(b[i]); return myAssign(a); }\n")
    out.write("public static MyString myAssign(String b){ return myAssign(new MyString(b)); }\n")
