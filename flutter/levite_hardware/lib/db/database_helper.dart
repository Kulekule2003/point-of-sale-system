import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/inventory_item.dart';
import '../models/sale.dart';
import '../models/sale_item.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('store.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future _createDB(Database db, int version) async {
    // Inventory Table
    await db.execute('''
      CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        unit_cost REAL NOT NULL
      )
    ''');

    // Sales Table
    await db.execute('''
      CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        total REAL NOT NULL
      )
    ''');

    // Sale Items Table
    await db.execute('''
      CREATE TABLE sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales(id)
      )
    ''');
  }

  // ========== Inventory CRUD Operations ==========
  Future<int> insertInventory(InventoryItem item) async {
    final db = await database;
    return await db.insert('inventory', item.toMap());
  }

  Future<List<InventoryItem>> getAllInventory() async {
    final db = await database;
    final result = await db.query('inventory');
    return result.map((e) => InventoryItem.fromMap(e)).toList();
  }

  Future<int> updateInventoryQuantity(int id, int newQuantity) async {
    final db = await database;
    return await db.update(
      'inventory',
      {'quantity': newQuantity},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  // ========== Sales Operations ==========
  Future<int> insertSale(Sale sale) async {
    final db = await database;
    return await db.insert('sales', sale.toMap());
  }

  Future<List<Sale>> getAllSales() async {
    final db = await database;
    final result = await db.query('sales', orderBy: 'sale_date DESC');
    return result.map((e) => Sale.fromMap(e)).toList();
  }

  // ========== Sale Items Operations ==========
  Future<int> insertSaleItem(SaleItem item) async {
    final db = await database;
    return await db.insert('sale_items', item.toMap());
  }

  Future<List<SaleItem>> getSaleItems(int saleId) async {
    final db = await database;
    final result = await db.query(
      'sale_items',
      where: 'sale_id = ?',
      whereArgs: [saleId],
    );
    return result.map((e) => SaleItem.fromMap(e)).toList();
  }

  // Close database connection
  Future close() async {
    final db = await instance.database;
    db.close();
  }
}
