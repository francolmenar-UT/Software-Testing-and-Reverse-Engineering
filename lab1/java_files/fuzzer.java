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
class Fuzzer {
    public HashMap<Integer, Integer> graph = new HashMap<>(); // Graph created of the program
    public HashMap<Integer, List<Integer> > rev_graph = new HashMap<>();
    public HashMap<Integer, Boolean> if_branch = new HashMap<>();
    public HashMap<Integer, Boolean> visited_branches = new HashMap<Integer, Boolean>();
    public static int inputCreated = 0;
    public static int randomFuzz = 10;
    public static int mutationRate = 3;

    public static int max_branches_visited = 0;
    public static int max_trait = 0;
    public static int iteration_number = 0;

    public static boolean USE_TAINT = false;

    /*********************** Logging Variables *********************/
    private static Logging log = null; 
    private static int count = 0;

    // Errors
    public static HashSet<Integer> errors_reached = new HashSet<>();

    public List<MyInput> created_inputs = new ArrayList<MyInput>();

    public Fuzzer(String filename, String isDepth) {
        log = new Logging(filename);
        if (isDepth != null && isDepth.equals("true")){
            DEPTH_FIRST_SEARCH = true;
        }
    }

    public static boolean DEPTH_FIRST_SEARCH = true;
    public static ArrayDeque<Integer> visit_order_queue = new ArrayDeque<>();
    public static int current_target_branch = -1;
    public static int attempt_for_target = 0;
    public static int MAX_ATTEMPT = 10000;

    // Returns the next branch to target. If there are no branches to target then returns -2.
    // Takes a boolean as parameter, which sets the type of priority: true -> depth-first | false -> breadth-first
    int getTargetBranch() {
        // Check if the previously returned branch was visited. If not, just return it
        if (current_target_branch != -1 && !visited_branches.get(current_target_branch)) {
            // We tried too much on this target without success. Put it back at the end of the queue.
            if (attempt_for_target > MAX_ATTEMPT) {
                visit_order_queue.addLast(current_target_branch);
                // System.err.println("Max attempt: " + current_target_branch + " queue: " + visit_order_queue);
            }
            else {
                attempt_for_target += 1;
                return current_target_branch;
            }
        }

        int node;
        // We visited every branch
        if (visit_order_queue.isEmpty()){
            //System.exit(25);
            System.exit(0);
        }   
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
        } while (node == 0 || visited_branches.get(node) || !visit_order_queue.isEmpty() );
        System.err.println("\nNext target branch: " + node);

        // Save the current target and set attempt_for_target to 1
        current_target_branch = node;
        attempt_for_target = 1;
        return node;
    }


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

    // Normal Fuzz
    public MyInput fuzz(MyString[] inputs) {
        iteration_number++;
        // stats
        int visited_stats = 0;
        for (Boolean visit : visited_branches.values()) {
            if (visit)
                visited_stats++;
        }

        // write to logfile. Only write in every 2nd iteration to reduce the amount of data
        if (count++ % 2 == 0){
            log.writeLog(visited_stats);
        }

        if (visited_stats > max_branches_visited) {
            max_branches_visited = visited_stats;
            System.err.println("Iteration: " + iteration_number+ " visited " + visited_stats + " branches out of" + visited_branches.size());
            System.err.println("Errors reached:" + errors_reached.size());
            System.err.println("Traits with this input: " + created_inputs.get(created_inputs.size()-1).trait_count);
            System.err.println("Max traits: " + max_trait);

            for (MyString s : created_inputs.get(created_inputs.size()-1).myStr) {
                System.err.print(s.val);
            }
            System.err.println();
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

        }
        else { // use AF and branch distance
            int target_branch = getTargetBranch();

            int minAL = -1;
            float minDistance = -1;
            int branch_id = -1;

            // Find the best closest input to it
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
    public void after_execution (MyInput input, int trait_count) {
        input.trait_count = trait_count;
        for (int branch : input.visitedBranchs) {
            visited_branches.put(branch, true);
        }
        if (trait_count > max_trait)
            max_trait = input.trait_count;
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
