import customtkinter as ctk
from inventory_view import InventoryView

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Point of Sale Backend
class Itemlist:
    def __init__(self):
        self.item_list = {}

    def add_item(self, item_name, quantity, price):
        if item_name not in self.item_list:
            self.item_list[item_name] = {"quantity": quantity, "price": price}
        else:
            return "item already exists"

    def remove_item(self, item_name):
        if item_name in self.item_list:
            del self.item_list[item_name]

    def sell_item(self, item_name, quantity):
        if item_name in self.item_list and self.item_list[item_name]["quantity"] >= quantity:
            self.item_list[item_name]["quantity"] -= quantity
        else:
            return "not enough stock"

class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Store POS")
        self.geometry("1000x700")

        self.item_list = Itemlist()
        self.cart = []  # [(name, quantity, unit_price)]

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(sidebar, text="home/sale dashboard", anchor="w").pack(pady=(10, 20), padx=10)

        ctk.CTkButton(sidebar, text="sell", command=self.show_sell_view).pack(pady=5, fill="x")
        ctk.CTkButton(sidebar, text="manage inventory", command=self.show_inventory_view).pack(pady=5, fill="x")
        ctk.CTkLabel(sidebar, text="ADMIN", anchor="center").pack(side="bottom", pady=10)

        # Main content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(expand=True, fill="both")

        self.sell_view = ctk.CTkFrame(self.main_frame)
        self.inventory_view = InventoryView(self.main_frame, self.item_list)

        self.create_sell_view()
        self.show_sell_view()

    def show_sell_view(self):
        self.inventory_view.pack_forget()
        self.sell_view.pack(expand=True, fill="both")

    def show_inventory_view(self):
        self.sell_view.pack_forget()
        self.inventory_view.pack(expand=True, fill="both")
        self.inventory_view.update_item_stats()

    def create_sell_view(self):
        # Search area
        search_frame = ctk.CTkFrame(self.sell_view)
        search_frame.pack(pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="search")
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.update_search_results)

        self.search_results_frame = ctk.CTkFrame(self.sell_view, fg_color="white")
        self.search_results_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Cart display
        self.cart_frame = ctk.CTkFrame(self.sell_view)
        self.cart_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.refresh_cart_view()

        # Bottom controls
        control_frame = ctk.CTkFrame(self.sell_view)
        control_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        ctk.CTkButton(control_frame, text="clear list", fg_color="red", command=self.clear_cart).pack(side="left")
        ctk.CTkLabel(control_frame, text="TOTAL COST", font=("Arial", 16)).pack(side="left", padx=20)
        self.total_cost_label = ctk.CTkLabel(control_frame, text="0", font=("Arial", 24))
        self.total_cost_label.pack(side="left")
        ctk.CTkButton(control_frame, text="receipt").pack(side="left", padx=10)
        ctk.CTkButton(control_frame, text="make purchase", fg_color="green", command=self.make_purchase).pack(side="right")

    def update_search_results(self, event=None):
        search_term = self.search_entry.get().lower()

        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

        if not search_term:
            return

        for name, info in self.item_list.item_list.items():
            if search_term in name.lower():
                ctk.CTkButton(
                    self.search_results_frame,
                    text=f"{name} (₦{info['price']})",
                    anchor="w",
                    command=lambda n=name, p=info["price"]: self.add_item_to_cart(n, p)
                ).pack(fill="x", pady=2)

    def add_item_to_cart(self, name, price):
        popup = ctk.CTkToplevel(self)
        popup.title("Enter Quantity")
        popup.geometry("250x150")

        ctk.CTkLabel(popup, text=f"Add quantity for: {name}").pack(pady=10)
        quantity_entry = ctk.CTkEntry(popup, placeholder_text="Quantity")
        quantity_entry.pack(pady=5)

        def confirm():
            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid quantity")
                return

            available = self.item_list.item_list[name]["quantity"]
            if quantity > available:
                print(f"Only {available} available in stock")
                return

            self.cart.append((name, quantity, price))
            self.refresh_cart_view()
            popup.destroy()

        ctk.CTkButton(popup, text="Add to Cart", command=confirm).pack(pady=10)

    def refresh_cart_view(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        headers = ctk.CTkFrame(self.cart_frame)
        headers.pack(fill="x")
        for col in ["item", "quantity", "unitcost", "cost"]:
            ctk.CTkLabel(headers, text=col, width=100).pack(side="left")

        total = 0
        for i, (name, quantity, unit_price) in enumerate(self.cart):
            row = ctk.CTkFrame(self.cart_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=name, width=100).pack(side="left")
            ctk.CTkLabel(row, text=str(quantity), width=100).pack(side="left")
            ctk.CTkLabel(row, text=str(unit_price), width=100).pack(side="left")
            cost = quantity * unit_price
            total += cost
            ctk.CTkLabel(row, text=str(cost), width=100).pack(side="left")
            ctk.CTkButton(row, text="remove", fg_color="red", width=80, command=lambda i=i: self.remove_item(i)).pack(side="left")

        self.total_cost_label.configure(text=str(total))

    def remove_item(self, index):
        if 0 <= index < len(self.cart):
            del self.cart[index]
            self.refresh_cart_view()

    def clear_cart(self):
        self.cart = []
        self.refresh_cart_view()

    def make_purchase(self):
        for name, quantity, _ in self.cart:
            self.item_list.sell_item(name, quantity)
        print("Purchase complete")
        self.clear_cart()

if __name__ == "__main__":
    app = POSApp()
    app.mainloop()