class Product {
  final int? id;
  final String name;
  final String category;
  final double price;
  final int stockLevel;
  final int reorderPoint;
  final String? imagePath;

  Product({
    this.id,
    required this.name,
    required this.category,
    required this.price,
    required this.stockLevel,
    required this.reorderPoint,
    this.imagePath,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'category': category,
      'price': price,
      'stock_level': stockLevel,
      'reorder_point': reorderPoint,
      'image_path': imagePath,
    };
  }

  factory Product.fromMap(Map<String, dynamic> map) {
    return Product(
      id: map['id'],
      name: map['name'],
      category: map['category'],
      price: map['price'].toDouble(),
      stockLevel: map['stock_level'],
      reorderPoint: map['reorder_point'],
      imagePath: map['image_path'],
    );
  }

  Product copyWith({
    int? id,
    String? name,
    String? category,
    double? price,
    int? stockLevel,
    int? reorderPoint,
    String? imagePath,
  }) {
    return Product(
      id: id ?? this.id,
      name: name ?? this.name,
      category: category ?? this.category,
      price: price ?? this.price,
      stockLevel: stockLevel ?? this.stockLevel,
      reorderPoint: reorderPoint ?? this.reorderPoint,
      imagePath: imagePath ?? this.imagePath,
    );
  }
}