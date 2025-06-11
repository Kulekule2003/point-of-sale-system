class Sale {
  final int? id;
  final DateTime date;
  final double total;
  final List<SaleItem> items;

  Sale({
    this.id,
    required this.date,
    required this.total,
    required this.items,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'date': date.toIso8601String(),
      'total': total,
    };
  }

  factory Sale.fromMap(Map<String, dynamic> map) {
    return Sale(
      id: map['id'],
      date: DateTime.parse(map['date']),
      total: map['total'].toDouble(),
      items: [],
    );
  }
}

class SaleItem {
  final int? id;
  final int saleId;
  final int productId;
  final String productName;
  final int quantity;
  final double price;

  SaleItem({
    this.id,
    required this.saleId,
    required this.productId,
    required this.productName,
    required this.quantity,
    required this.price,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'sale_id': saleId,
      'product_id': productId,
      'product_name': productName,
      'quantity': quantity,
      'price': price,
    };
  }

  factory SaleItem.fromMap(Map<String, dynamic> map) {
    return SaleItem(
      id: map['id'],
      saleId: map['sale_id'],
      productId: map['product_id'],
      productName: map['product_name'],
      quantity: map['quantity'],
      price: map['price'].toDouble(),
    );
  }
}

