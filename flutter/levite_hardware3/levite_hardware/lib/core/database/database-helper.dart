import 'dart:async';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/product.dart';
import '../models/sale.dart';
import '../models/sale_item.dart';

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  static Database? _database;

  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'pos_system.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDatabase,
    );
  }

  Future<void> _createDatabase(Database db, int version) async {
    // Create products table
    await db.execute('''
      CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_level INTEGER NOT NULL DEFAULT 0,
        reorder_point INTEGER NOT NULL DEFAULT 10,
        description TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    ''');

    // Create sales table
    await db.execute('''
      CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_amount REAL NOT NULL,
        sale_date TEXT NOT NULL,
        customer_name TEXT,
        customer_email TEXT,
        customer_phone TEXT,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed'
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
        unit_price REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
      )
    ''');

    // Insert sample data
    await _insertSampleData(db);
  }

  Future<void> _insertSampleData(Database db) async {
    // Sample products
    final sampleProducts = [
      {
        'name': 'Hammer',
        'category': 'Tools',
        'price': 15.99,
        'stock_level': 50,
        'reorder_point': 20,
        'description': 'Professional hammer for construction work',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Screwdriver Set',
        'category': 'Tools',
        'price': 29.99,
        'stock_level': 100,
        'reorder_point': 50,
        'description': 'Complete screwdriver set with multiple sizes',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Power Drill',
        'category': 'Tools',
        'price': 79.99,
        'stock_level': 20,
        'reorder_point': 5,
        'description': 'Electric power drill with multiple bits',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Measuring Tape',
        'category': 'Tools',
        'price': 9.99,
        'stock_level': 80,
        'reorder_point': 30,
        'description': '25ft measuring tape',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Wrench Set',
        'category': 'Tools',
        'price': 49.99,
        'stock_level': 60,
        'reorder_point': 30,
        'description': 'Complete wrench set',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Pliers',
        'category': 'Tools',
        'price': 19.99,
        'stock_level': 120,
        'reorder_point': 30,
        'description': 'Multi-purpose pliers',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Screws',
        'category': 'Fasteners',
        'price': 1.00,
        'stock_level': 200,
        'reorder_point': 50,
        'description': 'Assorted screws pack',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Paint',
        'category': 'Supplies',
        'price': 2.50,
        'stock_level': 30,
        'reorder_point': 10,
        'description': 'Multi-purpose paint',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
      {
        'name': 'Gloves',
        'category': 'Safety',
        'price': 8.00,
        'stock_level': 90,
        'reorder_point': 30,
        'description': 'Work gloves for safety',
        'created_at': DateTime.now().toIso8601String(),
        'updated_at': DateTime.now().toIso8601String(),
      },
    ];

    for (var product in sampleProducts) {
      await db.insert('products', product);
    }
  }

  // PRODUCT CRUD OPERATIONS
  Future<int> insertProduct(Product product) async {
    final db = await database;
    return await db.insert('products', product.toMap());
  }

  Future<List<Product>> getAllProducts() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('products');
    return List.generate(maps.length, (i) => Product.fromMap(maps[i]));
  }

  Future<Product?> getProduct(int id) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'products',
      where: 'id = ?',
      whereArgs: [id],
    );
    if (maps.isNotEmpty) {
      return Product.fromMap(maps.first);
    }
    return null;
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

  Future<int> updateProduct(Product product) async {
    final db = await database;
    return await db.update(
      'products',
      product.copyWith(updatedAt: DateTime.now()).toMap(),
      where: 'id = ?',
      whereArgs: [product.id],
    );
  }

  Future<int> deleteProduct(int id) async {
    final db = await database;
    return await db.delete(
      'products',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<int> updateProductStock(int productId, int newStockLevel) async {
    final db = await database;
    return await db.update(
      'products',
      {
        'stock_level': newStockLevel,
        'updated_at': DateTime.now().toIso8601String(),
      },
      where: 'id = ?',
      whereArgs: [productId],
    );
  }

  // SALES CRUD OPERATIONS
  Future<int> insertSale(Sale sale) async {
    final db = await database;
    return await db.insert('sales', sale.toMap());
  }

  Future<List<Sale>> getAllSales() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'sales',
      orderBy: 'sale_date DESC',
    );
    return List.generate(maps.length, (i) => Sale.fromMap(maps[i]));
  }

  Future<Sale?> getSale(int id) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'sales',
      where: 'id = ?',
      whereArgs: [id],
    );
    if (maps.isNotEmpty) {
      return Sale.fromMap(maps.first);
    }
    return null;
  }

  Future<List<Sale>> getSalesByDateRange(DateTime start, DateTime end) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'sales',
      where: 'sale_date BETWEEN ? AND ?',
      whereArgs: [start.toIso8601String(), end.toIso8601String()],
      orderBy: 'sale_date DESC',
    );
    return List.generate(maps.length, (i) => Sale.fromMap(maps[i]));
  }

  // SALE ITEMS CRUD OPERATIONS
  Future<int> insertSaleItem(SaleItem saleItem) async {
    final db = await database;
    return await db.insert('sale_items', saleItem.toMap());
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

  // ANALYTICS QUERIES
  Future<double> getTotalSalesAmount() async {
    final db = await database;
    final result = await db.rawQuery('SELECT SUM(total_amount) as total FROM sales');
    return (result.first['total'] as double?) ?? 0.0;
  }

  Future<double> getSalesAmountForPeriod(DateTime start, DateTime end) async {
    final db = await database;
    final result = await db.rawQuery(
      'SELECT SUM(total_amount) as total FROM sales WHERE sale_date BETWEEN ? AND ?',
      [start.toIso8601String(), end.toIso8601String()],
    );
    return (result.first['total'] as double?) ?? 0.0;
  }

  Future<List<Map<String, dynamic>>> getTopSellingProducts() async {
    final db = await database;
    return await db.rawQuery('''
      SELECT 
        p.name as product_name,
        p.category,
        SUM(si.quantity) as units_sold,
        SUM(si.subtotal) as revenue
      FROM sale_items si
      JOIN products p ON si.product_id = p.id
      GROUP BY si.product_id
      ORDER BY units_sold DESC
      LIMIT 10
    ''');
  }

  Future<List<Map<String, dynamic>>> getLowStockProducts() async {
    final db = await database;
    return await db.rawQuery('''
      SELECT * FROM products 
      WHERE stock_level <= reorder_point
      ORDER BY stock_level ASC
    ''');
  }

  Future<List<Map<String, dynamic>>> getMonthlySalesData() async {
    final db = await database;
    return await db.rawQuery('''
      SELECT 
        strftime('%Y-%m', sale_date) as month,
        SUM(total_amount) as total_amount,
        COUNT(*) as transaction_count
      FROM sales
      WHERE sale_date >= date('now', '-12 months')
      GROUP BY strftime('%Y-%m', sale_date)
      ORDER BY month
    ''');
  }

  // DATABASE UTILITIES
  Future<void> closeDatabase() async {
    final db = await database;
    await db.close();
  }

  Future<void> deleteDatabase() async {
    String path = join(await getDatabasesPath(), 'pos_system.db');
    await databaseFactory.deleteDatabase(path);
    _database = null;
  }
}