import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'dart:io';

import 'providers/product_provider.dart';
import 'providers/cart_provider.dart';
import 'providers/sales_provider.dart';
import 'screens/main_screen.dart';

void main() {
  // Initialize FFI for desktop
  if (Platform.isWindows || Platform.isMacOS || Platform.isLinux) {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ProductProvider()),
        ChangeNotifierProvider(create: (_) => CartProvider()),
        ChangeNotifierProvider(create: (_) => SalesProvider()),
      ],
      child: MaterialApp(
        title: 'Hardware Store POS',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.green,
          visualDensity: VisualDensity.adaptivePlatformDensity,
          fontFamily: 'Roboto',
        ),
        home: const MainScreen(),
      ),
    );
  }
}
