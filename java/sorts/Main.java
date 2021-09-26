import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;

public class Main {
  static Random gen;

  public static void main(String[] args) {
    gen = new Random();
    System.out.println(quickSort(new ArrayList<Float>(Arrays.asList(gen.nextFloat(), gen.nextFloat(), gen.nextFloat(), gen.nextFloat(), gen.nextFloat(), gen.nextFloat(), gen.nextFloat(), gen.nextFloat()))));
    System.out.println(quickSort(new ArrayList<String>(Arrays.asList(nextString(), nextString(), nextString(), nextString(), nextString(), nextString(), nextString(), nextString(), nextString(), nextString(), nextString()))));
  }

  public static String nextString() {
    return Character.toString((char) 33 + gen.nextInt(92));
  }

  public static <T extends Comparable<T>> List<T> quickSort(List<T> arr) {
    if (arr.size() < 2) {
      return arr;
    }

    if (arr.size() == 2) {
      List<T> temp = mergeSort(arr);
      arr.set(0, temp.get(0));
      arr.set(1, temp.get(1));
    }

    else {
      T cutoff = mergeSort(new ArrayList<T>(Arrays.asList(arr.get(0), arr.get(1), arr.get(2)))).get(1);
      int i = 0;
      int j = arr.size() - 1;

      while (i < j) {
        while (arr.get(i).compareTo(cutoff) <= 0 && i < arr.size() - 1) {
          i++;
        }
        while (arr.get(j).compareTo(cutoff) >= 0 && j > 0) {
          j--;
        }

        if (i < j) {
          T p = arr.get(i);
          arr.set(i, arr.get(j));
          arr.set(j, p);
        }
      }

      quickSort(arr.subList(0, i));
      quickSort(arr.subList(i, arr.size()));
    }

    return arr;
  }

  public static <T extends Comparable<T>> List<T> mergeSort(List<T> arr) {
    if (arr.size() < 2) {
      return arr;
    }

    List<T> sorted = new LinkedList<T>();
    
    List<T> arr1 = mergeSort(new LinkedList<T>(arr.subList(0, (arr.size()) / 2)));
    List<T> arr2 = mergeSort(new LinkedList<T>(arr.subList((arr.size()) / 2, arr.size())));

    do {
      if (arr1.size() < 1) {
        sorted.add(arr2.remove(0));
        continue;
      }
      if (arr2.size() < 1) {
        sorted.add(arr1.remove(0));
        continue;
      }
      sorted.add((arr1.get(0).compareTo(arr2.get(0)) < 0 ? arr1 : arr2).remove(0));
    } while (arr1.size() > 0 || arr2.size() > 0);

    return sorted;
  }
}
