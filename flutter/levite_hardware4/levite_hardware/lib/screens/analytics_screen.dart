import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/sales_provider.dart';
import '../widgets/sales_chart.dart';

class AnalyticsScreen extends StatelessWidget {
  const AnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final salesProvider = Provider.of<SalesProvider>(context);
    final analytics = salesProvider.analytics;
    final topItems = analytics['topSellingItems'] ?? [];
    final currentMonthSales = analytics['currentMonthSales'] ?? 0.0;
    final growthRate = analytics['growthRate'] ?? 0.0;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Analytics', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          const Text('Sales Trends', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Row(
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('\$${currentMonthSales.toStringAsFixed(2)}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                      Text(
                        growthRate >= 0 ? 'This Month +${growthRate.toStringAsFixed(1)}%' : 'This Month ${growthRate.toStringAsFixed(1)}%',
                        style: TextStyle(color: growthRate >= 0 ? Colors.green : Colors.red),
                      ),
                    ],
                  ),
                  const SizedBox(width: 32),
                  const Expanded(child: SalesChart()),
                ],
              ),
            ),
          ),
          const SizedBox(height: 32),
          const Text('Top Selling Items', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          Card(
            child: DataTable(
              columns: const [
                DataColumn(label: Text('Product')),
                DataColumn(label: Text('Units Sold')),
                DataColumn(label: Text('Revenue')),
              ],
              rows: topItems.map<DataRow>((item) {
                return DataRow(
                  cells: [
                    DataCell(Text(item['product_name'] ?? '')),
                    DataCell(Text('${item['units_sold'] ?? 0}')),
                    DataCell(Text('\$${(item['revenue'] ?? 0).toStringAsFixed(2)}')),
                  ],
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
