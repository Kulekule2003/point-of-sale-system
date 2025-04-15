import customtkinter as ctk
from tkinter import messagebox
from inventory_view import InventoryView

class Itemlist:
    def __init__(self):
        self.item_list = {}

    def add_item(self, item_name, quantity, price):
        self.item_list[item_name] = {
            "quantity": int(quantity),
            "price": float(price)
        }

    def sell_item(self, item_name, quantity):
        if item_name in self.item_list:
            if self.item_list[item_name]["quantity"] >= quantity:
                self.item_list[item_name]["quantity"] -= quantity
                return True
            else:
                return "Not enough stock"
        return "Item not found"


class POSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("POS Dashboard")
        self.geometry("950x680")
        self.item_list = Itemlist()
        self.cart = {}

        self.item_list.add_item("dangote cement 5kg", 20, 25000)

        self.create_ui()

    def create_ui(self):
        self.main_area = ctk.CTkFrame(self, fg_color="white")
        self.main_area.pack(side="left", fill="both", expand=True)

        # Views
        self.sell_view = ctk.CTkFrame(self.main_area, fg_color="white")
        self.sell_view.pack(fill="both", expand=True)

        self.inventory_view = InventoryView(self.main_area, self.item_list)
        self.inventory_view.pack_forget()

        self.create_sidebar()
        self.create_sell_view()  # ← This draws the sale screen into self.sell_view


    def create_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="home/sale dashboard", anchor="w", text_color="gray").pack(pady=10, padx=10)

        self.sell_btn = ctk.CTkButton(self.sidebar, text="sell", fg_color="#d9d9d9", text_color="black",command=self.show_sell)
        self.sell_btn.pack(pady=10, padx=10, fill="x")

        self.manage_inv_btn = ctk.CTkButton(self.sidebar, text="manage inventory", fg_color="#d9d9d9", text_color="black",command=self.show_inventory)
        self.manage_inv_btn.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(self.sidebar, text="ADMIN", fg_color="#d9d9d9", text_color="black").pack(side="bottom", pady=10, padx=10, fill="x")

    def create_main_area(self):
        # Search
        search_frame = ctk.CTkFrame(self.main_area, fg_color="white")
        search_frame.pack(fill="x", pady=10, padx=10)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="search", fg_color="#d9d9d9")
        self.search_entry.pack(side="right", padx=10)
        self.search_entry.bind("<KeyRelease>", self.search_inventory)

        # Cart Table Header
        header_frame = ctk.CTkFrame(self.main_area, fg_color="white")
        header_frame.pack(fill="x", padx=20)

        for text, width in zip(["item", "quantity", "unitcost", "cost", ""], [300, 100, 100, 100, 100]):
            ctk.CTkLabel(header_frame, text=text, text_color="black", width=width, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left")

        # Cart Items
        self.cart_frame = ctk.CTkScrollableFrame(self.main_area, height=300, fg_color="white")
        self.cart_frame.pack(fill="both", expand=False, padx=20, pady=5)

        # Bottom Controls
        control_frame = ctk.CTkFrame(self.main_area, fg_color="white")
        control_frame.pack(fill="x", padx=20, pady=10)

        self.clear_btn = ctk.CTkButton(control_frame, text="clear list", fg_color="#ff9999", command=self.clear_cart)
        self.clear_btn.pack(side="left")

        self.purchase_btn = ctk.CTkButton(control_frame, text="make purchase", fg_color="green", command=self.sell_items)
        self.purchase_btn.pack(side="right")

        # Receipt + Cost Area
        cost_frame = ctk.CTkFrame(self.main_area, fg_color="white")
        cost_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(cost_frame, text="TOTAL COST", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        self.total_label = ctk.CTkLabel(cost_frame, text="0", width=100, font=ctk.CTkFont(size=18), text_color="black", fg_color="#d9d9d9")
        self.total_label.pack(side="left", padx=10)

        self.receipt_btn = ctk.CTkButton(cost_frame, text="receipt", fg_color="#d9d9d9", text_color="black")
        self.receipt_btn.pack(side="left", padx=10)
    
    def show_sell(self):
        self.inventory_view.pack_forget()
        self.sell_view.pack(fill="both", expand=True)

    def show_inventory(self):
        self.sell_view.pack_forget()
        self.inventory_view.refresh_lists()
        self.inventory_view.pack(fill="both", expand=True)

    def search_inventory(self, event=None):
        query = self.search_entry.get().lower()
        for item in self.item_list.item_list:
            if query in item.lower():
                self.add_to_cart(item)
                self.search_entry.delete(0, "end")
                break

    def add_to_cart(self, item_name):
        if item_name not in self.item_list.item_list:
            return
        price = self.item_list.item_list[item_name]["price"]
        if item_name in self.cart:
            self.cart[item_name]["quantity"] += 1
        else:
            self.cart[item_name] = {"quantity": 1, "unitcost": price}
        self.update_cart_display()

    def update_cart_display(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        total = 0
        for item, data in self.cart.items():
            quantity = data["quantity"]
            unitcost = data["unitcost"]
            cost = quantity * unitcost
            total += cost

            row = ctk.CTkFrame(self.cart_frame, fg_color="#f0f0f0", corner_radius=5)
            row.pack(fill="x", padx=5, pady=5)

            for text, width in zip([item, str(quantity), f"{unitcost}", f"{cost}"], [300, 100, 100, 100]):
                ctk.CTkLabel(row, text=text, width=width, anchor="w", text_color="black").pack(side="left")

            remove_btn = ctk.CTkButton(row, text="remove", width=100, fg_color="#ff6666",
                                       command=lambda name=item: self.remove_item(name))
            remove_btn.pack(side="left", padx=5)

        self.total_label.configure(text=str(total))

    def remove_item(self, item_name):
        if item_name in self.cart:
            del self.cart[item_name]
            self.update_cart_display()

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()

    def sell_items(self):
        errors = []
        for item, data in self.cart.items():
            result = self.item_list.sell_item(item, data["quantity"])
            if result is not True:
                errors.append(f"{item}: {result}")
        if errors:
            messagebox.showerror("Sell Error", "\n".join(errors))
        else:
            messagebox.showinfo("Success", "Purchase complete!")
            self.clear_cart()


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = POSApp()
    app.mainloop()
