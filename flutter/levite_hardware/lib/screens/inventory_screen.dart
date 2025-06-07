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
    _refresh();
  }

  void _refresh() async {
    final items = await DatabaseHelper.instance.getAllInventory();
    setState(() {
      _items = items;
    });
  }

  void _addItem() async {
    final name = _nameController.text.trim();
    final qty = int.tryParse(_qtyController.text) ?? 0;
    final price = double.tryParse(_priceController.text) ?? 0.0;
    final unitCost = double.tryParse(_unitCostController.text) ?? 0.0;
    if (name.isEmpty || qty <= 0 || price < 0 || unitCost < 0) return;
    await DatabaseHelper.instance.insertInventory(
      InventoryItem(name: name, quantity: qty, price: price, unitCost: unitCost),
    );
    _nameController.clear();
    _qtyController.clear();
    _priceController.clear();
    _unitCostController.clear();
    _refresh();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Inventory', style: Theme.of(context).textTheme.headlineSmall),
          SizedBox(height: 20),
          Row(
            children: [
              Expanded(child: TextField(controller: _nameController, decoration: InputDecoration(labelText: 'Name'))),
              SizedBox(width: 10),
              Expanded(child: TextField(controller: _qtyController, decoration: InputDecoration(labelText: 'Qty'), keyboardType: TextInputType.number)),
              SizedBox(width: 10),
              Expanded(child: TextField(controller: _priceController, decoration: InputDecoration(labelText: 'Price'), keyboardType: TextInputType.number)),
              SizedBox(width: 10),
              Expanded(child: TextField(controller: _unitCostController, decoration: InputDecoration(labelText: 'Unit Cost'), keyboardType: TextInputType.number)),
              SizedBox(width: 10),
              ElevatedButton(
                onPressed: _addItem,
                child: Text('Add'),
              ),
            ],
          ),
          SizedBox(height: 24),
          Expanded(
            child: ListView(
              children: _items.map((item) {
                return ListTile(
                  title: Text(item.name),
                  subtitle: Text('Qty: ${item.quantity}, Price: \$${item.price.toStringAsFixed(2)}, Unit: \$${item.unitCost.toStringAsFixed(2)}'),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
