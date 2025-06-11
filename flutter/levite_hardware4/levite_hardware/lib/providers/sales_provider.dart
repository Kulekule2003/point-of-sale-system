import 'package:flutter/material.dart';
import '../models/sale.dart';
import '../database/database_helper.dart';

class SalesProvider with ChangeNotifier {
  final DatabaseHelper _dbHelper = DatabaseHelper();
  List<Sale> _sales = [];
  Map<String, dynamic> _analytics = {};
  List<Map<String, dynamic>> _monthlySales = [];

  List<Sale> get sales => _sales;
  Map<String, dynamic> get analytics => _analytics;
  List<Map<String, dynamic>> get monthlySales => _monthlySales;

  Future<void> loadSales() async {
    _sales = await _dbHelper.getSales();
    notifyListeners();
  }

  Future<void> loadAnalytics() async {
    _analytics = await _dbHelper.getSalesAnalytics();
    _monthlySales = await _dbHelper.getMonthlySalesData();
    notifyListeners();
  }

  Future<List<SaleItem>> getSaleItems(int saleId) async {
    return await _dbHelper.getSaleItems(saleId);
  }
}