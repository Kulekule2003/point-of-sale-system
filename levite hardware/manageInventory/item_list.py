import customtkinter as ctk

class ItemListPage:
    def __init__(self, master, items):
        self.master = master
        self.items = items

        self.item_name = ctk.CTkEntry(master, placeholder_text="itemname 2kg")
        self.item_name.pack(pady=10)
        self.item_quantity = ctk.CTkEntry(master, placeholder_text="7")
        self.item_quantity.pack(pady=10)
        self.item_price = ctk.CTkEntry(master, placeholder_text="300000")
        self.item_price.pack(pady=10)
        self.item_unit_cost = ctk.CTkEntry(master, placeholder_text="3000")
        self.item_unit_cost.pack(pady=10)
        self.add_item = ctk.CTkButton(master, text="Add Item", command=self.add_Item)
        self.add_item.pack(padx=10)
        self.clear_item = ctk.CTkButton(master, text="Clear input", command=self.clear_inputs)
        self.clear_item.pack(padx=10)

        self.message_label = ctk.CTkLabel(master, text="")
        self.message_label.pack(pady=10)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_item_list)
        self.search_entry = ctk.CTkEntry(master, placeholder_text="Search items...", textvariable=self.search_var)
        self.search_entry.pack(pady=10, fill="x")

        self.item_listbox = ctk.CTkTextbox(master, height=200)
        self.item_listbox.pack(pady=10, fill="both", expand=True)
        self.update_item_list()

    def add_Item(self):
        name = self.item_name.get()
        quantity = self.item_quantity.get()
        price = self.item_price.get()
        unit_cost = self.item_unit_cost.get()

        if not name or not quantity or not price or not unit_cost:
            self.message_label.configure(text="Please fill in all fields")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            unit_cost = float(unit_cost)
        except ValueError:
            self.message_label.configure(text="Quantity must be an integer, price and unit cost must be numbers.")
            return

        item = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "unit_cost": unit_cost,
        }

        self.items.append(item)
        self.message_label.configure(text=f"Item '{name}' added successfully")
        self.clear_inputs()
        self.update_item_list()

    def clear_inputs(self):
        self.item_name.delete(0, ctk.END)
        self.item_quantity.delete(0, ctk.END)
        self.item_price.delete(0, ctk.END)
        self.item_unit_cost.delete(0, ctk.END)

    def update_item_list(self, *args):
        search_text = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        self.item_listbox.delete("1.0", ctk.END)
        for item in self.items:
            if search_text in item["name"].lower():
                item_details = (
                    f"Name: {item['name']}, Quantity: {item['quantity']}, "
                    f"Price: {item['price']}, Unit cost: {item['unit_cost']}\n"
                )
                self.item_listbox.insert(ctk.END, item_details)
