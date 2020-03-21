// General class
class MyVariable<T> {
    public T val;
    public boolean flow = false; // Used for tainting
    public int id = -1;

    public MyVariable(T v) {
        this.val = v;
    }

    public MyVariable(T v, boolean f) {
        this.val = v;
        this.flow = f;
    }

    public MyVariable(T v, boolean f, int id) {
        this.val = v;
        this.flow = f;
        this.id = id;
    }
}

//MyInt
class MyInt extends MyVariable<Integer> {
    public MyInt(int v) {
        super(v);
    }

    public MyInt(int v, boolean b) {
        super(v, b);
    }

    public MyInt(int v, boolean b, int id) {
        super(v, b, id);
    }
}

//MyBool
class MyBool extends MyVariable<Boolean> {
    public float branchDistance = (float) -1.0; // Used for the branch distance calculation

    public MyBool(boolean v) {
        super(v);
    }

    public MyBool(boolean v, boolean b) {
        super(v, b);
    }

    public MyBool(boolean v, boolean b, int id) {
        super(v, b, id);
    }

    public void setBranchDistance(float branchDistance) {
        this.branchDistance = branchDistance;
    }
}

//MyString
class MyString extends MyVariable<String> {
    public MyString(String v) {
        super(v);
    }

    public MyString(String v, boolean b) {
        super(v, b);
    }

    public MyString(String v, boolean b, int id) {
        super(v, b, id);
    }
}

//MyInput
class MyInput {
    public MyString[] myStr; // Array of Strings-char fuzzed
    public List<Integer> visitedBranchs = new ArrayList<Integer>(); // All the visited branches by a fuzzed input
    public HashMap<Integer, Float> branch_distance = new HashMap<Integer, Float>();  // Hash map with the id of the visited branches and its branch distance

    public int trait_count = 0;

    public MyInput(MyString[] myStr) {
        this.myStr = myStr;
    }

    public void addBranch(int branch) {
        visitedBranchs.add(branch);
    }

    public void setBranchDistance(int branch_id, float branchDistance) {
        this.branch_distance.put(branch_id, branchDistance);
    }
}

class Errors {
    public static void __VERIFIER_error(int i) {
        Fuzzer.errors_reached.add(i);
        throw new IllegalArgumentException( "error_" + i );
    }
}