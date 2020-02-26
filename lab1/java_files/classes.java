class MyVariable <T> {
    public T val;
    public boolean flow = false;
    public MyVariable(T v) { this.val = v; }
    public MyVariable(T v, boolean f) { this.val = v; this.flow = f; }
}

class MyInt extends MyVariable<Integer> {
    public MyInt(int v){ super(v); }
    public MyInt(int v, boolean b){ super(v, b); }
}

class MyBool extends MyVariable<Boolean> {
    public MyBool(boolean v){ super(v); }
    public MyBool(boolean v, boolean b){ super(v, b); }
}

class MyString extends MyVariable<String>{
    public MyString(String v){ super(v); }
    public MyString(String v, boolean b){ super(v, b); }
}

