import 'package:eshop/domain/models/product.dart';

abstract class AbsRepository {
  getAllProducts();
  getProductById(int id);
} 


class ProductRepository implements AbsRepository {
  final List<Product> _products = [
    Product(id: 1, name: 'Bike', color: 'Red'),
    Product(id: 2, name: 'Ball', description: 'Soccer ball'),
    Product(id: 3, name: 'Console'),
    Product(id: 4, name: 'Pończochy')
  ];

  List<Product> getAllProducts() {
    return _products;
  }

  Product? getProductById(int id) {
    for (Product product in _products) {
      if (product.id == id) {
        return product;
      }
    }
    return null;
  }

  void addNewProduct(String name, String? description, String? color) {
    int id = _products.last.id + 1;
    _products.add(Product(
      id: id,
      name: name,
      color: color,
      description: description,
    ));
  }

  void updateProduct(int id, String? description, String? color) {
    for (final product in _products) {
      if (product.id == id) {
        product.description = description;
        product.color = color;
      }
    }
  }

  void deleteProduct(int id) {
    _products.removeWhere((element) => element.id == id);
  }
}
