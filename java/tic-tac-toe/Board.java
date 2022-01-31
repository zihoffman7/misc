import java.util.Arrays;

public class Board {
  char board[][] = new char[3][3];

  public boolean move(char p, int move) {
    if (p == '-' || move > -1 && move < 9 && (board[move / board.length][move % board.length] == 0 || board[move / board.length][move % board.length] == '-')) {
      board[move / board.length][move % board.length] = p;
      return true;
    }
    return false;
  }

  public boolean computerMove(char t, char p) {
    boolean a;
    for (int i = 0; i < 9; i++) {
      a = move(t, i);
      if (a) {
        if (checkWin(t)) {
          return true;
        }
        move('-', i);
      }
      a = move(p, i);
      if (a) {
        if (checkWin(p)) {
          move('-', i);
          move(t, i);
          return false;
        }
        move('-', i);
      }
    }
    while (true) {
      a = move(t, (int) (Math.random() * 9));
      if (a) {
        return false;
      }
    }
  }

  public boolean checkWin(char p) {
    for (int i = 0; i < board.length; i++) {
      if (board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][2] == p || board[0][i] == board[1][i] && board[1][i] == board[2][i] && board[2][i] == p) {
        return true;
      }
    }
    if (board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[2][2] == p || board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[1][1] == p) {
      return true;
    }
    return false;
  }

  public void printB() {
    for (char[] i : board) {
      for (char j : i) {
        System.out.print(((j != 0) ? j : "-") + " ");
      }
      System.out.println();
    }
    System.out.println();
  }

  public void printMoves() {
    for (int i = 0; i < board.length; i++) {
      for (int j = 0; j < board[i].length; j++) {
        System.out.print((i*board[i].length + j) + " ");
      }
      System.out.println();
    }
  }
}
