// Pair of elements
class Pair<A, B> {
    public A first;
    public B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }
}

// Fuzzer
// TODO Check which variables are not needed
class Fuzzer {
    public static final String INPUT = "EIFJCDGABHEIFJCDGABH";
    private static final Boolean DEBUG_NEW_BRANCH = true; // Enables printNewBranch
    private static final Boolean DEBUG_SAT = true; // Enables SAT Debugger

    public HashMap<Integer, Integer> graph = new HashMap<>(); // Graph created of the program
    public HashMap<Integer, Boolean> if_branch = new HashMap<>();
    public HashMap<Integer, Boolean> visited_branches = new HashMap<Integer, Boolean>();
    public static int inputCreated = 0;
    public static int randomFuzz = 10; // Probably unused
    public static int mutationRate = 3; // Probably unused

    public static int max_branches_visited = 0;
    public static int max_trait = 0; // Probably unused
    public static int iteration_number = 0;

    public static boolean USE_TAINT = false; // Probably unused

    // Errors
    public static HashSet<Integer> errors_reached = new HashSet<>();

    public List<MyInput> created_inputs = new ArrayList<MyInput>();

    public Fuzzer() {
    }

    public Pair<Integer, Integer> approachLevel(int goal, MyInput input) {
        int distance = -1;
        int node = goal;

        String trace = new String("");

        while (!(input.visitedBranchs.contains(node) && this.if_branch.get(node)) || node == 0) {
            distance++;
            node = this.graph.get(node);

            if (node == 0)
                return new Pair(-2, -1);
        }

        return new Pair(distance, node);
    }

    /**
     * Returns a MyInput from a String
     *
     * @param str:  String to be converted to MyInput
     * @param bool: boolen to set the flow
     * @return
     */
    public MyInput StrToInput(String str, Boolean bool) {
        MyString[] Mystr = new MyString[str.length()];
        for (int i = 0; i < str.length(); i++) {
            Mystr[i] = new MyString(Character.toString(str.charAt(i)), bool); // Each char as String
        }
        return new MyInput(Mystr);
    }

    /**
     * Print information when a new input triggers a new branch
     */
    public void printNewBranch() {
        if (!DEBUG_NEW_BRANCH) return; // It is only printed if DEBUG_NEW_BRANCH is true
        System.err.println("\n************ FUZZER ************");
        System.err.println("Iteration: " + iteration_number + " visited " + max_branches_visited + " branches out of " + visited_branches.size());
        System.err.println("\tErrors reached: " + errors_reached.size());
        if (created_inputs.size() == 0) { // Avoid index issues
            System.err.println("\tTraits with this input: " + created_inputs.get(created_inputs.size()).trait_count);
        } else {
            System.err.println("\tTraits with this input: " + created_inputs.get(created_inputs.size() - 1).trait_count);
        }
        System.err.println("\tMax traits: " + max_trait);
        System.err.print("\tInput used: ");

        for (MyString s : created_inputs.get(created_inputs.size() - 1).myStr) {
            System.err.print(s.val);
        }
        System.err.println();
    }

    /**
     * Print information when a new input triggers a longer branch - or a new one
     *
     * @param condition:   Last Boolean Expression
     * @param new_input:   MyInput to be created
     * @param satisfiable: boolean used to knwo which branch has been taken
     */
    public static void printSAT(BoolExpr condition, MyInput new_input, Boolean satisfiable) {
        if (!DEBUG_SAT) return; // It is only printed if DEBUG_SAT is true
        System.err.println("\n************ SAT SOLVER ************");
        System.err.println("\tLast Condition: " + condition.toString());
        if (satisfiable) {
            System.err.println("\tBranch Reacheable, the condition is Satisfiable!");
        } else {
            System.err.println("Branch unreachable, the condition is NOT Satisfiable");
        }
        System.err.print("New input created: ");
        printMyInput(new_input);
    }

    /**
     * Auxiliary method for printing a MyInput
     * It mainly calls to printMyArrString
     *
     * @param input: MyInput to be printed
     */
    public static void printMyInput(MyInput input) {
        printMyArrString(input.myStr);
    }

    /**
     * Auxiliary method for printing a MyString[]
     *
     * @param str: MyString[] to be printed
     */
    public static void printMyArrString(MyString[] str) {
        for (int i = 0; i < str.length; i++) {
            System.err.print(str[i].val);
        }
        System.err.print("\n");
    }

    /**
     * Generates the new input for the program
     * If it is the first iteration it gets the fixed INPUT
     * Otherwise, it uses the SAT solver to decide the new input
     *
     * @param current_input: input of the actual execution of the program
     * @param ctx:           z3 context
     * @param z3f:           Boolean Expresion representing the Path Constraint
     * @param condition:     Last condition triggered by the input
     * @param valid_inputs:  Valid characters for the input of the program
     * @return the MyInput which corresponds to the new input for the program
     */
    public MyInput fuzz_sat(MyString[] current_input, Context ctx, BoolExpr z3f, Expr condition, MyString[] valid_inputs) {
        iteration_number++;
        // stats
        int visited_stats = 0;
        for (Boolean visit : visited_branches.values()) {
            if (visit)
                visited_stats++;
        }
        // We found a longer branch
        if (visited_stats > max_branches_visited) {
            max_branches_visited = visited_stats;
            printNewBranch();
        }

        if (iteration_number < 2) { // Use the defined String as an starting point
            MyInput result = StrToInput(INPUT, true);
            created_inputs.add(result);
            return result;
        } else { // Use the SAT Solver
            MyInput result = sat_solver(ctx, z3f, (BoolExpr) condition, valid_inputs, current_input);
            created_inputs.add(result);
            return result;
        }
    }

    /**
     * Runs the SAT Solver
     * If it is Satisfiable, only one character is modified for the new input
     * Otherwise, a new random MyInput is created
     *
     * @param ctx:           z3 context
     * @param z3f:           Boolean Expresion representing the Path Constraint
     * @param condition:     Last condition triggered by the input
     * @param valid_inputs:  Valid characters for the input of the program
     * @param current_input: input of the actual execution of the program
     * @return the MyInput which corresponds to the new input for the program
     */
    public static MyInput sat_solver(Context ctx, BoolExpr z3f, BoolExpr condition, MyString[] valid_inputs, MyString[] current_input) {
        MyInput new_input = new MyInput(new MyString[]{new MyString("")}); // Empty MyInput for later use

        Solver s = ctx.mkSolver(); // create the Solver
        s.add(z3f); // Add the Path Constraint to the solver
        s.add(ctx.mkEq(condition, condition.isTrue() ? ctx.mkFalse() : ctx.mkTrue())); // Add the !branch

        // path-constraint + branch=false -> SAT
        if (s.check() == Status.SATISFIABLE) { // The branch can be reachable
            // Create a new input by changing one random character
            new_input = slight_fuzz(current_input, valid_inputs);
            printSAT(condition, new_input, true);
        } else { // The branch is unreachable
            new_input = random_fuzz(valid_inputs); // Return a random input
            printSAT(condition, new_input, false);
        }
        return new_input;
    }

    /**
     * Generates a new input by changing only one character
     *
     * @param current_input: original input which is going to be changed only one char
     * @param valid_inputs:  valid charcters to be inserted in the input
     * @return new_input as a MyInput
     */
    public static MyInput slight_fuzz(MyString[] current_input, MyString[] valid_inputs) {
        Random rand = new Random();
        int count = 0; // Counter for exiting the while loop
        MyString[] new_input = current_input; // The new input is the old one with one char changed
        while (count < 10) { // To avoid an infinite loop if the characters are reapted
            int new_input_char = rand.nextInt(valid_inputs.length); // The char which is going to be inserted
            int char_to_change = rand.nextInt(current_input.length); // The char wich is going to be erased

            // Check that the chars are not the same
            if (current_input[char_to_change] != valid_inputs[new_input_char]) {
                new_input[char_to_change] = valid_inputs[new_input_char]; // Substitute the char
                break;
            }
        }
        return new MyInput(new_input); // Return the new input as a MyInput
    }

    /**
     * Generates a randon MyInput using the valid MyStrings of inputs
     *
     * @param inputs: Valid MyStrings to be used in the generation
     * @return MyInput which is randomly generated
     */
    public static MyInput random_fuzz(MyString[] inputs) {
        Random rand = new Random();
        int length = rand.nextInt(iteration_number) + 10;
        MyString[] fuzzStr = new MyString[length];

        for (int i = 0; i < length; i++) {
            int index = rand.nextInt(inputs.length);
            fuzzStr[i] = new MyString(inputs[index].val, true);
        }
        return new MyInput(fuzzStr);
    }

    //  ----- Genetic Algorithm Implementation ----
    // Normal Fuzz (lab1)
    public MyInput fuzz(MyString[] inputs) {
        iteration_number++;
        // stats
        int visited_stats = 0;
        for (Boolean visit : visited_branches.values()) {
            if (visit)
                visited_stats++;
        }
        if (visited_stats > max_branches_visited) {
            max_branches_visited = visited_stats;
            printNewBranch();
        }

        // In the beginning just generate random inputs
        if (iteration_number < randomFuzz || iteration_number % 100 == 0) {
            MyInput result = random_fuzz(inputs);
            created_inputs.add(result);
            return result;
        }

        // The input to mutate
        MyInput best_input = created_inputs.get(0);

        // Every 10 iterations create new input by mutating the one with more taints
        if (iteration_number % 10 == 0 && USE_TAINT) {
            // find input with more traits
            for (MyInput input : created_inputs) {
                if (input.trait_count > best_input.trait_count) {
                    best_input = input;
                }
            }

        } else { // use AF and branch distance
            int target_branch = -1;

            int minAL = -1;
            float minDistance = -1;
            int branch_id = -1;

            // Select a branch not visited
            for (Map.Entry<Integer, Boolean> entry : visited_branches.entrySet()) {
                Integer branch = entry.getKey();
                Boolean visited = entry.getValue();

                if (!visited) {
                    target_branch = branch;

                    // Find the best closest input to it
                    minAL = -1;
                    minDistance = -1;
                    branch_id = -1;
                    best_input = created_inputs.get(0);
                    for (MyInput input : created_inputs) {
                        Pair<Integer, Integer> res = approachLevel(target_branch, input);
                        if (res.first < 0) continue; //there was an error

                        if (minAL == -1 || res.first < minAL) {
                            minAL = res.first;
                            branch_id = res.second;
                            minDistance = input.branch_distance.get(branch_id);
                            best_input = input;
                        } else if (res.first == minAL) {
                            float distance = input.branch_distance.get(branch_id);
                            if (distance < minDistance && distance >= 0) {
                                minAL = res.first;
                                branch_id = res.second;
                                minDistance = distance;
                                best_input = input;
                            }
                        }
                    }
                    if (minDistance >= 0)
                        break;
                }
            }
        }
        MyString[] fuzzStr = new MyString[best_input.myStr.length];
        System.arraycopy(best_input.myStr, 0, fuzzStr, 0, best_input.myStr.length);

        Random rand = new Random();
        for (int i = 0; i < fuzzStr.length; i++) {
            if (rand.nextInt(100) < mutationRate) {
                int index = rand.nextInt(inputs.length);
                fuzzStr[i] = new MyString(inputs[index].val, true);
            }
        }
        MyInput result = new MyInput(fuzzStr);
        created_inputs.add(result);
        return result;
    }

    /*
    After an execution update the visited_branches with the data computed during the execution
    */
    public void after_execution(MyInput input, int trait_count) {
        input.trait_count = trait_count; // TODO Probably unused
        for (int branch : input.visitedBranchs) {
            visited_branches.put(branch, true);
        }
        if (trait_count > max_trait) // TODO Probably unused
            max_trait = input.trait_count;
    }
}
