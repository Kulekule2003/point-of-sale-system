class Product {
  final int? id;
  final String name;
  final String category;
  final double price;
  final int stockLevel;
  final int reorderPoint;
  final String? description;
  final DateTime createdAt;
  final DateTime updatedAt;

  Product({
    this.id,
    required this.name,
    required this.category,
    required this.price,
    required this.stockLevel,
    required this.reorderPoint,
    this.description,
    DateTime? createdAt,
    DateTime? updatedAt,
  })  : createdAt = createdAt ?? DateTime.now(),
        updatedAt = updatedAt ?? DateTime.now();

  // Convert Product to Map for database storage
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'category': category,
      'price': price,
      'stock_level': stockLevel,
      'reorder_point': reorderPoint,
      'description': description,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  // Create Product from Map (database result)
  factory Product.fromMap(Map<String, dynamic> map) {
    return Product(
      id: map['id'],
      name: map['name'],
      category: map['category'],
      price: map['price'].toDouble(),
      stockLevel: map['stock_level'],
      reorderPoint: map['reorder_point'],
      description: map['description'],
      createdAt: DateTime.parse(map['created_at']),
      updatedAt: DateTime.parse(map['updated_at']),
    );
  }

  // Create a copy of Product with updated fields
  Product copyWith({
    int? id,
    String? name,
    String? category,
    double? price,
    int? stockLevel,
    int? reorderPoint,
    String? description,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Product(
      id: id ?? this.id,
      name: name ?? this.name,
      category: category ?? this.category,
      price: price ?? this.price,
      stockLevel: stockLevel ?? this.stockLevel,
      reorderPoint: reorderPoint ?? this.reorderPoint,
      description: description ?? this.description,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  // Check if product is low in stock
  bool get isLowStock => stockLevel <= reorderPoint;

  // Check if product is out of stock
  bool get isOutOfStock => stockLevel <= 0;

  @override
  String toString() {
    return 'Product{id: $id, name: $name, category: $category, price: $price, stockLevel: $stockLevel}';
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Product &&
        other.id == id &&
        other.name == name &&
        other.category == category &&
        other.price == price &&
        other.stockLevel == stockLevel;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        name.hashCode ^
        category.hashCode ^
        price.hashCode ^
        stockLevel.hashCode;
  }
}