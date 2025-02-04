class I {
<insert_var>

    public static Random random = new Random(42);

    public static void myAdd(MyInt a, MyInt b, MyInt c) {
        a.val = b.val + c.val;
    }

    public static void myDel(MyInt a, MyInt b, MyInt c) {
        a.val = b.val - c.val;
    }

    public static void myMul(MyInt a, MyInt b, MyInt c) {
        a.val = b.val * c.val;
    }

    public static void myDiv(MyInt a, MyInt b, MyInt c) {
        a.val = b.val / c.val;
    }

    public static void myMod(MyInt a, MyInt b, MyInt c) {
        a.val = b.val % c.val;
    }

    /****************************               ****************************/
    public static void myInd(MyInt a, MyInt[] b, MyInt c) {
        a.val = b[c.val].val;
    }

    public static void myInd(MyString a, MyString[] b, MyInt c) {
        a.val = b[c.val].val;
    }

    /****************************               ****************************/
    public static void myEquals(MyBool a, MyBool b, MyBool c, MyInput input) {
        a.val = (b.val == c.val);
        float b_distance = branch_distance_eq(a.val);
        input.setBranchDistance(this_branch_id, b_distance); // Set Branch distance to the MyInput
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    public static void myEquals(MyBool a, MyInt b, MyInt c, MyInput input) {
        a.val = (b.val == c.val);
        float b_distance = branch_distance_eq(a.val);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean

    }

    public static void myEquals(MyBool a, MyString b, MyString c, MyInput input) {
        a.val = (b.val.equals(c.val));
        float b_distance = editDistDP(b.val, c.val, b.val.length(), c.val.length());
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    /****************************               ****************************/
    public static void myLess(MyBool a, MyInt b, MyInt c, MyInput input) {
        a.val = (b.val < c.val);
        float b_distance = branch_distance_less_eq(b.val, c.val, a.val);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    public static void myGreater(MyBool a, MyInt b, MyInt c, MyInput input) {
        a.val = (b.val > c.val);
        float b_distance = branch_distance_greater_eq(b.val, c.val, a.val);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    public static void myLessEqual(MyBool a, MyInt b, MyInt c, MyInput input) {
        a.val = (b.val <= c.val);
        float b_distance = branch_distance_less_eq(b.val, c.val, a.val);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    public static void myGreaterEqual(MyBool a, MyInt b, MyInt c, MyInput input) {
        a.val = (b.val >= c.val);
        float b_distance = branch_distance_greater_eq(b.val, c.val, a.val);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    /****************************               ****************************/
    public static MyBool myAssign(MyBool b) {
        MyBool a = new MyBool(b.val);
        return a;
    }

    public static MyInt myAssign(MyInt b) {
        MyInt a = new MyInt(b.val);
        return a;
    }

    public static MyInt[] myAssign(MyInt[] b) {
        MyInt a[] = new MyInt[b.length];
        for (int i = 0; i < b.length; i++) {
            a[i] = new MyInt(b[i].val);
        }
        return a;
    }

    public static MyString myAssign(MyString b) {
        MyString a = new MyString(b.val);
        return a;
    }

    /****************************               ****************************/
    public static void myAnd(MyBool a, MyBool b, MyBool c, MyInput input) {
        a.val = (b.val && c.val);
        float b_distance = branch_distance_and(b.branchDistance, c.branchDistance);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    public static void myOr(MyBool a, MyBool b, MyBool c, MyInput input) {
        a.val = (b.val || c.val);
        float b_distance = branch_distance_or(b.branchDistance, c.branchDistance);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    public static void myNot(MyBool a, MyBool b, MyInput input) {
        a.val = (!b.val);
        float b_distance = branch_distance_not(b.branchDistance);
        input.setBranchDistance(this_branch_id, b_distance);
        a.setBranchDistance(b_distance); // Set Branch distance to the resulting boolean
    }

    /****************************               ****************************/
    public static void myPrint(MyString a) {
        System.out.println("\n" + a.val);
    }

    public static void myPrint(String a) {
        myPrint(new MyString(a));
    }

    public static boolean myIf(MyBool a) {
        if (a.val)
            I.stack.push(a.flow || (stack.empty() ? false : stack.peek()));
        // System.out.print("b" + a.val + " ");
        return a.val;
    }

    /****************************               ****************************/
    public static void myAdd(MyInt a, MyInt b, int c) {
        myAdd(a, b, new MyInt(c));
    }

    public static void myAdd(MyInt a, int b, MyInt c) {
        myAdd(a, new MyInt(b), c);
    }

    public static void myAdd(MyInt a, int b, int c) {
        myAdd(a, new MyInt(b), new MyInt(c));
    }

    public static void myDel(MyInt a, MyInt b, int c) {
        myDel(a, b, new MyInt(c));
    }

    public static void myDel(MyInt a, int b, MyInt c) {
        myDel(a, new MyInt(b), c);
    }

    public static void myDel(MyInt a, int b, int c) {
        myDel(a, new MyInt(b), new MyInt(c));
    }

    public static void myMul(MyInt a, MyInt b, int c) {
        myMul(a, b, new MyInt(c));
    }

    public static void myMul(MyInt a, int b, MyInt c) {
        myMul(a, new MyInt(b), c);
    }

    public static void myMul(MyInt a, int b, int c) {
        myMul(a, new MyInt(b), new MyInt(c));
    }

    public static void myDiv(MyInt a, MyInt b, int c) {
        myDiv(a, b, new MyInt(c));
    }

    public static void myDiv(MyInt a, int b, MyInt c) {
        myDiv(a, new MyInt(b), c);
    }

    public static void myDiv(MyInt a, int b, int c) {
        myDiv(a, new MyInt(b), new MyInt(c));
    }

    public static void myMod(MyInt a, MyInt b, int c) {
        myMod(a, b, new MyInt(c));
    }

    public static void myMod(MyInt a, int b, MyInt c) {
        myMod(a, new MyInt(b), c);
    }

    public static void myMod(MyInt a, int b, int c) {
        myMod(a, new MyInt(b), new MyInt(c));
    }

    public static void myInd(MyInt a, MyInt[] b, int c) {
        myInd(a, b, new MyInt(c));
    }

    public static void myInd(MyInt a, int[] b, int c) {
        myInd(a, I.myAssign(b), new MyInt(c));
    }

    public static void myInd(MyString a, MyString[] b, int c) {
        myInd(a, b, new MyInt(c));
    }

    /****************************               ****************************/
    public static void myEquals(MyBool a, MyBool b, boolean c, MyInput input) {
        myEquals(a, b, new MyBool(c), input);
    }

    public static void myEquals(MyBool a, MyInt b, int c, MyInput input) {
        myEquals(a, b, new MyInt(c), input);
    }

    public static void myEquals(MyBool a, MyString b, String c, MyInput input) {
        myEquals(a, b, new MyString(c), input);
    }

    public static void myEquals(MyBool a, boolean b, MyBool c, MyInput input) {
        myEquals(a, new MyBool(b), c, input);
    }

    public static void myEquals(MyBool a, int b, MyInt c, MyInput input) {
        myEquals(a, new MyInt(b), c, input);
    }

    public static void myEquals(MyBool a, String b, MyString c, MyInput input) {
        myEquals(a, new MyString(b), c, input);
    }

    public static void myEquals(MyBool a, boolean b, boolean c, MyInput input) {
        myEquals(a, new MyBool(b), new MyBool(c), input);
    }

    public static void myEquals(MyBool a, int b, int c, MyInput input) {
        myEquals(a, new MyInt(b), new MyInt(c), input);
    }

    public static void myEquals(MyBool a, String b, String c, MyInput input) {
        myEquals(a, new MyString(b), new MyString(c), input);
    }

    /****************************               ****************************/
    public static void myLess(MyBool a, MyInt b, int c, MyInput input) {
        myLess(a, b, new MyInt(c), input);
    }

    public static void myGreater(MyBool a, MyInt b, int c, MyInput input) {
        myGreater(a, b, new MyInt(c), input);
    }

    public static void myLessEqual(MyBool a, MyInt b, int c, MyInput input) {
        myLessEqual(a, b, new MyInt(c), input);
    }

    public static void myGreaterEqual(MyBool a, MyInt b, int c, MyInput input) {
        myGreaterEqual(a, b, new MyInt(c), input);
    }

    public static void myLess(MyBool a, int b, MyInt c, MyInput input) {
        myLess(a, new MyInt(b), c, input);
    }

    public static void myGreater(MyBool a, int b, MyInt c, MyInput input) {
        myGreater(a, new MyInt(b), c, input);
    }

    public static void myLessEqual(MyBool a, int b, MyInt c, MyInput input) {
        myLessEqual(a, new MyInt(b), c, input);
    }

    public static void myGreaterEqual(MyBool a, int b, MyInt c, MyInput input) {
        myGreaterEqual(a, new MyInt(b), c, input);
    }

    public static void myLess(MyBool a, int b, int c, MyInput input) {
        myLess(a, new MyInt(b), new MyInt(c), input);
    }

    public static void myGreater(MyBool a, int b, int c, MyInput input) {
        myGreater(a, new MyInt(b), new MyInt(c), input);
    }

    public static void myLessEqual(MyBool a, int b, int c, MyInput input) {
        myLessEqual(a, new MyInt(b), new MyInt(c), input);
    } // .-

    public static void myGreaterEqual(MyBool a, int b, int c, MyInput input) {
        myGreaterEqual(a, new MyInt(b), new MyInt(c), input);
    }

    /****************************               ****************************/
    public static MyBool myAssign(boolean b) {
        return myAssign(new MyBool(b));
    }

    public static MyInt myAssign(int b) {
        return myAssign(new MyInt(b));
    }

    public static MyInt[] myAssign(int[] b) {
        MyInt a[] = new MyInt[b.length];
        for (int i = 0; i < b.length; i++) a[i] = new MyInt(b[i]);
        return myAssign(a);
    }

    public static MyString myAssign(String b) {
        return myAssign(new MyString(b));
    }

    /**
     * Normalize an Int
     *
     * @param distance: input Int to be normalized
     * @return float normalized value
     */
    public static float normalize_int(int distance) {
        return (float) distance / (distance + 1);
    }

    /**
     * Normalize a Float
     *
     * @param distance: input Float to be normalized
     * @return float normalized value
     */
    public static float normalize_float(float distance) {
        return (float) distance / (distance + 1);
    }

    /**
     * Branch distance for Equal comparison of Ints
     *
     * @param b: First parameter in the comparison
     * @param c: Second parameter in the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_eq(int b, int c) {
        return normalize_int(b - c);
    }

    /**
     * Branch distance for Equal comparison of Booleans
     *
     * @param equal: Result of the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_eq(boolean equal) {
        if (equal) {
            return (float) 0.0;
        }
        return (float) 1.0;
    }

    /**
     * Branch distance for Less or Equal comparison of Ints
     *
     * @param b: First parameter in the comparison
     * @param c: Second parameter in the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_less_eq(int b, int c, boolean less) {
        if (less) {
            return (float) 0.0;
        }
        return (float) normalize_int(b - c);
    }

    /**
     * Branch distance for Greater or Equal comparison of Ints
     *
     * @param b: First parameter in the comparison
     * @param c: Second parameter in the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_greater_eq(int b, int c, boolean greater) {
        if (greater) {
            return (float) 0.0;
        }
        return (float) normalize_int(b - c);
    }

    /**
     * Branch distance for And comparisons
     *
     * @param b: Branch distance of the first parameter in the comparison
     * @param c: Branch distance of the second parameter in the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_and(float b, float c) {
        if (b == -1.0) b = (float) 0.0;
        if (c == -1.0) c = (float) 0.0;
        return normalize_float(b + c);
    }

    /**
     * Branch distance for Or comparisons
     *
     * @param b: Branch distance of the first parameter in the comparison
     * @param c: Branch distance of the second parameter in the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_or(float b, float c) {
        if (b == -1.0) b = (float) 0.0;
        if (c == -1.0) c = (float) 0.0;
        return Math.min(b, c);
    }

    /**
     * Branch distance for Or comparisons
     *
     * @param b: Branch distance of the first parameter in the comparison
     * @return float representing the branch distance
     */
    public static float branch_distance_not(float b) {
        if (b == -1.0) b = (float) 0.0;
        return (float) 1.0 - b;
    }

    /**
     * //TODO Check if it works and if m and n are the lengths of the strings
     * <p>
     * Calculates the branch distance for two strings
     *
     * @param str1: First parameter in the comparison
     * @param str2: Second parameter in the comparison
     * @param m
     * @param n
     * @return float representing the branch distance
     */
    static float editDistDP(String str1, String str2, int m, int n) {
        int table[][] = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) {
            for (int j = 0; j <= n; j++) {
                // If first string is empty
                if (i == 0) table[i][j] = j;
                    // If second string is empty
                else if (j == 0) table[i][j] = i;
                    // If last characters are same
                else if (str1.charAt(i - 1) == str2.charAt(j - 1)) table[i][j] = table[i - 1][j - 1];
                    // If the last character is different
                else {
                    table[i][j] = 1 + Math.min(Math.min(table[i][j - 1], table[i - 1][j]), table[i - 1][j - 1]);
                }
            }
        }
        return normalize_int(table[m][n]);
    }

    public static int this_branch_id; // ID used for storing the branch distance in the Hash Map

    public static Stack<Boolean> stack = new Stack<>();
}
