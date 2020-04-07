/**
 * Fuzzer class
 */
class Fuzzer {
    /*********************** Graph Variables ***********************/
    static public HashMap<Integer, Integer> graph = new HashMap<>(); // Graph created of the program
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


    public void Fuzzer() {
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
            int target_branch = -1;
            for (Map.Entry<Integer, Boolean> entry : visited_branches.entrySet()) {
                Integer branch = entry.getKey();
                Boolean visited = entry.getValue();

                if (!visited) {
                    target_branch = branch;
                    break;
                }
            }

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


