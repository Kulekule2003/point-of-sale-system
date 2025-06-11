import 'package:flutter/material.dart';
import '../models/product.dart';
import '../models/category.dart';
import '../database/database_helper.dart';

class ProductProvider with ChangeNotifier {
  final DatabaseHelper _dbHelper = DatabaseHelper();
  List<Product> _products = [];
  List<Category> _categories = [];
  String _selectedCategory = 'All';

  List<Product> get products => _selectedCategory == 'All' 
      ? _products 
      : _products.where((p) => p.category == _selectedCategory).toList();
  
  List<Category> get categories => _categories;
  String get selectedCategory => _selectedCategory;

  Future<void> loadProducts() async {
    _products = await _dbHelper.getProducts();
    notifyListeners();
  }

  Future<void> loadCategories() async {
    _categories = await _dbHelper.getCategories();
    notifyListeners();
  }

  void selectCategory(String category) {
    _selectedCategory = category;
    notifyListeners();
  }

  Future<void> addProduct(Product product) async {
    await _dbHelper.insertProduct(product);
    await loadProducts();
  }

  Future<void> updateProduct(Product product) async {
    await _dbHelper.updateProduct(product);
    await loadProducts();
  }

  Future<void> updateProductStock(int productId, int adjustment) async {
    final product = _products.firstWhere((p) => p.id == productId);
    final newStock = product.stockLevel + adjustment;
    await _dbHelper.updateProductStock(productId, newStock);
    await loadProducts();
  }
}