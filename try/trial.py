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
            if self.item_list[item_name]["quantity"] >= int(quantity):
                self.item_list[item_name]["quantity"] -= int(quantity)
            else:
                return "Not enough stock."
        else:
            return "Item not found."


class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hardware Store POS")
        self.geometry("600x500")
        self.item_list = Itemlist()

        self.create_widgets()

    def create_widgets(self):
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
        ctk.CTkButton(self, text="Sell Item", command=self.sell_item).pack(pady=5)
        ctk.CTkButton(self, text="Show Inventory", command=self.show_inventory).pack(pady=10)

        self.text_display = ctk.CTkTextbox(self, height=200)
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
        else:
            messagebox.showwarning("Input error", "Enter item name.")

    def sell_item(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        if name and quantity:
            result = self.item_list.sell_item(name, quantity)
            if result:
                messagebox.showerror("Error", result)
            else:
                messagebox.showinfo("Success", "Item sold.")
                self.clear_entries()
        else:
            messagebox.showwarning("Input error", "Enter item name and quantity.")

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
