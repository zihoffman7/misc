import java.util.Scanner;

public class Main {
  static Scanner s = new Scanner(System.in);
  static int inp;
  static boolean c;

  public static void main(String args[]) {
    computerGame();
  }

  public static void humanGame() {
    Board b = new Board();
    while (true) {
      do {
        b.printMoves();
        System.out.print("Number: ");
        inp = s.nextInt();
      } while (!b.move('x', inp));
      b.printB();
      if (b.checkWin('x')) {
        System.out.println("x wins!");
        break;
      }
      do {
        b.printMoves();
        System.out.print("Number: ");
        inp = s.nextInt();
      } while (!b.move('o', inp));
      b.printB();
      if (b.checkWin('o')) {
        System.out.println("o wins!");
        break;
      }
    }
  }

  public static void computerGame() {
    Board b = new Board();
    while (true) {
      do {
        b.printMoves();
        System.out.print("Number: ");
        inp = s.nextInt();
      } while (!b.move('x', inp));
      b.printB();
      if (b.checkWin('x')) {
        System.out.println("x wins!");
        break;
      }
      c = b.computerMove('o', 'x');
      if (c) {
        b.printB();
        System.out.println("o wins!");
        break;
      }
      b.printB();
    }
  }
}
