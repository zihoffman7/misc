#include <iostream>
#include <cmath>
#include <map>

using namespace std;

class str {
public:
  string text = "";
  map<char, int> chars;
  str(string text) {
    this->text = text;
    for (int i = 0; i < text.length(); i++) {
      try {
        this->chars[tolower(text[i])] += 1;
      }
      catch(int i) {}
    }
  }
};

float sigmoid(float x) {
  return(1 / (1 + exp(-x)));
}

float compare(str *a, str *b) {
  int c1 = 0;
  int c2 = 0;
  int sum = 0;
  for (map<char, int>::iterator iter = a->chars.begin(); iter != a->chars.end(); iter++) {
    try {
      c1 += b->chars[iter->first] + iter->second;
      c2 += 1;
      sum += 2 * iter->second;
    }
    catch(map<char, int>::iterator iter) {
      c1 += 0.5;
      c2 += 1;
    }
  }
  float evaluate = sigmoid(sum / c2 - c1 / c2);
  if (evaluate == 0.5 && a->text != b->text) {
    for (int i = 0; i < a->text.length(); i++) {
      c2 += 1;
      if (a->text[i] == b->text[i]) {
        c1 += 2;
      }
    }
    evaluate = abs((float)(c1 / c2 / a->text.length()));
  }
  return(evaluate);
}

class similarity {
public:
  float r = 0;
  similarity(str a, str b) {
    r = ((1 - abs(0.5 - compare(&a, &b)) * 2) + (1 - abs(0.5 - compare(&b, &a)) * 2)) / 2;
  }
  float eval() {
    return(r);
  }
};

int main() {
  while (true) {
    string d;
    string f;
    getline(cin, d);
    getline(cin, f);
    str a(d);
    str b(f);
    similarity x(a, b);
    cout << x.eval() << endl;
  }
}
