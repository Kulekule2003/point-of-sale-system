import 'package:flutter/material.dart';
import '../db/database_helper.dart';
import '../models/sale.dart';

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
    setState(() {
      _sales = sales;
    });
  }

  void _showReceipt(int saleId) async {
    final items = await DatabaseHelper.instance.getSaleItems(saleId);
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Receipt #$saleId'),
          content: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: items.map((item) {
                return Text('${item.itemName} x${item.quantity}: \$${item.amount.toStringAsFixed(2)}');
              }).toList(),
            ),
          ),
          actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('Close'))],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Sales History', style: Theme.of(context).textTheme.headlineSmall),
          SizedBox(height: 24),
          Expanded(
            child: ListView(
              children: _sales.map((sale) {
                return ListTile(
                  title: Text('Receipt #${sale.id}'),
                  subtitle: Text('Date: ${sale.saleDate} | Total: \$${sale.total.toStringAsFixed(2)}'),
                  trailing: TextButton(
                    child: Text('View Receipt'),
                    onPressed: () => _showReceipt(sale.id!),
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
