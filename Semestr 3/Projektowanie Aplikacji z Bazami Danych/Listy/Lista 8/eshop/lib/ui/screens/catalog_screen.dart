import 'package:eshop/application/cart_application_service.dart';
import 'package:eshop/application/product_application_service.dart';
import 'package:eshop/ui/screens/cart_screen.dart';
import 'package:eshop/ui/views/product_card_view.dart';
import 'package:flutter/material.dart';

class CatalogScreen extends StatefulWidget {
  final ProductApplicationService productService;
  final CartApplicationService cartService;
  const CatalogScreen(
      {super.key, required this.productService, required this.cartService});

  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  final _textController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('e-Shop'),
        centerTitle: true,
        actions: [
          IconButton(
              onPressed: () {
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => CartScreen(
                    cartService: widget.cartService,
                  ),
                ));
              },
              icon: const Icon(Icons.shopping_cart))
        ],
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(10),
        gridDelegate:
            const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2),
        itemCount: widget.productService.getAllProducts().length,
        itemBuilder: (context, index) {
          final product = widget.productService.getAllProducts()[index];
          return ProductCard(product: product, onPressed: () {
            widget.cartService.addProductToCart(product);
          },);
        },
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          showDialog(
            context: context,
            builder: (context) {
              return AlertDialog(
                title: const Text('Add new prduct'),
                content: TextField(
                  controller: _textController,
                ),
                actions: [
                  TextButton(
                    onPressed: () {
                      widget.productService
                          .addNewProduct(_textController.text, null, null);
                      setState(() {});
                    },
                    child: const Text('Add product'),
                  ),
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('Cancel'),
                  ),
                ],
              );
            },
          );
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
