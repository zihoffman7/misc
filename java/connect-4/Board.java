import java.util.Scanner;

public class Board {
  char[][] board;
  Scanner s = new Scanner(System.in);

  public Board() {
    board = new char[6][7];
    for (int i = 0; i < board.length; i++) {
      for (int j = 0; j < board[i].length; j++) {
        board[i][j] = ' ';
      }
    }
  }

  public boolean drop(int column, char token) {
    int o = -1;
    for (int i = 0; i < board.length; i++) {
      if (board[i][column] == ' ') {
        o = i;
      }
    }
    if (o >= 0) {
      board[o][column] = token;
      return true;
    }
    return false;
  }

  public void undrop(int column) {
    int o = -1;
    for (int i = 0; i < board.length; i++) {
      if (board[i][column] != ' ') {
        o = i;
        break;
      }
    }
    if (o >= 0) {
      board[o][column] = ' ';
    }
  }

  public void playerMove(char token) {
    System.out.print(token + ", it is your turn\n> ");
    int move = s.nextInt();
    if (move >= 1 && move <= board[0].length) {
      if (drop(move - 1, token)) {
        return;
      }
    }
    System.out.println("Enter an open slot");
    playerMove(token);
  }

  public void display() {
    System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n  1   2   3   4   5   6   7\n-----------------------------");
    for (char[] row : board) {
      System.out.println("| " + row[0] + " | " + row[1] + " | " + row[2] + " | " + row[3] + " | " + row[4] + " | " + row[5] + " | " + row[6] + " |\n-----------------------------");
    }
  }

  public boolean gameOverCheck() {
    for (char[] r : board) {
      for (int i = 0; i < 4; i++) {
        if (r[i] == r[i+1] && r[i+2] == r[i+3] && r[i] == r[i+2] && r[i] != ' ') {
          return true;
        }
      }
    }
    for (int r = 0; r < 3; r++) {
      for (int c = 0; c < board.length; c++) {
        if (board[r][c] == board[r+1][c] && board[r+2][c] == board[r+3][c] && board[r][c] == board[r+2][c] && board[r][c] != ' ') {
          return true;
        }
      }
    }
    for (int r = 0; r < 3; r++) {
      for (int c = 0; c < 4; c++) {
        if (board[r][c] == board[r+1][c+1] && board[r+2][c+2] == board[r+3][c+3] && board[r][c] == board[r+2][c+2] && board[r][c] != ' ') {
          return true;
        }
        if (board[r][c+3] == board[r+1][c+2] && board[r+2][c+1] == board[r+3][c] && board[r][c+3] == board[r+2][c+1] && board[r][c+3] != ' ') {
          return true;
        }
      }
    }
    return false;
  }

  public int winnable(char token) {
    for (int c = 0; c < board[0].length; c++) {
      if (drop(c, token) && gameOverCheck()) {
        undrop(c);
        return c + 1;
      }
      undrop(c);
    }
    return -1;
  }

  public void botMove(char computerToken, char playerToken) {
    int w = winnable(computerToken);
    if (w == -1) {
      w = winnable(playerToken);
      if (w == -1) {
        w = (int)(Math.random() * 7) + 1;
      }
    }
    if (!drop(w-1, computerToken)) {
      botMove(computerToken, playerToken);
    }
  }
}
