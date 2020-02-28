class Fuzzer {
    public static MyInput fuzz(MyString[] inputs) {
        Random rand = new Random();
        int length = rand.nextInt(50) + 10;
        MyString[] fuzzStr = new MyString[length];
        for(int i = 0; i < length; i++) {
            int index = rand.nextInt(inputs.length);
            fuzzStr[i] = new MyString(inputs[index].val, true);
        }
        return new MyInput(fuzzStr);
    }
}
