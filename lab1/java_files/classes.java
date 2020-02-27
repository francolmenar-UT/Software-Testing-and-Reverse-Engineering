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

// Maybe a struct for a String wth ids of the branches
// We need to create a graph -> method to know which if statements have to be trigered to get to a desired branch
// Method to calculate the branch distance
class Input {
    public String input = "";
    public List<Integer> visitedBranchs = new ArrayList<Integer>();
    public int branchDistance = -1;

    public Input (String input) {
        this.input = input;
    }

    public addBranch(int branch){
        visitedBranchs.add(branch);
    }

    public void setBranchDistance(int branchDistance) {
        this.branchDistance = branchDistance;
    }
}

