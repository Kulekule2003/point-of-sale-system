class SaleItem {
  final int? id;
  final int saleId;
  final String itemName;
  final int quantity;
  final double amount;

  SaleItem({this.id, required this.saleId, required this.itemName, required this.quantity, required this.amount});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'sale_id': saleId,
      'item_name': itemName,
      'quantity': quantity,
      'amount': amount,
    };
  }

  factory SaleItem.fromMap(Map<String, dynamic> map) {
    return SaleItem(
      id: map['id'],
      saleId: map['sale_id'],
      itemName: map['item_name'],
      quantity: map['quantity'],
      amount: map['amount'],
    );
  }
}