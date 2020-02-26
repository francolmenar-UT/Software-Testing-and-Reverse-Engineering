class Fuzzer {
    public static MyString[] fuzz(MyString[] inputs) {
        Random rand = new Random();
        int length = rand.nextInt(50) + 10;
        MyString[] result = new MyString[length];

        for(int i = 0; i < length; i++) {
            int index = rand.nextInt(inputs.length);
            result[i] = new MyString(inputs[index].val, true);
        }
        return result;
    }
}
