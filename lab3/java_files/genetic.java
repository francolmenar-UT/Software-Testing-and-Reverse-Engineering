/**
 * Population
 */
class Population {
    int size;
    Dna[] population;
    Double[] fitness;

    private Double totalFitness;

    public Population (int size) {
        this.size = size;
        this.population = new Dna[size];
        for (int i = 0; i < size; i++) {
            population[i] = new Dna();
        }

        this.fitness = new Double[size];
    }

    public void nextGeneration() {
        Dna[] nextGeneration = new Dna[size];

        for (int i = 0; i < size; i++) {
            Dna parent1 = this.getParent();
            Dna parent2 = this.getParent();

            nextGeneration[i] = parent1.crossover(parent2);
            nextGeneration[i].mutate();
        }

        population = nextGeneration;
    }

    public void calculateFitness(int branchId) {
        this.totalFitness = (Double) 0.0;

        for (int i = 0; i < this.size; i++) {
            this.fitness[i] = this.population[i].calculateFitness(branchId);

            this.totalFitness += this.fitness[i];
        }
    }

    private Dna getParent() {
        Random rand = new Random();
        Double fit = rand.nextDouble() * this.totalFitness;

        int index = 0;
        while (index < this.size - 1 && fit >= this.fitness[index]) {
            fit -= fitness[index];
            index++;
        }

        return population[index];
    }
}

/**
 * DNA
 */
class Dna {
    MyInput dna;
    int length = 10;
    double delta = 0.1; // Used to avoid division by 0
    double mutation_factor = 0.01;

    public Dna() {
        this.dna = this.randomDna();
    }

    public Dna(int length) {
        this.length = length;

        this.dna = this.randomDna();
    }

    public Dna(MyInput dna) {
        this.dna = dna;
        this.length = dna.myStr.length;
    }

    MyInput randomDna() {
        Random rand = new Random();
        MyString[] myString = new MyString[this.length];

        for (int i = 0; i < this.length; i++) {
            int index = rand.nextInt(Fuzzer.inputs.length);
            myString[i] = new MyString(Fuzzer.inputs[index].val, true);
        }
        return new MyInput(myString);
    }

    public Double calculateFitness(int targetBranch) {
        Pair<Integer, Integer> al = Fuzzer.approachLevel(targetBranch, dna);

        if (al.first < 0) {// there was an error
            return 0.0;
        }
        int approachLevel = al.first;
        int branchId = al.second;

        double distance = (double) this.dna.branch_distance.get(branchId);

        // Since approachLevel is more important and distance <= 1, we compute totalDistance as following.
        // This allow to order it by al first and then by distance
        double totalDistance = (double) (approachLevel * 10) + distance;

        // We need fitness as greater = better for the getParent function.
        // So we can simply compute the inverse of the total distance. delta is used to avoid division by 0
        double fitness = 1 / (totalDistance + this.delta);
        
        return fitness;
    }

    /*
     * Generate a new Dna which is the crossover between this dna and the partner
     */
    public Dna crossover(Dna partner) {
        Random rand = new Random();
        int splitPosition = rand.nextInt(this.length);

        // The final len is the segment from this [0..splitPosition] + what is added from partner
        // [splitPosition..partner.length] If partner.length < splitPosition then nothing is added and the final len =
        // the segment from this, which is splitPosition +1 because splitPosition starts from 0
        int child_len = splitPosition >= partner.length - 1 ? splitPosition + 1 : partner.length;

        MyString[] gene = new MyString[child_len];

        assert(this.length == this.dna.myStr.length) : "this.len";
        assert(partner.length == partner.dna.myStr.length) : "partner.len";
        for (int i = 0; i < child_len; i++) {
            if (i <= splitPosition)
                gene[i] = new MyString(this.dna.myStr[i].val, true);
            else
                gene[i] = new MyString(partner.dna.myStr[i].val, true);
        }
        return new Dna(new MyInput(gene));
    }

    public void mutate() {
        Random rand = new Random();

        for (int i = 0; i < this.length; i++) {
            if (rand.nextDouble() < Fuzzer.mutation_factor) {
                /* Decide which mutation to apply:
                 * 0 -> modify char
                 * 1 -> remove char
                 * 2 -> add char after this
                 */
                int operation = rand.nextInt(3);

                if (operation == 0) { //change
                    int index = rand.nextInt(Fuzzer.inputs.length);
                    this.dna.myStr[i] = new MyString(Fuzzer.inputs[index].val, true);
                } else if (operation == 1 && this.length > 1) { //remove
                    int p = this.dna.myStr.length;
                    this.dna.myStr = ArrayUtils.remove(this.dna.myStr, i);
                    assert(p != this.dna.myStr.length) : "java sucks";
                    this.length--;
                } else { // add
                    int index = rand.nextInt(Fuzzer.inputs.length);
                    int p = this.dna.myStr.length;
                    this.dna.myStr = ArrayUtils.insert(i+1, this.dna.myStr, new MyString(Fuzzer.inputs[index].val, true));
                    assert(p != this.dna.myStr.length) : "java sucks 2";
                    this.length++;
                    i++; // skip the next element cause it was just added
                }

            }
        }
        assert(this.length == this.dna.myStr.length) : "wrong mutate";
    }
}
