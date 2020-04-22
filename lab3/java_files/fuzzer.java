/**
 * Fuzzer class
 */
class Fuzzer {
    /*********************** Graph Variables ***********************/
    static public HashMap<Integer, Integer> graph = new HashMap<>(); // Graph created of the program
    static public HashMap<Integer, List<Integer> > rev_graph = new HashMap<>();
    static public HashMap<Integer, Boolean> if_branch = new HashMap<>();
    static public HashMap<Integer, Boolean> visited_branches = new HashMap<Integer, Boolean>();
    public static MyString[] inputs;
    public static HashSet<Integer> errors_reached = new HashSet<>(); // Errors reacehd

    /*********************** Iteration Variables ***********************/
    public static int max_branches_visited = 0;
    public static int iteration_number = 0;

    /*********************** Population Variables ***********************/
    private Population population = null;
    private int populationSize = 30;
    private int dnaIndex = 0;

    /*********************** Debug Variables ***********************/
    private static final Boolean DEBUG_NEW_BRANCH = true; // Enables printNewBranch

    /*********************** Logging Variables *********************/
    private static Logging log = null; 
    private static int count = 0;

    public static boolean DEPTH_FIRST_SEARCH = false;
    public static ArrayDeque<Integer> visit_order_queue = new ArrayDeque<>();
    public static int current_target_branch = -1;
    public static int attempt_for_target = 0;
    public static int MAX_ATTEMPT = 10000;

    public Fuzzer(String filename, String isDepth) {
        log = new Logging(filename);
        if (isDepth != null && isDepth.equals("true")){
            DEPTH_FIRST_SEARCH = true;
        }
       
    }

    // Returns the next branch to target. If there are no branches to target then returns -2.
    // Takes a boolean as parameter, which sets the type of priority: true -> depth-first | false -> breadth-first
    int getTargetBranch() {
        // Check if the previously returned branch was visited. If not, just return it
        if (current_target_branch != -1 && !visited_branches.get(current_target_branch)) {
            // We tried too much on this target without success. Put it back at the end of the queue.
            if (attempt_for_target > MAX_ATTEMPT) {
                visit_order_queue.addLast(current_target_branch);
            }
            else {
                attempt_for_target += 1;
                return current_target_branch;
            }
        }

        int node;
        // We visited every branch
        if (visit_order_queue.isEmpty())
            System.exit(25);
        do {
            node = visit_order_queue.removeFirst();
            List<Integer> children = rev_graph.get(node);
            if(children != null) { // Check that it actually has children, otherwise no need to insert them
                for (Integer child : children) {
                    if (DEPTH_FIRST_SEARCH)
                        visit_order_queue.addFirst(child);
                    else
                        visit_order_queue.addLast(child);
                }
            }
        } while (node == 0 || visited_branches.get(node));
        System.err.println("\nNext target branch: " + node);

        // Save the current target and set attempt_for_target to 1
        current_target_branch = node;
        attempt_for_target = 1;
        return node;
    }

    /**
     * Genetic algorithm Fuzz
     *
     * @param inputs: current Input in the form of MyString[]
     * @return the new input to be used as a MyInput Object
     */
    public MyInput fuzz(MyString[] inputs) {
        this.inputs = inputs;
        if (dnaIndex > 1)
            this.statistics(population.population[dnaIndex - 1].dna);

        if (this.population == null) {
            this.population = new Population(populationSize);
        }

        // The entire generation was used. So we need to get a new generation
        if (dnaIndex == populationSize) {
            // Get a branch to target
            int target_branch = getTargetBranch();

            population.calculateFitness(target_branch);
            population.nextGeneration();
            dnaIndex = 0;
        }

        // Use the next input in the population
        return population.population[dnaIndex++].dna;
    }



    /**
     * It calculates the distance between the execution path and the target branch
     * It's the distance in number of nodes in the graph
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
     * Updates counters and values for stadistics
     *
     * @param lastInput
     */
    private void statistics(MyInput lastInput) {
        iteration_number++; // Update global iteration counter
        int visited_stats = 0; // Counter to check the amount of visited branchs

        // Count the visited branchs
        for (Boolean visit : visited_branches.values()) {
            if (visit)
                visited_stats++;
        }

        // write to logfile. Only write in every 5th iteration to reduce the amount of data
        if (count++ % 5 == 0){
            log.writeLog(visited_stats);
        }
        

        // Check if we acchieved a new maximum of visited branches
        if (visited_stats > max_branches_visited) {
            max_branches_visited = visited_stats; // Update counter
            printNewBranch(lastInput); // Debug print
        }
    }

    /**
     * After an execution update the visited_branches with the data computed during the execution
     */
    public void after_execution(MyInput input) {
        for (int branch : input.visitedBranchs) {
            visited_branches.put(branch, true);
        }
    }


    /**
     * Print information when a new input triggers a new branch
     */
    public void printNewBranch(MyInput lastInput) {
        if (!DEBUG_NEW_BRANCH) return; // It is only printed if DEBUG_NEW_BRANCH is true
        System.err.println("\n************ FUZZER ************");
        System.err.println("Iteration: " + iteration_number + " visited " + max_branches_visited + " branches out of " + visited_branches.size());
        System.err.println("\tErrors reached: " + errors_reached.size());

        System.err.print("\tInput used: ");

        for (MyString s : lastInput.myStr) {
            System.err.print(s.val);
        }
        System.err.println();
    }
}


/** Used log the elapsed time and the branch coverage. */
class Logging {
    public long startTime;
    public long elapsedTime;
    public BufferedWriter out;
    public String outName;

    /**
     * Creates a new logger.
     * The name of the logfile depends on the current time.
     * @param outName The name of the logfile
     */
    public Logging(String outName) {
        startTime = System.nanoTime();
        elapsedTime = 0;
        this.outName = outName;
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
            out = new BufferedWriter(new FileWriter(this.outName + ".txt", true));
            out.write(String.valueOf(getElapsedTime()) + ", " + String.valueOf(numVisited) + "\n");
            out.close();
        } catch (IOException e) {
            System.out.println("Could not write to file.");
            e.printStackTrace();
        }
    }
}


