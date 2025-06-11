import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fl_chart/fl_chart.dart';
import '../providers/sales_provider.dart';

class SalesChart extends StatelessWidget {
  const SalesChart({super.key});

  @override
  Widget build(BuildContext context) {
    final monthlySales = Provider.of<SalesProvider>(context).monthlySales;

    if (monthlySales.isEmpty) {
      return const Center(child: Text('No sales data available.'));
    }

    final spots = monthlySales.asMap().entries.map((entry) {
      int idx = entry.key;
      var monthData = entry.value;
      return FlSpot(idx.toDouble(), (monthData['total'] as num).toDouble());
    }).toList();

    return SizedBox(
      height: 220,
      child: LineChart(
        LineChartData(
          titlesData: FlTitlesData(
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                getTitlesWidget: (value, meta) {
                  int idx = value.toInt();
                  if (idx < 0 || idx >= monthlySales.length) return const SizedBox();
                  String label = monthlySales[idx]['month'].substring(5); // 'YYYY-MM'
                  return Text(label, style: const TextStyle(fontSize: 12));
                },
              ),
            ),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: spots,
              isCurved: true,
              color: Colors.green,
              dotData: const FlDotData(show: false),
              belowBarData: BarAreaData(show: true, color: Colors.green.withValues()),
            ),
          ],
        ),
      ),
    );
  }
}
