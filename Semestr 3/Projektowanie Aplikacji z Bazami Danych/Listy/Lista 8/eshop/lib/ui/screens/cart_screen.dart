import 'package:eshop/application/cart_application_service.dart';
import 'package:eshop/ui/views/cart_tile_view.dart';
import 'package:flutter/material.dart';

class CartScreen extends StatefulWidget {
  final CartApplicationService cartService;
  const CartScreen({super.key, required this.cartService});

  @override
  State<CartScreen> createState() => _CartScreenState();
}

class _CartScreenState extends State<CartScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Twój koszyk'),
        centerTitle: true,
      ),
      body: ListView.builder(
        itemCount: widget.cartService.getCartItems().length,
        itemBuilder: (context, index) {
          final item = widget.cartService.getCartItems()[index];
          return CartListTile(name: item.product.name, quantity: item.quantity);
        },
      ),
    );
  }
}
