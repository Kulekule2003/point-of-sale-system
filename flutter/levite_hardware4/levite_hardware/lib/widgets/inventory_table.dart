import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/product_provider.dart';

class InventoryTable extends StatelessWidget {
  const InventoryTable({super.key});

  @override
  Widget build(BuildContext context) {
    final products = Provider.of<ProductProvider>(context).products;

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: DataTable(
        columns: const [
          DataColumn(label: Text('Product')),
          DataColumn(label: Text('Category')),
          DataColumn(label: Text('Stock Level')),
          DataColumn(label: Text('Reorder Point')),
        ],
        rows: products.map((p) {
          return DataRow(
            cells: [
              DataCell(Text(p.name)),
              DataCell(Text(p.category)),
              DataCell(Text('${p.stockLevel}')),
              DataCell(Text('${p.reorderPoint}')),
            ],
          );
        }).toList(),
      ),
    );
  }
}
