import 'package:flutter/material.dart';
import '../db/database_helper.dart';
import '../models/inventory_item.dart';

class InventoryScreen extends StatefulWidget {
  @override
  State<InventoryScreen> createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  final _nameController = TextEditingController();
  final _qtyController = TextEditingController();
  final _priceController = TextEditingController();
  final _unitCostController = TextEditingController();

  List<InventoryItem> _items = [];

  @override
  void initState() {
    super.initState();
    _refreshItems();
  }

  void _refreshItems() async {
    final items = await DatabaseHelper.instance.getAllInventory();
    setState(() => _items = items);
  }

  void _addItem() async {
    if (_nameController.text.isEmpty ||
        _qtyController.text.isEmpty ||
        _priceController.text.isEmpty ||
        _unitCostController.text.isEmpty) return;

    final newItem = InventoryItem(
      name: _nameController.text,
      quantity: int.tryParse(_qtyController.text) ?? 0,
      price: double.tryParse(_priceController.text) ?? 0,
      unitCost: double.tryParse(_unitCostController.text) ?? 0,
    );

    await DatabaseHelper.instance.insertInventory(newItem);
    _clearForm();
    _refreshItems();
  }

  void _clearForm() {
    _nameController.clear();
    _qtyController.clear();
    _priceController.clear();
    _unitCostController.clear();
  }

  double get _totalValue {
    return _items.fold(0, (sum, item) => sum + (item.quantity * item.price));
  }

  @override
  Widget build(BuildContext context) {
    final darkBackground = Color(0xFF181A20);
    final cardColor = Color(0xFF23262F);
    final borderColor = Color(0xFF353945);

    return Scaffold(
      backgroundColor: darkBackground,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header
            Container(
              padding: EdgeInsets.symmetric(vertical: 24),
              decoration: BoxDecoration(
                color: cardColor,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  Icon(Icons.inventory_2, size: 32, color: Colors.white),
                  SizedBox(width: 12),
                  Text(
                    "Inventory Management System",
                    style: TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 32),

            // Add New Item Section
            Container(
              decoration: BoxDecoration(
                color: cardColor,
                borderRadius: BorderRadius.circular(12),
              ),
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Text(
                    "+ Add New Item",
                    style: TextStyle(
                      color: Colors.blue[300],
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                  SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: _inputField(
                          label: "Item Name",
                          controller: _nameController,
                        ),
                      ),
                      SizedBox(width: 16),
                      Expanded(
                        child: _inputField(
                          label: "Quantity",
                          controller: _qtyController,
                          keyboardType: TextInputType.number,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: _inputField(
                          label: "Total Price (\$)",
                          controller: _priceController,
                          keyboardType: TextInputType.number,
                        ),
                      ),
                      SizedBox(width: 16),
                      Expanded(
                        child: _inputField(
                          label: "Unit Cost (\$)",
                          controller: _unitCostController,
                          keyboardType: TextInputType.number,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green,
                            minimumSize: Size(double.infinity, 48),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          icon: Icon(Icons.add),
                          label: Text("Add Item"),
                          onPressed: _addItem,
                        ),
                      ),
                      SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.grey[600],
                            minimumSize: Size(double.infinity, 48),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                          icon: Icon(Icons.clear),
                          label: Text("Clear Form"),
                          onPressed: _clearForm,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            SizedBox(height: 24),

            // Search Inventory
            Container(
              decoration: BoxDecoration(
                color: cardColor,
                borderRadius: BorderRadius.circular(12),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: TextField(
                style: TextStyle(color: Colors.purple[200]),
                decoration: InputDecoration(
                  prefixIcon: Icon(Icons.search, color: Colors.purple[200]),
                  hintText: "Search Inventory",
                  hintStyle: TextStyle(color: Colors.purple[200]),
                  border: InputBorder.none,
                ),
              ),
            ),
            SizedBox(height: 24),

            // Current Inventory
            Text(
              "Current Inventory",
              style: TextStyle(
                color: Colors.orange[400],
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 8),
            Container(
              decoration: BoxDecoration(
                color: cardColor,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: borderColor),
              ),
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // ASCII-style Table
                  Text(
                    _asciiTable(_items, _totalValue),
                    style: TextStyle(
                      fontFamily: 'Consolas',
                      color: Colors.white,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _inputField({
    required String label,
    required TextEditingController controller,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: TextStyle(color: Colors.white70)),
        SizedBox(height: 6),
        TextField(
          controller: controller,
          keyboardType: keyboardType,
          style: TextStyle(color: Colors.white),
          decoration: InputDecoration(
            filled: true,
            fillColor: Color(0xFF181A20),
            hintText: label.contains('Price') || label.contains('Cost') ? "0.00" : "Enter ${label.toLowerCase()}",
            hintStyle: TextStyle(color: Colors.white38),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: Colors.blueGrey),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: Colors.blueGrey),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: Colors.blueAccent),
            ),
          ),
        ),
      ],
    );
  }

  String _asciiTable(List<InventoryItem> items, double totalValue) {
    final buffer = StringBuffer();
    buffer.writeln("=====================================================");
    buffer.writeln("ITEM NAME      QTY   PRICE        UNIT COST   TOTAL");
    buffer.writeln("=====================================================");
    for (var item in items) {
      buffer.writeln(
          "${item.name.padRight(14)}"
          "${item.quantity.toString().padRight(6)}"
          "\$${item.price.toStringAsFixed(2).padRight(12)}"
          "\$${item.unitCost.toStringAsFixed(2).padRight(12)}"
          "\$${(item.quantity * item.price).toStringAsFixed(2)}"
      );
    }
    buffer.writeln("=====================================================");
    buffer.writeln("SUMMARY: ${items.length} items found | Total Value: \$${totalValue.toStringAsFixed(2)}");
    buffer.writeln("=====================================================");
    return buffer.toString();
  }
}
