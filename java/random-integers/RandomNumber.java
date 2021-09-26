public class RandomNumber {
  public static int random(int x) {
    return (int) (Math.random() * (x + 1));
  }

  public static int random(int x, int y) {
    return ((int) (Math.random() * (Math.abs(x - y) + 1))) + Math.min(x, y);
  }

  public static void main(String[] args) {
    System.out.println(random(2, 4));
  }
}
