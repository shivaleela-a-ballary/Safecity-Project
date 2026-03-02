public class PatternProgram {
    public static void main(String[] args) {
        System.out.println("Pattern 1:");
        pattern1();
        System.out.println("\nPattern 2:");
        pattern2();
        System.out.println("\nPattern 3:");
        pattern3();
    }

    // Pattern 1: Pyramid pattern
    public static void pattern1() {
        int rows = 3; // Number of rows for the pattern
        for (int i = 1; i <= rows; i++) {
            // Print leading spaces
            for (int j = rows; j > i; j--) {
                System.out.print(" ");
            }
            // Print stars with spaces
            for (int k = 1; k <= i; k++) {
                System.out.print("* ");
            }
            System.out.println(); // Move to the next line
        }
    }

    // Pattern 2: Descending and Ascending stars
    public static void pattern2() {
        int rows = 4; // Number of rows for the descending pattern
        // Print descending pattern
        for (int i = rows; i >= 1; i--) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
        // Print ascending pattern
        for (int i = 2; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("*");
            }
            System.out.println();
        }
    }

    // Pattern 3: Alphabet pattern
    public static void pattern3() {
        char lastChar = 'D'; // Last character in the pattern
        for (char i = 'A'; i <= lastChar; i++) {
            for (char j = 'A'; j <= i; j++) {
                System.out.print(j);
            }
            System.out.println();
        }
    }
}