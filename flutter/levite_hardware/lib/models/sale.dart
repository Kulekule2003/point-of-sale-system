class Sale {
  final int? id;
  final String saleDate;
  final double total;

  Sale({this.id, required this.saleDate, required this.total});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'sale_date': saleDate,
      'total': total,
    };
  }

  factory Sale.fromMap(Map<String, dynamic> map) {
    return Sale(
      id: map['id'],
      saleDate: map['sale_date'],
      total: map['total'],
    );
  }
}
