// screens/main_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/product_provider.dart';
import '../providers/sales_provider.dart';
import 'sales_screen.dart';
import 'inventory_screen.dart';
import 'analytics_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;
  
  // ignore: unused_field
  final List<String> _titles = [
    'Sales',
    'Inventory',
    'Analytics',
  ];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final productProvider = Provider.of<ProductProvider>(context, listen: false);
    final salesProvider = Provider.of<SalesProvider>(context, listen: false);
    
    await productProvider.loadProducts();
    await productProvider.loadCategories();
    await salesProvider.loadSales();
    await salesProvider.loadAnalytics();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        title: Row(
          children: [
            Icon(
              Icons.hardware,
              color: Colors.green[600],
              size: 28,
            ),
            const SizedBox(width: 12),
            Text(
              'Hardware Store POS',
              style: TextStyle(
                color: Colors.grey[800],
                fontSize: 20,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
        actions: [
          _buildNavButton('Sales', 0),
          _buildNavButton('Inventory', 1),
          _buildNavButton('Analytics', 2),
          const SizedBox(width: 20),
          CircleAvatar(
            backgroundColor: Colors.green[100],
            child: Icon(Icons.person, color: Colors.green[600]),
          ),
          const SizedBox(width: 20),
        ],
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: const [
          SalesScreen(),
          InventoryScreen(),
          AnalyticsScreen(),
        ],
      ),
    );
  }

  Widget _buildNavButton(String title, int index) {
    final isSelected = _selectedIndex == index;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4),
      child: TextButton(
        onPressed: () {
          setState(() {
            _selectedIndex = index;
          });
        },
        style: TextButton.styleFrom(
          backgroundColor: isSelected ? Colors.green[50] : Colors.transparent,
          foregroundColor: isSelected ? Colors.green[600] : Colors.grey[600],
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: Text(
          title,
          style: TextStyle(
            fontSize: 16,
            fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
          ),
        ),
      ),
    );
  }
}