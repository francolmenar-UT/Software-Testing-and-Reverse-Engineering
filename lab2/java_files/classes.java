import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;

// General class
class MyVariable<T> {
    public T val;
    public boolean flow = false; // Used for tainting
    public int id = -1;

    public Expr expr; // Symbolic expression
    public int varType = 0;
    public static int symbolic_int_counter = 0;
    public static int symbolic_string_counter = 0;
    public static int symbolic_bool_counter = 0;
    public static int symbolic_input_counter = 0;

    private void setExpr(boolean sym_input) {
        if (this instanceof MyInt) {
            String expr_name = sym_input ? "inp_" + symbolic_input_counter++ : "int_" + symbolic_int_counter++;
            expr = I.ctx.mkConst(I.ctx.mkSymbol(expr_name), I.ctx.getIntSort());
        } else if (this instanceof MyString) {
            String expr_name = sym_input ? "inp_" + symbolic_input_counter++ : "str_" + symbolic_string_counter++;
            expr = I.ctx.mkConst(I.ctx.mkSymbol(expr_name), I.ctx.getStringSort());
        } else if (this instanceof MyBool) {
            String expr_name = sym_input ? "inp_" + symbolic_input_counter++ : "bol_" + symbolic_bool_counter++;
            expr = I.ctx.mkConst(I.ctx.mkSymbol(expr_name), I.ctx.getBoolSort());
        }
        else {
            System.err.println("Wrong varType: " + varType);
            System.exit(1);
        }
    }

    public MyVariable(T v) {
        this.val = v;

        this.setExpr(false);
    }

    public MyVariable(T v, boolean f) {
        this.val = v;
        this.flow = f;

        this.setExpr(false);
    }

    public MyVariable(T v, boolean f, int id) {
        this.val = v;
        this.flow = f;
        this.id = id;

        this.setExpr(false);
    }

    /**
     * Use this function to create MyInput variables setting sym_input to true.
     * It sets the name of expr to recognisable value
     */
    public MyVariable(T v, boolean f, boolean sym_input) {
        this.val = v;
        this.flow = f;

        this.setExpr(sym_input);
    }
}

// MyInt
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

// MyBool
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

// MyString
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

// MyInput
class MyInput {
    public MyString[] myStr; // Array of Strings-char fuzzed
    public List<Integer> visitedBranchs = new ArrayList<Integer>(); // All the visited branches by a fuzzed input
    public HashMap<Integer, Float> branch_distance = new HashMap<Integer, Float>(); // Hash map with the id of the
                                                                                    // visited branches and its branch
                                                                                    // distance

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
        throw new IllegalArgumentException("error_" + i);
    }
}

/** Used log the elapsed time and the branch coverage. */
class Logging {
    public long startTime;
    public long elapsedTime;
    public PrintWriter out;

    public Logging() {
        startTime = System.nanoTime();
        elapsedTime = 0;
        try {
            out = new PrintWriter(new BufferedWriter(new FileWriter("log_" + new Date(), true)));
        } catch (IOException e) {
            System.out.println("Could not write to file.");
            e.printStackTrace();
        }
    }

    /**
     * @return the elapsedTime
     */
    public long getElapsedTime() {
        return startTime - System.nanoTime();
    }

    /**TODO: Add branch distance. */
    public void writeLog(){
        out.write(String.valueOf(getElapsedTime()) + ", " + "branchDistance");
    }

}