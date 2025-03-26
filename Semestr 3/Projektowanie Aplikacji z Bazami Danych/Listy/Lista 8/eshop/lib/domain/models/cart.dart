import 'package:eshop/domain/models/product.dart';


class CartItem {
  final Product product;
  int quantity;

  CartItem({
    required this.product,
    this.quantity = 1,
  });
}

class Cart {
  final List<CartItem> items = [];

  void addProduct(Product product) {
    // sprawdzanie, czy juz prodkut znajduje sie w koszyku

    for (final cartItem in items) {
      if (cartItem.product.id == product.id) {
        cartItem.quantity++;
        return;
      }
    }
    items.add(CartItem(product: product));
  }

  void removeCartItem(Product product) {
    items.removeWhere((element) => element.product == product);
  }

}
