import 'package:eshop/domain/models/product.dart';
import 'package:eshop/infrastructure/repositories/product_repository.dart';

class ProductApplicationService {
  final ProductRepository repository;

  ProductApplicationService(this.repository);

  List<Product> getAllProducts() {
    return repository.getAllProducts();
  }

  void addNewProduct(String name, String? description, String? color) {
    repository.addNewProduct(name, description, color);
  }

  void deleteProduct(int id) {
    repository.deleteProduct(id);
  }

  void updateProduct(int id, {String? description, String? color}) {
    repository.updateProduct(id, description, color);
  }
}
