template <typename T> struct Rectangle {
  T perimeter() const { return 2 * (b + h); }

  T area() const { return b * h; }
};
