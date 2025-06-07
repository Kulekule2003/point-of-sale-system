class InventoryItem {
  final int? id;
  final String name;
  final int quantity;
  final double price;
  final double unitCost;

  InventoryItem({
    this.id,
    required this.name,
    required this.quantity,
    required this.price,
    required this.unitCost,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'quantity': quantity,
      'price': price,
      'unit_cost': unitCost,
    };
  }

  factory InventoryItem.fromMap(Map<String, dynamic> map) {
    return InventoryItem(
      id: map['id'],
      name: map['name'],
      quantity: map['quantity'],
      price: map['price'],
      unitCost: map['unit_cost'],
    );
  }
}
