import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  final int selectedIndex;
  final Function(int) onTap;

  Sidebar({required this.selectedIndex, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final items = [
      {'icon': Icons.home, 'label': 'Home'},
      {'icon': Icons.inventory, 'label': 'Inventory'},
      {'icon': Icons.analytics, 'label': 'Analytics'},
      {'icon': Icons.receipt_long, 'label': 'Sales History'},
    ];

    return Container(
      width: 200,
      color: Colors.blue[800],
      child: Column(
        children: [
          SizedBox(height: 40),
          Text(
            'Dashboard',
            style: TextStyle(
              color: Colors.white,
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 40),
          ...List.generate(items.length, (i) {
            return ListTile(
              leading: Icon(items[i]['icon'] as IconData, color: Colors.white),
              title: Text(
                items[i]['label'] as String,
                style: TextStyle(color: Colors.white),
              ),
              selected: selectedIndex == i,
              selectedTileColor: Colors.blue[600],
              onTap: () => onTap(i),
            );
          }),
        ],
      ),
    );
  }
}
