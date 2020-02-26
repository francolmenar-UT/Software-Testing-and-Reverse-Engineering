class I {
<insert_var>

    public static void myAdd(MyInt a, MyInt b, MyInt c){ a.val = b.val+c.val; }
    public static void myDel(MyInt a, MyInt b, MyInt c){ a.val = b.val-c.val;  }
    public static void myMul(MyInt a, MyInt b, MyInt c){ a.val = b.val*c.val;  }
    public static void myDiv(MyInt a, MyInt b, MyInt c){ a.val = b.val/c.val;  }
    public static void myMod(MyInt a, MyInt b, MyInt c){ a.val = b.val%c.val;  }

    public static void myInd(MyInt a, MyInt[] b, MyInt c){ a.val = b[c.val].val; }
    public static void myInd(MyString a, MyString[] b, MyInt c){ a.val = b[c.val].val; }

    public static void myEquals(MyBool a, MyBool b, MyBool c){ a.val = (b.val == c.val); }
    public static void myEquals(MyBool a, MyInt b, MyInt c){ a.val = (b.val == c.val); }
    public static void myEquals(MyBool a, MyString b, MyString c){ a.val = (b.val.equals(c.val)); }

    public static void myLess(MyBool a, MyInt b, MyInt c){ a.val = (b.val < c.val); }
    public static void myGreater(MyBool a, MyInt b, MyInt c){ a.val = (b.val > c.val); }
    public static void myLessEqual(MyBool a, MyInt b, MyInt c){ a.val = (b.val <= c.val); }
    public static void myGreaterEqual(MyBool a, MyInt b, MyInt c){ a.val = (b.val >= c.val); }

    public static MyBool myAssign(MyBool b){ MyBool a = new MyBool(b.val); return a; }
    public static MyInt myAssign(MyInt b){ MyInt a = new MyInt(b.val); return a; }
    public static MyInt[] myAssign(MyInt[] b){ MyInt a[] = new MyInt[b.length]; for(int i = 0; i < b.length; i++) a[i] = new MyInt(b[i].val); return a; }
    public static MyString myAssign(MyString b){ MyString a = new MyString(b.val); return a; }

    public static void myAnd(MyBool a, MyBool b, MyBool c){ a.val = (b.val && c.val); }
    public static void myOr(MyBool a, MyBool b, MyBool c){ a.val = (b.val || c.val); }
    public static void myNot(MyBool a, MyBool b){ a.val = (!b.val); }

    public static void myPrint(MyString a){ System.out.println("\n"+a.val); }
    public static void myPrint(String a){ myPrint(new MyString(a)); }
    public static boolean myIf(MyBool a){ System.out.print("b" + a.val + " "); return a.val; }

    public static void myAdd(MyInt a, MyInt b, int c){ myAdd(a,b,new MyInt(c)); }
    public static void myAdd(MyInt a, int b, MyInt c){ myAdd(a,new MyInt(b),c); }
    public static void myAdd(MyInt a, int b, int c){ myAdd(a,new MyInt(b),new MyInt(c)); }
    public static void myDel(MyInt a, MyInt b, int c){ myDel(a,b,new MyInt(c)); }
    public static void myDel(MyInt a, int b, MyInt c){ myDel(a,new MyInt(b),c); }
    public static void myDel(MyInt a, int b, int c){ myDel(a,new MyInt(b),new MyInt(c)); }
    public static void myMul(MyInt a, MyInt b, int c){ myMul(a,b,new MyInt(c)); }
    public static void myMul(MyInt a, int b, MyInt c){ myMul(a,new MyInt(b),c); }
    public static void myMul(MyInt a, int b, int c){ myMul(a,new MyInt(b),new MyInt(c)); }
    public static void myDiv(MyInt a, MyInt b, int c){ myDiv(a,b,new MyInt(c)); }
    public static void myDiv(MyInt a, int b, MyInt c){ myDiv(a,new MyInt(b),c); }
    public static void myDiv(MyInt a, int b, int c){ myDiv(a,new MyInt(b),new MyInt(c)); }
    public static void myMod(MyInt a, MyInt b, int c){ myMod(a,b,new MyInt(c)); }
    public static void myMod(MyInt a, int b, MyInt c){ myMod(a,new MyInt(b),c); }
    public static void myMod(MyInt a, int b, int c){ myMod(a,new MyInt(b),new MyInt(c)); }
    public static void myInd(MyInt a, MyInt[] b, int c){ myInd(a,b,new MyInt(c)); }
    public static void myInd(MyInt a, int[] b, int c){ myInd(a,I.myAssign(b),new MyInt(c)); }
    public static void myInd(MyString a, MyString[] b, int c){ myInd(a,b,new MyInt(c)); }

    public static void myEquals(MyBool a, MyBool b, boolean c){ myEquals(a, b, new MyBool(c)); }
    public static void myEquals(MyBool a, MyInt b, int c){ myEquals(a, b, new MyInt(c)); }
    public static void myEquals(MyBool a, MyString b, String c){ myEquals(a, b, new MyString(c)); }
    public static void myEquals(MyBool a, boolean b, MyBool c){ myEquals(a, new MyBool(b), c); }
    public static void myEquals(MyBool a, int b, MyInt c){ myEquals(a, new MyInt(b), c); }
    public static void myEquals(MyBool a, String b, MyString c){ myEquals(a, new MyString(b), c); }
    public static void myEquals(MyBool a, boolean b, boolean c){ myEquals(a, new MyBool(b), new MyBool(c)); }
    public static void myEquals(MyBool a, int b, int c){ myEquals(a, new MyInt(b), new MyInt(c)); }
    public static void myEquals(MyBool a, String b, String c){ myEquals(a, new MyString(b), new MyString(c)); }

    public static void myLess(MyBool a, MyInt b, int c){ myLess(a, b, new MyInt(c)); }
    public static void myGreater(MyBool a, MyInt b, int c){ myGreater(a, b, new MyInt(c)); }
    public static void myLessEqual(MyBool a, MyInt b, int c){ myLessEqual(a, b, new MyInt(c)); }
    public static void myGreaterEqual(MyBool a, MyInt b, int c){ myGreaterEqual(a, b, new MyInt(c)); }
    public static void myLess(MyBool a, int b, MyInt c){ myLess(a, new MyInt(b), c); }
    public static void myGreater(MyBool a, int b, MyInt c){ myGreater(a, new MyInt(b), c); }
    public static void myLessEqual(MyBool a, int b, MyInt c){ myLessEqual(a, new MyInt(b), c); }
    public static void myGreaterEqual(MyBool a, int b, MyInt c){ myGreaterEqual(a, new MyInt(b), c); }
    public static void myLess(MyBool a, int b, int c){ myLess(a, new MyInt(b), new MyInt(c)); }
    public static void myGreater(MyBool a, int b, int c){ myGreater(a, new MyInt(b), new MyInt(c)); }
    public static void myLessEqual(MyBool a, int b, int c){ myLessEqual(a, new MyInt(b), new MyInt(c)); }
    public static void myGreaterEqual(MyBool a, int b, int c){ myGreaterEqual(a, new MyInt(b), new MyInt(c)); }

    public static MyBool myAssign(boolean b){ return myAssign(new MyBool(b)); }
    public static MyInt myAssign(int b){ return myAssign(new MyInt(b)); }
    public static MyInt[] myAssign(int[] b){ MyInt a[] = new MyInt[b.length]; for(int i = 0; i < b.length; i++) a[i] = new MyInt(b[i]); return myAssign(a); }
    public static MyString myAssign(String b){ return myAssign(new MyString(b)); }
}