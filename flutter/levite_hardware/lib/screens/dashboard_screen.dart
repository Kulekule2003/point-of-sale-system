import 'package:flutter/material.dart';
import '../widgets/sidebar.dart';
import 'inventory_screen.dart';
import 'sales_screen.dart';
import 'analytics_screen.dart';
import 'sales_history_screen.dart';

class DashboardScreen extends StatefulWidget {
  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    SalesScreen(),
    InventoryScreen(),
    AnalyticsScreen(),
    SalesHistoryScreen(),
  ];

  void _onSidebarTap(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Sidebar(
            selectedIndex: _selectedIndex,
            onTap: _onSidebarTap,
          ),
          Expanded(
            child: _pages[_selectedIndex],
          ),
        ],
      ),
    );
  }
}
