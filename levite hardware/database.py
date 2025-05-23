import sqlite3

DB_NAME = "store.db"

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Inventory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                unit_cost REAL NOT NULL
            )
        """)
        # Sales table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL
            )
        """)
        # Sale items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            )
        """)

def add_inventory_item(name, quantity, price, unit_cost):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inventory (name, quantity, price, unit_cost) VALUES (?, ?, ?, ?)",
            (name, quantity, price, unit_cost)
        )

def get_inventory():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, quantity, price, unit_cost FROM inventory")
        return cursor.fetchall()

def update_inventory_quantity(item_id, new_quantity):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = ? WHERE id = ?",
            (new_quantity, item_id)
        )

def record_sale(items, total):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sales (total) VALUES (?)",
            (total,)
        )
        sale_id = cursor.lastrowid
        for item in items:
            cursor.execute(
                "INSERT INTO sale_items (sale_id, item_name, quantity, amount) VALUES (?, ?, ?, ?)",
                (sale_id, item['description'], item['quantity'], item['amount'])
            )
        return sale_id
