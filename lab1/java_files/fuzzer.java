class Pair<A, B> {
    public A first;
    public B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }
}

class Fuzzer {
    public HashMap<Integer, Integer> graph = new HashMap<>();
    public HashMap<Integer, Boolean> if_branch = new HashMap<>();
    public HashMap<Integer, Boolean> visited_branches = new HashMap<Integer, Boolean>();
    public static int inputCreated = 0;
    public static int randomFuzz = 10;
    public static int mutationRate = 3;

    public static int max_branches_visited = 0;
    public static int iteration_number = 0;

    public List<MyInput> created_inputs = new ArrayList<MyInput>();

    public void Fuzzer() { }

    public static MyInput random_fuzz(MyString[] inputs) {
        Random rand = new Random();
        int length = rand.nextInt(iteration_number) + 10;
        MyString[] fuzzStr = new MyString[length];
        for(int i = 0; i < length; i++) {
            int index = rand.nextInt(inputs.length);
            fuzzStr[i] = new MyString(inputs[index].val, true);
        }
        return new MyInput(fuzzStr);
    }

    public Pair<Integer, Integer> approachLevel(int goal, MyInput input) {
        int distance = -1;
        int node = goal;

        String trace = new String("");

        while (!(input.visitedBranchs.contains(node) && this.if_branch.get(node)) || node ==0) {
            distance++;
            node = this.graph.get(node);

            if (node == 0)
                return new Pair(-2, -1);
        }

        return new Pair(distance, node);
    }

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
            System.err.println("Iteration: " + iteration_number+ " visited " + visited_stats + " branches out of" + visited_branches.size());
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

        int target_branch = -1;

        int minAL = -1;
        float minDistance = -1;
        int branch_id = -1;
        MyInput best_input = created_inputs.get(0);

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
                    if (res.first <0) continue; //there was an error

                    if(minAL == -1 || res.first < minAL) {
                        minAL = res.first;
                        branch_id = res.second;
                        minDistance = input.branch_distance.get(branch_id);
                        best_input = input;
                    }
                    else if (res.first == minAL) {
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



        // Mutate it
        MyString[] fuzzStr = new MyString[best_input.myStr.length];
        System.arraycopy(best_input.myStr, 0, fuzzStr, 0, best_input.myStr.length);

        Random rand = new Random();
        for(int i = 0; i < fuzzStr.length; i++) {
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
    public void after_execution (MyInput input) {
        for (int branch : input.visitedBranchs) {
            visited_branches.put(branch, true);
        }
    }

}
