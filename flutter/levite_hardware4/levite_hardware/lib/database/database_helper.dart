// database/database_helper.dart
import 'package:path/path.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import '../models/product.dart';
import '../models/category.dart';
import '../models/sale.dart';

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'pos_database.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    // Create products table
    await db.execute('''
      CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_level INTEGER NOT NULL,
        reorder_point INTEGER NOT NULL,
        image_path TEXT
      )
    ''');

    // Create categories table
    await db.execute('''
      CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
      )
    ''');

    // Create sales table
    await db.execute('''
      CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        total REAL NOT NULL
      )
    ''');

    // Create sale_items table
    await db.execute('''
      CREATE TABLE sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
      )
    ''');

    // Insert default categories
    await _insertDefaultData(db);
  }

  Future<void> _insertDefaultData(Database db) async {
    final categories = ['Tools', 'Materials', 'Safety Gear', 'Fasteners', 'Supplies'];
    for (String category in categories) {
      await db.insert('categories', {'name': category});
    }

    // Insert sample products
    final sampleProducts = [
      {'name': 'Hammer', 'category': 'Tools', 'price': 15.99, 'stock_level': 50, 'reorder_point': 20},
      {'name': 'Screwdriver Set', 'category': 'Tools', 'price': 29.99, 'stock_level': 100, 'reorder_point': 50},
      {'name': 'Power Drill', 'category': 'Tools', 'price': 79.99, 'stock_level': 20, 'reorder_point': 5},
      {'name': 'Measuring Tape', 'category': 'Tools', 'price': 9.99, 'stock_level': 80, 'reorder_point': 30},
      {'name': 'Wrench Set', 'category': 'Tools', 'price': 49.99, 'stock_level': 80, 'reorder_point': 30},
      {'name': 'Pliers', 'category': 'Tools', 'price': 19.99, 'stock_level': 120, 'reorder_point': 30},
      {'name': 'Screws', 'category': 'Fasteners', 'price': 5.99, 'stock_level': 200, 'reorder_point': 50},
      {'name': 'Paint', 'category': 'Supplies', 'price': 25.99, 'stock_level': 30, 'reorder_point': 10},
      {'name': 'Gloves', 'category': 'Safety Gear', 'price': 8.99, 'stock_level': 80, 'reorder_point': 30},
    ];

    for (Map<String, dynamic> product in sampleProducts) {
      await db.insert('products', product);
    }
  }

  // Product operations
  Future<int> insertProduct(Product product) async {
    final db = await database;
    return await db.insert('products', product.toMap());
  }

  Future<List<Product>> getProducts() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('products');
    return List.generate(maps.length, (i) => Product.fromMap(maps[i]));
  }

  Future<List<Product>> getProductsByCategory(String category) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'products',
      where: 'category = ?',
      whereArgs: [category],
    );
    return List.generate(maps.length, (i) => Product.fromMap(maps[i]));
  }

  Future<void> updateProduct(Product product) async {
    final db = await database;
    await db.update(
      'products',
      product.toMap(),
      where: 'id = ?',
      whereArgs: [product.id],
    );
  }

  Future<void> updateProductStock(int productId, int newStock) async {
    final db = await database;
    await db.update(
      'products',
      {'stock_level': newStock},
      where: 'id = ?',
      whereArgs: [productId],
    );
  }

  // Category operations
  Future<List<Category>> getCategories() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('categories');
    return List.generate(maps.length, (i) => Category.fromMap(maps[i]));
  }

  // Sales operations
  Future<int> insertSale(Sale sale) async {
    final db = await database;
    final saleId = await db.insert('sales', sale.toMap());
    
    for (SaleItem item in sale.items) {
      await db.insert('sale_items', item.copyWith(saleId: saleId).toMap());
      // Update product stock
      await db.rawUpdate(
        'UPDATE products SET stock_level = stock_level - ? WHERE id = ?',
        [item.quantity, item.productId],
      );
    }
    
    return saleId;
  }

  Future<List<Sale>> getSales() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('sales', orderBy: 'date DESC');
    return List.generate(maps.length, (i) => Sale.fromMap(maps[i]));
  }

  Future<List<SaleItem>> getSaleItems(int saleId) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'sale_items',
      where: 'sale_id = ?',
      whereArgs: [saleId],
    );
    return List.generate(maps.length, (i) => SaleItem.fromMap(maps[i]));
  }

  Future<Map<String, dynamic>> getSalesAnalytics() async {
    final db = await database;
    
    // Get total sales for current month
    final now = DateTime.now();
    final startOfMonth = DateTime(now.year, now.month, 1);
    final startOfLastMonth = DateTime(now.year, now.month - 1, 1);
    
    final currentMonthSales = await db.rawQuery(
      'SELECT SUM(total) as total FROM sales WHERE date >= ?',
      [startOfMonth.toIso8601String()],
    );
    
    final lastMonthSales = await db.rawQuery(
      'SELECT SUM(total) as total FROM sales WHERE date >= ? AND date < ?',
      [startOfLastMonth.toIso8601String(), startOfMonth.toIso8601String()],
    );
    
    // Get top selling items
    final topItems = await db.rawQuery('''
      SELECT product_name, SUM(quantity) as units_sold, SUM(quantity * price) as revenue
      FROM sale_items 
      GROUP BY product_name 
      ORDER BY units_sold DESC 
      LIMIT 5
    ''');
    
    double currentTotal = (currentMonthSales.first['total'] as num?)?.toDouble() ?? 0.0;
    double lastTotal = (lastMonthSales.first['total'] as num?)?.toDouble() ?? 0.0;

    double growthRate = lastTotal > 0 ? ((currentTotal - lastTotal) / lastTotal) * 100 : 0.0;
    
    return {
      'currentMonthSales': currentTotal,
      'growthRate': growthRate,
      'topSellingItems': topItems,
    };
  }

  Future<List<Map<String, dynamic>>> getMonthlySalesData() async {
    final db = await database;
    return await db.rawQuery('''
      SELECT 
        strftime('%Y-%m', date) as month,
        SUM(total) as total
      FROM sales 
      WHERE date >= date('now', '-6 months')
      GROUP BY strftime('%Y-%m', date)
      ORDER BY month
    ''');
  }
}

extension SaleItemExtension on SaleItem {
  SaleItem copyWith({
    int? id,
    int? saleId,
    int? productId,
    String? productName,
    int? quantity,
    double? price,
  }) {
    return SaleItem(
      id: id ?? this.id,
      saleId: saleId ?? this.saleId,
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      quantity: quantity ?? this.quantity,
      price: price ?? this.price,
    );
  }
}