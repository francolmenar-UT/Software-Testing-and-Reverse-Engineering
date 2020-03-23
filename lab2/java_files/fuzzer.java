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
     * Print information when a new input triggers a longer branch - or a new one
     */
    public void printNewBranch(){
        if (!DEBUG_NEW_BRANCH) return;
        System.err.println("\nIteration: " + iteration_number + " visited " + max_branches_visited + " branches out of " + visited_branches.size());
        System.err.println("\tErrors reached: " + errors_reached.size());
        System.err.println("\tTraits with this input: " + created_inputs.get(created_inputs.size() - 1).trait_count);
        System.err.println("\tMax traits: " + max_trait);

        System.err.print("\tInput used: ");
        for (MyString s : created_inputs.get(created_inputs.size() - 1).myStr) {
            System.err.print(s.val);
        }
        System.err.println();
    }

    /**
     * Generates the input for the program
     * If it is the first iteration it gets the fixed INPUT
     * Otherwise, it uses the SAT solver to get a new input which trigers a new branch
     *
     * @param inputs: TODO I think that they are not being used, Maybe after the second iteration
     * @return the MyInput which corresponds to the new input for the program
     */
    public MyInput fuzz_sat(MyString[] inputs) {
        iteration_number++;
        // stats
        int visited_stats = 0;
        for (Boolean visit : visited_branches.values()) {
            if (visit)
                visited_stats++;
        }
        // We found a longer branch  TODO Ask if it is still needed
        if (visited_stats > max_branches_visited) {
            max_branches_visited = visited_stats;
            printNewBranch();
        }

        // TODO Check that this is correct
        //  if (iteration_number < 2 || iteration_number % 100 == 0) {
        // In the beginning just return the predefined Input
        if (iteration_number < 2) {
            // Create the object to return
            return StrToInput(INPUT, true);
        } else { // Use the SAT Solver
            return StrToInput(INPUT, true); // TODO Change to SAT solver
        }
    }


    /**
     * Create the SAT solver and checks its result
     *
     * @param ctx
     * @param graph_c
     * @param instance_c
     */
    public static void sat_solver(Context ctx, BoolExpr graph_c, BoolExpr instance_c) {
        Solver s = ctx.mkSolver(); // create the Solver
        s.add(graph_c); // Add the Expressions to the solver
        s.add(instance_c);

        if (s.check() == Status.SATISFIABLE) { // Check the result of the solver
            Model m = s.getModel(); // Get the model
            // TODO Negate the last Expr of the comparisons in order to reach a new branch
            // Basically it's a Backtrack, you just go to the parent comparison to try to go to the other leaf

            // TODO Print the new Input that reaches this leaf
            System.out.println("Graph solution:");
            // TODO Iterate through the model to print the solution
            // TODO Reverse engineried the solution from the expresion

            /*  CHANGE, THIS JUST PRINTS THE SOLUTION OF THE SUDOKU
            for (int i = 0; i < 9; i++) {
                for (int j = 0; j < 9; j++)
                    System.out.print(" " + R[i][j]);
                System.out.println();
            }*/
        } else {
            System.out.println("Failed to solve the graph");
            // TODO I have no idea what happens then, Try to negate a new Expr? Go to the parent node?
        }
    }

    //  ----- Genetic Algorithm Implementation ----
    // Random Fuzz
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
    // Normal Fuzz
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
    TODO Is it needed to do more stuff here?
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
