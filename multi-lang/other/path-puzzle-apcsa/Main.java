public class Main {
  public static long factorial(long x) {
    return (x < 2L) ? 1L : x * factorial(x - 1L);
  }

  public static long catalanNumber(long x) {
    return factorial(2L * x) / (factorial(x + 1L) * factorial(x));
  }

  public static long possibleAttempts(long x) {
    return (3L * x - 2L) * catalanNumber(x - 1L);
  }

  public static long possibleSolutions(long x) {
    return (x == 1L) ? 1L : possibleSolutions(x - 1) + possibleAttempts(x - 1);
  }

  public static void main(String[] args) {
    System.out.println((int) (Math.random() * 7));
    System.out.println(Long.MAX_VALUE);
  }
}
