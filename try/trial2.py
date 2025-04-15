import customtkinter as ctk
from tkinter import messagebox


class Itemlist:
    def __init__(self):
        self.item_list = {}

    def add_item(self, item_name, quantity, price):
        if item_name not in self.item_list:
            self.item_list[item_name] = {
                "quantity": int(quantity),
                "price": float(price)
            }
        else:
            return "Item already exists."

    def remove_item(self, item_name):
        if item_name in self.item_list:
            del self.item_list[item_name]
        else:
            return "Item not found."

    def sell_item(self, item_name, quantity):
        if item_name in self.item_list:
            if self.item_list[item_name]["quantity"] >= quantity:
                self.item_list[item_name]["quantity"] -= quantity
            else:
                return "Not enough stock."
        else:
            return "Item not found."


class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Store POS")
        self.geometry("800x600")
        self.item_list = Itemlist()
        self.cart = {}

        self.create_widgets()

    def create_widgets(self):
        # Top Inputs
        ctk.CTkLabel(self, text="Item Name").pack()
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack()

        ctk.CTkLabel(self, text="Quantity").pack()
        self.entry_quantity = ctk.CTkEntry(self)
        self.entry_quantity.pack()

        ctk.CTkLabel(self, text="Price").pack()
        self.entry_price = ctk.CTkEntry(self)
        self.entry_price.pack()

        ctk.CTkButton(self, text="Add Item", command=self.add_item).pack(pady=5)
        ctk.CTkButton(self, text="Remove Item", command=self.remove_item).pack(pady=5)

        # Search Area
        ctk.CTkLabel(self, text="Search Inventory").pack(pady=(10, 0))
        self.search_entry = ctk.CTkEntry(self)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.search_inventory)

        self.search_listbox = ctk.CTkTextbox(self, height=100)
        self.search_listbox.pack(padx=10, pady=5, fill="x")
        self.search_listbox.bind("<Button-1>", self.select_from_search)

        # Cart Area
        ctk.CTkLabel(self, text="Cart").pack(pady=(10, 0))
        self.cart_display = ctk.CTkTextbox(self, height=100)
        self.cart_display.pack(padx=10, pady=5, fill="x")

        ctk.CTkButton(self, text="Sell Items", command=self.sell_items).pack(pady=10)

        # Inventory Output
        ctk.CTkButton(self, text="Show Inventory", command=self.show_inventory).pack(pady=10)
        self.text_display = ctk.CTkTextbox(self, height=150)
        self.text_display.pack(padx=10, pady=10, fill="both", expand=True)

    def add_item(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        if name and quantity and price:
            result = self.item_list.add_item(name, quantity, price)
            if result:
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", "Item added.")
                self.clear_entries()
                self.show_inventory()
        else:
            messagebox.showwarning("Input error", "Fill all fields.")

    def remove_item(self):
        name = self.entry_name.get()
        if name:
            result = self.item_list.remove_item(name)
            if result:
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", "Item removed.")
                self.show_inventory()
        else:
            messagebox.showwarning("Input error", "Enter item name.")

    def search_inventory(self, event=None):
        query = self.search_entry.get().lower()
        self.search_listbox.delete("1.0", "end")
        for item in self.item_list.item_list:
            if query in item.lower():
                self.search_listbox.insert("end", f"{item}\n")

    def select_from_search(self, event=None):
        index = self.search_listbox.index(f"@{event.x},{event.y}")
        selected_line = self.search_listbox.get(f"{index} linestart", f"{index} lineend").strip()
        if selected_line:
            # Prompt for quantity
            quantity = self.simple_quantity_prompt(f"Enter quantity for {selected_line}")
            if quantity:
                try:
                    quantity = int(quantity)
                    if selected_line in self.cart:
                        self.cart[selected_line] += quantity
                    else:
                        self.cart[selected_line] = quantity
                    self.update_cart_display()
                except ValueError:
                    messagebox.showwarning("Invalid", "Quantity must be a number.")

    def simple_quantity_prompt(self, prompt):
        popup = ctk.CTkInputDialog(title="Quantity", text=prompt)
        return popup.get_input()

    def update_cart_display(self):
        self.cart_display.delete("1.0", "end")
        for item, qty in self.cart.items():
            self.cart_display.insert("end", f"{item} x {qty}\n")

    def sell_items(self):
        errors = []
        for item, qty in self.cart.items():
            result = self.item_list.sell_item(item, qty)
            if result:
                errors.append(f"{item}: {result}")
        if errors:
            messagebox.showerror("Sell Errors", "\n".join(errors))
        else:
            messagebox.showinfo("Success", "Items sold successfully.")
            self.cart.clear()
            self.update_cart_display()
            self.show_inventory()

    def show_inventory(self):
        self.text_display.delete("1.0", "end")
        for item, data in self.item_list.item_list.items():
            line = f"{item} - Qty: {data['quantity']}, Price: ${data['price']:.2f}\n"
            self.text_display.insert("end", line)

    def clear_entries(self):
        self.entry_name.delete(0, "end")
        self.entry_quantity.delete(0, "end")
        self.entry_price.delete(0, "end")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = POSApp()
    app.mainloop()
