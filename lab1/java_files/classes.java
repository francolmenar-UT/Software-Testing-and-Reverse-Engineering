class MyVariable <T> {
    public T val;
    public boolean flow = false;
    public int id = -1;
    public MyVariable(T v) { this.val = v; }
    public MyVariable(T v, boolean f) { this.val = v; this.flow = f; }
    public MyVariable(T v, boolean f, int id) { this.val = v; this.flow = f; this.id = id; }
}

class MyInt extends MyVariable<Integer> {
    public MyInt(int v){ super(v); }
    public MyInt(int v, boolean b){ super(v, b); }
    public MyInt(int v, boolean b, int id){ super(v, b, id); }
}

class MyBool extends MyVariable<Boolean> {
    public float branchDistance = (float) -1.0;

    public MyBool(boolean v){ super(v); }
    public MyBool(boolean v, boolean b){ super(v, b); }
    public MyBool(boolean v, boolean b, int id){ super(v, b, id); }

    public void setBranchDistance(float branchDistance) {
        this.branchDistance = branchDistance;
    }
}

class MyString extends MyVariable<String>{
    public MyString(String v){ super(v); }
    public MyString(String v, boolean b){ super(v, b); }
    public MyString(String v, boolean b, int id){ super(v, b, id); }
}

// Maybe a struct for a String wth ids of the branches
// We need to create a graph -> method to know which if statements have to be trigered to get to a desired branch
// Method to calculate the branch distance
// As we have to store the branch distance in the Input we have to pass the struct to the comparison methods
class MyInput {
    public MyString [] myStr;
    public List<Integer> visitedBranchs = new ArrayList<Integer>();
    HashMap<Integer, Float> branch_distance = new HashMap<Integer, Float>();


    public MyInput (MyString[] myStr) {
        this.myStr = myStr;
    }

    public void addBranch(int branch){
        visitedBranchs.add(branch);
    }

    public void setBranchDistance(int branch_id, float branchDistance) {
        this.branch_distance.put(branch_id, branchDistance);
    }
}
