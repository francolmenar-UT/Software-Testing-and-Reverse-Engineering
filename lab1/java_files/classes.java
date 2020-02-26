class MyInt {
    public int val = 0;
    public MyInt(int v){ this.val = v; }
}

class MyBool {
    public boolean val = false;
    public MyBool(boolean v){ this.val = v; }
}

class MyString {
    public String val = "";
    public boolean flow = false;
    public MyString(String v){ this.val = v; }
    public MyString(String v, boolean b){ this.val = v; this.flow = b; }
}