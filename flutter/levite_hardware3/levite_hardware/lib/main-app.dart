import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'features/sales/providers/sales_provider.dart';
import 'features/inventory/providers/inventory_provider.dart';
import 'features/analytics/providers/analytics_provider.dart';
import 'features/sales/screens/sales_screen.dart';
import 'features/inventory/screens/inventory_screen.dart';
import 'features/analytics/screens/analytics_screen.dart';
import 'core/theme/app_theme.dart';
import 'shared/widgets/custom_app_bar.dart';
import 'shared/widgets/navigation_rail.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SalesProvider()),
        ChangeNotifierProvider(create: (_) => InventoryProvider()),
        ChangeNotifierProvider(create: (_) => AnalyticsProvider()),
      ],
      child: MaterialApp(
        title: 'Tool Emporium POS',
        theme: AppTheme.lightTheme,
        debugShowCheckedModeBanner: false,
        home: MainScreen(),
      ),
    );
  }
}

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    SalesScreen(),
    InventoryScreen(),
    AnalyticsScreen(),
  ];

  final List<String> _screenTitles = [
    'Sales',
    'Inventory',
    'Analytics',
  ];

  final List<IconData> _screenIcons = [
    Icons.point_of_sale,
    Icons.inventory_2,
    Icons.analytics,
  ];

  @override
  void initState() {
    super.initState();
    // Initialize providers
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SalesProvider>().loadProducts();
      context.read<InventoryProvider>().loadProducts();
      context.read<AnalyticsProvider>().loadAnalyticsData();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: Row(
        children: [
          // Navigation Rail for desktop
          CustomNavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: (index) {
              setState(() {
                _selectedIndex = index;
              });
            },
            destinations: List.generate(
              _screenTitles.length,
              (index) => NavigationRailDestination(
                icon: Icon(_screenIcons[index]),
                selectedIcon: Icon(_screenIcons[index]),
                label: Text(_screenTitles[index]),
              ),
            ),
          ),
          
          // Main content area
          Expanded(
            child: Column(
              children: [
                // Custom App Bar
                CustomAppBar(
                  title: _screenTitles[_selectedIndex],
                  selectedIndex: _selectedIndex,
                  onTabChanged: (index) {
                    setState(() {
                      _selectedIndex = index;
                    });
                  },
                  tabs: _screenTitles,
                ),
                
                // Screen content
                Expanded(
                  child: _screens[_selectedIndex],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Cart Item class for managing shopping cart
class CartItem {
  final int productId;
  final String productName;
  final double price;
  int quantity;

  CartItem({
    required this.productId,
    required this.productName,
    required this.price,
    this.quantity = 1,
  });

  double get total => price * quantity;

  Map<String, dynamic> toMap() {
    return {
      'productId': productId,
      'productName': productName,
      'price': price,
      'quantity': quantity,
      'total': total,
    };
  }

  CartItem copyWith({
    int? productId,
    String? productName,
    double? price,
    int? quantity,
  }) {
    return CartItem(
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      price: price ?? this.price,
      quantity: quantity ?? this.quantity,
    );
  }

  @override
  String toString() {
    return 'CartItem{productId: $productId, productName: $productName, quantity: $quantity, total: $total}';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is CartItem &&
        other.productId == productId &&
        other.productName == productName &&
        other.price == price &&
        other.quantity == quantity;
  }

  @override
  int get hashCode {
    return productId.hashCode ^
        productName.hashCode ^
        price.hashCode ^
        quantity.hashCode;
  }
}