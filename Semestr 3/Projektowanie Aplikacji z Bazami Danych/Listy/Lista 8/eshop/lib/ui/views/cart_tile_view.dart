import 'package:flutter/material.dart';

class CartListTile extends StatelessWidget {
  final String name;
  final int quantity;
  const CartListTile({super.key, required this.name, required this.quantity});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text('Produkt: $name Ilość: $quantity'),
      // trailing: Row(
      //   children: [
      //     IconButton(
      //       onPressed: () {},
      //       icon: const Icon(Icons.delete),
      //     ),
      //     IconButton(
      //       onPressed: () {},
      //       icon: const Icon(Icons.add),
      //     ),
      //   ],
      // ),
    );
  }
}
