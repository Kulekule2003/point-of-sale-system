import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/cart_provider.dart';

class CartWidget extends StatelessWidget {
  const CartWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final cart = Provider.of<CartProvider>(context);

    return Card(
      margin: const EdgeInsets.all(8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            const Text('Cart', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const Divider(),
            ...cart.items.map((item) => ListTile(
                  leading: item.product.imagePath != null
                      ? Image.asset(item.product.imagePath!, width: 32, height: 32)
                      : const Icon(Icons.image),
                  title: Text(item.product.name),
                  subtitle: Text('\$${item.product.price.toStringAsFixed(2)}'),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.remove),
                        onPressed: () => cart.removeItem(item.product),
                      ),
                      Text('${item.quantity}'),
                      IconButton(
                        icon: const Icon(Icons.add),
                        onPressed: () => cart.addItem(item.product),
                      ),
                    ],
                  ),
                )),
            const Divider(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Total:', style: TextStyle(fontWeight: FontWeight.bold)),
                Text('\$${cart.total.toStringAsFixed(2)}', style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: cart.items.isNotEmpty ? () => cart.completePurchase() : null,
              child: const Text('Complete Purchase'),
            ),
            TextButton(
              onPressed: cart.items.isNotEmpty ? () => cart.clearCart() : null,
              child: const Text('Clear Cart'),
            ),
          ],
        ),
      ),
    );
  }
}
