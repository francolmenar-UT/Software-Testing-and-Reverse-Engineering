// Pair of elements
class Pair<A, B> {
    public A first;
    public B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }
}

/** Used log the elapsed time and the branch coverage. */
class Logging {
    public long startTime;
    public long elapsedTime;
    public BufferedWriter out;

    /**
     * Creates a new logger.
     * The name of the logfile depends on the current time.
     */
    public Logging() {
        startTime = System.nanoTime();
        elapsedTime = 0;
    }

    /**
     * @return the elapsedTime
     */
    public long getElapsedTime() {
        return System.nanoTime() - startTime;
    }

    /**
     * Write the elapsed time and the number of visited branches into the logfile.
     * @param numVisited number of visited branches
     */
    public void writeLog(int numVisited){
        try {
            out = new BufferedWriter(new FileWriter("log_problem1.txt", true));
            out.write(String.valueOf(getElapsedTime()) + ", " + String.valueOf(numVisited) + "\n");
            out.close();
        } catch (IOException e) {
            System.out.println("Could not write to file.");
            e.printStackTrace();
        }
    }
}

// Fuzzer
class Fuzzer {
    static public HashMap<Integer, Integer> graph = new HashMap<>(); // Graph created of the program
    static public HashMap<Integer, Boolean> if_branch = new HashMap<>();
    static public HashMap<Integer, Boolean> visited_branches = new HashMap<Integer, Boolean>();

    public static int inputCreated = 0;
    public static int randomFuzz = 10;  // Up to the iteration that we randomly generate the input
    public static int mutationRate = 3;
    public static final int mutation_reset =10; // Sets the iterations after which a mutation takes place

    public static int max_branches_visited = 0;
    public static int max_trait = 0;
    public static int iteration_number = 0;

    // Used to decide when the random fuzz will be used
    // Each #reset_iteration iterations the random fuzz is called
    public static final int reset_iteration = 100;
    // Used in random_fuzz to decide the posible new length of the input
    // new_length = [rdn_offset, iteration_number]
    public static final int rdn_offset = 10;

    public static boolean USE_TAINT = false;
    private static final Boolean DEBUG_NEW_BRANCH = true; // Enables printNewBranch
    private static final Boolean DEBUG_RANDOM = false; // Enables printRandomFuzz

    // Errors
    public static HashSet<Integer> errors_reached = new HashSet<>();

    public List<MyInput> created_inputs = new ArrayList<MyInput>();

    static MyString[] inputs;

    public void Fuzzer() {
    }

    /**
     * Generates a randon MyInput using the valid MyStrings of inputs
     *
     * @param inputs: Valid MyStrings to be used in the generation
     * @return MyInput which is randomly generated
     */
    public static MyInput random_fuzz(MyString[] inputs) {
        Random rand = new Random();
        int length = rand.nextInt(iteration_number) + rdn_offset; // TODO Check if it makes sense

        MyString[] fuzzStr = new MyString[length];

        for (int i = 0; i < length; i++) {
            int index = rand.nextInt(inputs.length);
            fuzzStr[i] = new MyString(inputs[index].val, true);
        }
        printRandomFuzz(inputs, fuzzStr, length);
        return new MyInput(fuzzStr);
    }

    /**
     * TODO: EXPLAIN THIS METHOD, I HAVE NO IDEA WHAT IT DOES
     *
     * @param goal
     * @param input
     * @return
     */
    static public Pair<Integer, Integer> approachLevel(int goal, MyInput input) {
        int distance = -1;
        int node = goal;

        while (!(input.visitedBranchs.contains(node) && if_branch.get(node)) || node == 0) {
            distance++;
            node = graph.get(node);

            if (node == 0)
                return new Pair(-2, -1);
        }

        return new Pair(distance, node);
    }

    /**
     * Genetic algorithm Fuzz
     * Entry point to the Fuzz process
     *
     * @param inputs: current Input in the form of MyString[]
     * @return the new input to be used as a MyInput Object
     */
    public MyInput fuzz(MyString[] inputs) {
        this.inputs = inputs;
        iteration_number++; // Update global iteration counter
        int visited_stats = 0; // Counter to check the amount of visited branchs

        // Count the visited branchs
        for (Boolean visit : visited_branches.values()) {
            if (visit)
                visited_stats++;
        }

        // Check if we acchieved a new maximum of visited branches
        if (visited_stats > max_branches_visited) {
            max_branches_visited = visited_stats; // Update counter
            printNewBranch(); // Debug print
        }

        // In the beginning just generate random inputs
        // Or when we reach the reset iteration
        if (iteration_number < randomFuzz || iteration_number % reset_iteration == 0) {
            MyInput result = random_fuzz(inputs); // Generate a random input
            created_inputs.add(result); // Update the history of created inputs
            return result;
        }

        // The input to mutate
        MyInput best_input = created_inputs.get(0);

        // Every #mutation_reset iterations create new input by mutating the one with more taints
        if (iteration_number % mutation_reset == 0 && USE_TAINT) {
            // find input with more traits
            for (MyInput input : created_inputs) {
                if (input.trait_count > best_input.trait_count) {
                    best_input = input;
                }
            }

        } else { // use AF and branch distance
            best_input = af_bdistance(best_input);
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

    /**
     * Refactored from fuzz
     * @return
     */
    public  MyInput af_bdistance(MyInput best_input){
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
        return best_input;
    }

    /*
    After an execution update the visited_branches with the data computed during the execution
    */
    public void after_execution(MyInput input, int trait_count) {
        input.trait_count = trait_count;
        for (int branch : input.visitedBranchs) {
            visited_branches.put(branch, true);
        }
        if (trait_count > max_trait)
            max_trait = input.trait_count;
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
     * Prints debug informatiion regarding the method random_fuzz
     *
     * @param valid_inputs: Valid MyStrings to be used in the generation of the new input
     * @param new_input:    New value created through random fuzz
     * @param length:       Leght calculated for the new random value
     */
    public static void printRandomFuzz(MyString[] valid_inputs, MyString[] new_input, int length) {
        if (!DEBUG_RANDOM) return; // It is only printed if DEBUG_RANDOM is true
        System.err.println("\n******* Random Fuzzer *******");
        System.err.println("\tIteration_number: " + iteration_number);

        System.err.print("\tValid inputs: ");
        printMyArrString(valid_inputs);

        System.err.print("\tNew input: ");
        printMyArrString(new_input);

        System.err.println("\tLenght of the Input: " + length + " == " + new_input.length);
    }
}


