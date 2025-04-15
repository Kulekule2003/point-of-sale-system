import customtkinter as ctk
from inventory_view import InventoryView

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
    def print_items(self):
        return self.item_list


# ------------------ POS Application -------------------

class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x650")
        self.title("Hardware Store POS")
        self.item_list = Itemlist()

        # Sample data
        self.item_list.add_item("dangote cement 5kg", 10, 25000)
        self.item_list.add_item("paint white 2L", 4, 15000)
        self.item_list.add_item("nails 100pcs", 20, 500)

        self.cart = []
        self.create_ui()

    def create_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.sell_btn = ctk.CTkButton(self.sidebar, text="sell", fg_color="#d9d9d9", text_color="black",
                                      command=self.show_sell)
        self.sell_btn.pack(pady=10, fill="x")

        self.manage_inv_btn = ctk.CTkButton(self.sidebar, text="manage inventory", fg_color="#d9d9d9", text_color="black",
                                            command=self.show_inventory)
        self.manage_inv_btn.pack(pady=10, fill="x")

        ctk.CTkLabel(self.sidebar, text="ADMIN", fg_color="#d9d9d9", text_color="black").pack(side="bottom", pady=10)

        # Main area
        self.main_area = ctk.CTkFrame(self, fg_color="white")
        self.main_area.pack(side="left", fill="both", expand=True)

        # Views
        self.sell_view = ctk.CTkFrame(self.main_area, fg_color="white")
        self.sell_view.pack(fill="both", expand=True)

        self.inventory_view = InventoryView(self.main_area, self.item_list)
        self.inventory_view.pack_forget()

        self.create_sell_view()

    def create_sell_view(self):
        # Search
        search_bar = ctk.CTkEntry(self.sell_view, placeholder_text="search")
        search_bar.pack(pady=10)
        search_button = ctk.CTkButton(self.sell_view, text="search", command=lambda: self.search_item(search_bar.get()))
        search_button.pack()

        # Cart
        self.cart_frame = ctk.CTkFrame(self.sell_view, fg_color="white")
        self.cart_frame.pack(pady=10, fill="x")

        # Action buttons
        bottom_frame = ctk.CTkFrame(self.sell_view)
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.total_label = ctk.CTkLabel(bottom_frame, text="TOTAL COST", font=ctk.CTkFont(weight="bold"))
        self.total_label.pack(side="left", padx=20)

        self.total_amount_label = ctk.CTkLabel(bottom_frame, text="0", width=120, font=ctk.CTkFont(size=26, weight="bold"), fg_color="#d9d9d9", corner_radius=5)
        self.total_amount_label.pack(side="left")

        ctk.CTkButton(bottom_frame, text="clear list", fg_color="#f08080", command=self.clear_cart).pack(side="left", padx=10)
        ctk.CTkButton(bottom_frame, text="receipt").pack(side="left", padx=10)
        ctk.CTkButton(bottom_frame, text="make purchase", fg_color="green", command=self.make_purchase).pack(side="right", padx=20)
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

        total_cost = 0

        for item in self.cart:
            name, qty, price = item
            cost = qty * price
            total_cost += cost

            row = ctk.CTkFrame(self.cart_frame, fg_color="#d9d9d9", height=30)
            row.pack(fill="x", pady=2, padx=20)

            ctk.CTkLabel(row, text=name, anchor="w").pack(side="left", padx=5, expand=True)
            ctk.CTkLabel(row, text=str(qty)).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(price)).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(cost)).pack(side="left", padx=5)

            ctk.CTkButton(row, text="remove", fg_color="red", width=50,
                          command=lambda i=item: self.remove_from_cart(i)).pack(side="right", padx=5)

        self.total_amount_label.configure(text=str(total_cost))

    def search_item(self, search_term):
        # In a real app, this would do more
        for name, info in self.item_list.item_list.items():
            if search_term.lower() in name.lower():
                self.cart.append((name, 1, info["price"]))
                self.refresh_cart_view()
                break

    def remove_from_cart(self, item):
        self.cart.remove(item)
        self.refresh_cart_view()

    def clear_cart(self):
        self.cart = []
        self.refresh_cart_view()

    def make_purchase(self):
        for name, qty, price in self.cart:
            self.item_list.sell_item(name, qty)
        self.cart = []
        self.refresh_cart_view()

    def show_sell(self):
        self.inventory_view.pack_forget()
        self.sell_view.pack(fill="both", expand=True)

    def show_inventory(self):
        self.sell_view.pack_forget()
        self.inventory_view.refresh_lists()
        self.inventory_view.pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = POSApp()
    app.mainloop()
