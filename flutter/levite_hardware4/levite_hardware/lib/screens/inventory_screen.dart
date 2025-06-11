import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/product_provider.dart';
import '../models/product.dart';
import '../widgets/inventory_table.dart';

class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});

  @override
  State<InventoryScreen> createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  final _formKey = GlobalKey<FormState>();
  String? _itemName;
  String? _category;
  double? _price;
  int? _stockLevel;
  int? _reorderPoint;

  String? _searchName;
  int? _stockAdjustment;

  @override
  Widget build(BuildContext context) {
    final productProvider = Provider.of<ProductProvider>(context);
    final categories = productProvider.categories.map((c) => c.name).toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Inventory Management',
            style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'Add new items or update existing stock levels.',
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 32),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Add New Item
              Expanded(
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Add New Item', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 16),
                      TextFormField(
                        decoration: const InputDecoration(labelText: 'Item Name', hintText: 'e.g., Hammer'),
                        validator: (value) => value == null || value.isEmpty ? 'Enter item name' : null,
                        onSaved: (value) => _itemName = value,
                      ),
                      const SizedBox(height: 16),
                      DropdownButtonFormField<String>(
                        decoration: const InputDecoration(labelText: 'Category'),
                        items: categories.map((cat) => DropdownMenuItem(value: cat, child: Text(cat))).toList(),
                        onChanged: (value) => setState(() => _category = value),
                        validator: (value) => value == null ? 'Select category' : null,
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        decoration: const InputDecoration(labelText: 'Price', hintText: 'e.g., 19.99'),
                        keyboardType: TextInputType.number,
                        validator: (value) => value == null || double.tryParse(value) == null ? 'Enter valid price' : null,
                        onSaved: (value) => _price = double.tryParse(value!),
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        decoration: const InputDecoration(labelText: 'Stock Level', hintText: 'e.g., 50'),
                        keyboardType: TextInputType.number,
                        validator: (value) => value == null || int.tryParse(value) == null ? 'Enter valid stock' : null,
                        onSaved: (value) => _stockLevel = int.tryParse(value!),
                      ),
                      const SizedBox(height: 16),
                      TextFormField(
                        decoration: const InputDecoration(labelText: 'Reorder Point', hintText: 'e.g., 10'),
                        keyboardType: TextInputType.number,
                        validator: (value) => value == null || int.tryParse(value) == null ? 'Enter valid reorder point' : null,
                        onSaved: (value) => _reorderPoint = int.tryParse(value!),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: () async {
                          if (_formKey.currentState!.validate()) {
                            _formKey.currentState!.save();
                            final newProduct = Product(
                              name: _itemName!,
                              category: _category!,
                              price: _price!,
                              stockLevel: _stockLevel!,
                              reorderPoint: _reorderPoint!,
                            );
                            await productProvider.addProduct(newProduct);
                            _formKey.currentState!.reset();
                          }
                        },
                        child: const Text('Add Item'),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 40),
              // Update Stock
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Update Stock', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 16),
                    TextField(
                      decoration: const InputDecoration(labelText: 'Item Name', hintText: 'Search for item'),
                      onChanged: (value) => setState(() => _searchName = value),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      decoration: const InputDecoration(labelText: 'Stock Level Adjustment', hintText: 'Enter adjustment'),
                      keyboardType: TextInputType.number,
                      onChanged: (value) => _stockAdjustment = int.tryParse(value),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () async {
                        if (_searchName != null && _stockAdjustment != null) {
                          final product = productProvider.products.firstWhere(
                            (p) => p.name.toLowerCase() == _searchName!.toLowerCase(),
                            orElse: () => Product(
                              name: '', category: '', price: 0, stockLevel: 0, reorderPoint: 0,
                            ),
                          );
                          if (product.id != null) {
                            await productProvider.updateProductStock(product.id!, _stockAdjustment!);
                          }
                        }
                      },
                      child: const Text('Update Stock'),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 40),
          const InventoryTable(),
        ],
      ),
    );
  }
}
