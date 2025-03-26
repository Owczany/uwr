import 'package:eshop/application/cart_application_service.dart';
import 'package:eshop/application/product_application_service.dart';
import 'package:eshop/domain/models/cart.dart';
import 'package:eshop/infrastructure/repositories/product_repository.dart';
import 'package:eshop/ui/screens/catalog_screen.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'e-Shop',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: CatalogScreen(
        productService: ProductApplicationService(ProductRepository()),
        cartService: CartApplicationService(Cart()),
      ),
    );
  }
}
