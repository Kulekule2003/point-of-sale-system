import 'package:flutter/material.dart';
import '../models/cart_item.dart';
import '../models/product.dart';
import '../models/sale.dart';
import '../database/database_helper.dart';

class CartProvider with ChangeNotifier {
  final DatabaseHelper _dbHelper = DatabaseHelper();
  final List<CartItem> _items = [];

  List<CartItem> get items => _items;
  
  double get total => _items.fold(0.0, (sum, item) => sum + item.total);
  
  int get itemCount => _items.fold(0, (sum, item) => sum + item.quantity);

  void addItem(Product product) {
    final existingIndex = _items.indexWhere((item) => item.product.id == product.id);
    
    if (existingIndex >= 0) {
      if (_items[existingIndex].quantity < product.stockLevel) {
        _items[existingIndex].quantity++;
      }
    } else {
      if (product.stockLevel > 0) {
        _items.add(CartItem(product: product));
      }
    }
    notifyListeners();
  }

  void removeItem(Product product) {
    final existingIndex = _items.indexWhere((item) => item.product.id == product.id);
    
    if (existingIndex >= 0) {
      if (_items[existingIndex].quantity > 1) {
        _items[existingIndex].quantity--;
      } else {
        _items.removeAt(existingIndex);
      }
    }
    notifyListeners();
  }

  void updateQuantity(Product product, int quantity) {
    final existingIndex = _items.indexWhere((item) => item.product.id == product.id);
    
    if (existingIndex >= 0) {
      if (quantity <= 0) {
        _items.removeAt(existingIndex);
      } else if (quantity <= product.stockLevel) {
        _items[existingIndex].quantity = quantity;
      }
    }
    notifyListeners();
  }

  Future<void> completePurchase() async {
    if (_items.isEmpty) return;

    final saleItems = _items.map((cartItem) => SaleItem(
      saleId: 0, // Will be set by database
      productId: cartItem.product.id!,
      productName: cartItem.product.name,
      quantity: cartItem.quantity,
      price: cartItem.product.price,
    )).toList();

    final sale = Sale(
      date: DateTime.now(),
      total: total,
      items: saleItems,
    );

    await _dbHelper.insertSale(sale);
    _items.clear();
    notifyListeners();
  }

  void clearCart() {
    _items.clear();
    notifyListeners();
  }
}