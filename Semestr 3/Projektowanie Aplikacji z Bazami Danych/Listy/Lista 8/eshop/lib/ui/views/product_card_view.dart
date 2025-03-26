import 'package:eshop/domain/models/product.dart';
import 'package:flutter/material.dart';

class ProductCard extends StatelessWidget {
  final Product product;
  final void Function() onPressed;
  const ProductCard(
      {super.key, required this.product, required this.onPressed});

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1.0,
      child: Card(
        child: Column(
          children: [
            Expanded(
              flex: 5,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(product.name),
                  product.description != null
                      ? Text('Opis: ${product.description}')
                      : const SizedBox(),
                  product.color != null
                      ? Text('Kolor: ${product.color}')
                      : const SizedBox(),
                ],
              ),
            ),
            Expanded(
              child: Align(
                  alignment: Alignment.bottomRight,
                  child: IconButton(
                      onPressed: onPressed,
                      icon: const Icon(Icons.add_shopping_cart))),
            ),
          ],
        ),
      ),
    );
  }
}
