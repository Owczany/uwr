enum Color {
  RED,
  BLUE,
  GREEN
}

class Product {
  int id;
  String name;
  String? description;
  String? color;

  // konstruktor
  Product({
    required this.id,
    required this.name,
    this.description,
    this.color,
  });
}
