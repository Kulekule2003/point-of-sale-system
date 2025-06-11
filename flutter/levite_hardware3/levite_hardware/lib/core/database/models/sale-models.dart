class Sale {
  final int? id;
  final double totalAmount;
  final DateTime saleDate;
  final String? customerName;
  final String? customerEmail;
  final String? customerPhone;
  final String paymentMethod;
  final String status; // 'completed', 'pending', 'cancelled'
  final List<SaleItem>? items;

  Sale({
    this.id,
    required this.totalAmount,
    DateTime? saleDate,
    this.customerName,
    this.customerEmail,
    this.customerPhone,
    required this.paymentMethod,
    this.status = 'completed',
    this.items,
  }) : saleDate = saleDate ?? DateTime.now();

  // Convert Sale to Map for database storage
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'total_amount': totalAmount,
      'sale_date': saleDate.toIso8601String(),
      'customer_name': customerName,
      'customer_email': customerEmail,
      'customer_phone': customerPhone,
      'payment_method': paymentMethod,
      'status': status,
    };
  }

  // Create Sale from Map (database result)
  factory Sale.fromMap(Map<String, dynamic> map) {
    return Sale(
      id: map['id'],
      totalAmount: map['total_amount'].toDouble(),
      saleDate: DateTime.parse(map['sale_date']),
      customerName: map['customer_name'],
      customerEmail: map['customer_email'],
      customerPhone: map['customer_phone'],
      paymentMethod: map['payment_method'],
      status: map['status'] ?? 'completed',
    );
  }

  // Create a copy of Sale with updated fields
  Sale copyWith({
    int? id,
    double? totalAmount,
    DateTime? saleDate,
    String? customerName,
    String? customerEmail,
    String? customerPhone,
    String? paymentMethod,
    String? status,
    List<SaleItem>? items,
  }) {
    return Sale(
      id: id ?? this.id,
      totalAmount: totalAmount ?? this.totalAmount,
      saleDate: saleDate ?? this.saleDate,
      customerName: customerName ?? this.customerName,
      customerEmail: customerEmail ?? this.customerEmail,
      customerPhone: customerPhone ?? this.customerPhone,
      paymentMethod: paymentMethod ?? this.paymentMethod,
      status: status ?? this.status,
      items: items ?? this.items,
    );
  }

  @override
  String toString() {
    return 'Sale{id: $id, totalAmount: $totalAmount, saleDate: $saleDate, status: $status}';
  }
}

class SaleItem {
  final int? id;
  final int saleId;
  final int productId;
  final String productName;
  final int quantity;
  final double unitPrice;
  final double subtotal;

  SaleItem({
    this.id,
    required this.saleId,
    required this.productId,
    required this.productName,
    required this.quantity,
    required this.unitPrice,
    required this.subtotal,
  });

  // Convert SaleItem to Map for database storage
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'sale_id': saleId,
      'product_id': productId,
      'product_name': productName,
      'quantity': quantity,
      'unit_price': unitPrice,
      'subtotal': subtotal,
    };
  }

  // Create SaleItem from Map (database result)
  factory SaleItem.fromMap(Map<String, dynamic> map) {
    return SaleItem(
      id: map['id'],
      saleId: map['sale_id'],
      productId: map['product_id'],
      productName: map['product_name'],
      quantity: map['quantity'],
      unitPrice: map['unit_price'].toDouble(),
      subtotal: map['subtotal'].toDouble(),
    );
  }

  // Create a copy of SaleItem with updated fields
  SaleItem copyWith({
    int? id,
    int? saleId,
    int? productId,
    String? productName,
    int? quantity,
    double? unitPrice,
    double? subtotal,
  }) {
    return SaleItem(
      id: id ?? this.id,
      saleId: saleId ?? this.saleId,
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      quantity: quantity ?? this.quantity,
      unitPrice: unitPrice ?? this.unitPrice,
      subtotal: subtotal ?? this.subtotal,
    );
  }

  @override
  String toString() {
    return 'SaleItem{id: $id, productName: $productName, quantity: $quantity, subtotal: $subtotal}';
  }
}