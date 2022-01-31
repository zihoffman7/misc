public class Game {

  public static void botGame() {
    Board b = new Board();
    while (true) {
      b.display();
      b.playerMove('x');
      if (b.gameOverCheck()) {
        b.display();
        System.out.println("X WINS");
        break;
      }
      b.botMove('o', 'x');
      if (b.gameOverCheck()) {
        b.display();
        System.out.println("O WINS");
        break;
      }
    }
    System.out.println("GAME OVER");
  }
}
