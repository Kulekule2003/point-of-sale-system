import 'package:flutter/material.dart';
import '../db/database_helper.dart';
import '../models/sale.dart';
import '../models/sale_item.dart';  // Critical import

class SalesHistoryScreen extends StatefulWidget {
  @override
  State<SalesHistoryScreen> createState() => _SalesHistoryScreenState();
}

class _SalesHistoryScreenState extends State<SalesHistoryScreen> {
  List<Sale> _sales = [];

  @override
  void initState() {
    super.initState();
    _refresh();
  }

  void _refresh() async {
    final sales = await DatabaseHelper.instance.getAllSales();
    setState(() => _sales = sales);
  }

  void _showReceipt(int saleId) async {
    final items = await DatabaseHelper.instance.getSaleItems(saleId);
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Receipt #$saleId'),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: items.map((item) => Text(
              '${item.itemName} x${item.quantity}: \$${item.amount.toStringAsFixed(2)}'
            )).toList(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Close'),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Sales History',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          SizedBox(height: 24),
          Expanded(
            child: ListView.builder(
              itemCount: _sales.length,
              itemBuilder: (context, index) => ListTile(
                title: Text('Receipt #${_sales[index].id}'),
                subtitle: Text(
                  'Date: ${_sales[index].saleDate} | '
                  'Total: \$${_sales[index].total.toStringAsFixed(2)}'
                ),
                trailing: TextButton(
                  child: Text('View Receipt'),
                  onPressed: () => _showReceipt(_sales[index].id!),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
