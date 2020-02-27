class Fuzzer {
    public static MyInput[] fuzz(MyString[] inputs) {
        Random rand = new Random();
        int length = rand.nextInt(50) + 10;
        MyInput [] resultFuzz = new MyInput[length];
        for(int i = 0; i < length; i++) {
            int index = rand.nextInt(inputs.length);
            resultFuzz[i] = new MyInput();
            resultFuzz[i].myStr = new MyString(inputs[index].val, true);
        }
        return resultFuzz;
    }
}
