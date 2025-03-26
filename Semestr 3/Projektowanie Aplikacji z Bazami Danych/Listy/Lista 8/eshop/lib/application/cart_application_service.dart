import 'package:eshop/domain/models/cart.dart';
import 'package:eshop/domain/models/product.dart';

class CartApplicationService {
  final Cart cart;

  CartApplicationService(this.cart);

  void addProductToCart(Product product) {
    cart.addProduct(product);
  }

  List<CartItem> getCartItems() {
    return cart.items;
  }

  void deleteProductFromCart() {
    
  }
}
