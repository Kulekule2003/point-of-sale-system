import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Levite Hardware")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_title.pack(pady=20)

        self.inventory_expanded = False  # track toggle state

        self.items = []  # Store items as a list of dicts

        self.create_sidebar_buttons()
        self.show_dashboard("Home")

    def create_sidebar_buttons(self):
        dashboards = ["Home"]
        for name in dashboards:
            btn = ctk.CTkButton(self.sidebar, text=name, command=lambda n=name: self.show_dashboard(n))
            btn.pack(pady=5, fill="x")

        self.inventory_btn = ctk.CTkButton(
            self.sidebar, text="Manage Inventory ▸", command=self.toggle_inventory_submenu
        )
        self.inventory_btn.pack(pady=(20, 5), fill="x")

        self.inventory_submenu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.inventory_buttons = []

        submenu_items = ["Item List", "analytics", "Sales History"]
        for item in submenu_items:
            btn = ctk.CTkButton(
                self.inventory_submenu_frame,
                text=f"  • {item}",
                command=lambda n=item: self.show_dashboard(n),
                height=30,
                fg_color="transparent",
                anchor="w"
            )
            btn.pack(fill="x", padx=10)
            self.inventory_buttons.append(btn)

    def toggle_inventory_submenu(self):
        self.inventory_expanded = not self.inventory_expanded
        if self.inventory_expanded:
            self.inventory_btn.configure(text="Manage Inventory ▼")
            self.inventory_submenu_frame.pack(fill="x")
        else:
            self.inventory_btn.configure(text="Manage Inventory ▸")
            self.inventory_submenu_frame.forget()

    def show_dashboard(self, name):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        if name == "Home":
            self.home_dashboard()
        elif name == "Item List":
            self.Item_list()
        elif name == "analytics":
            self.analytics()
        else:
            self.Sales_history()

    def home_dashboard(self):
        title = ctk.CTkLabel(self.main_content, text="This is the home dashboard")
        title.pack(pady=20)

    def Item_list(self):
        # Entry fields for new item
        self.item_name = ctk.CTkEntry(self.main_content, placeholder_text="itemname 2kg")
        self.item_name.pack(pady=10)
        self.item_quantity = ctk.CTkEntry(self.main_content, placeholder_text="7")
        self.item_quantity.pack(pady=10)
        self.item_price = ctk.CTkEntry(self.main_content, placeholder_text="300000")
        self.item_price.pack(pady=10)
        self.item_unit_cost = ctk.CTkEntry(self.main_content, placeholder_text="3000")
        self.item_unit_cost.pack(pady=10)
        self.add_item = ctk.CTkButton(self.main_content, text="Add Item", command=self.add_Item)
        self.add_item.pack(padx=10)
        self.clear_item = ctk.CTkButton(self.main_content, text="Clear input", command=self.clear_inputs)
        self.clear_item.pack(padx=10)

        # Message label
        self.message_label = ctk.CTkLabel(self.main_content, text="")
        self.message_label.pack(pady=10)

        # Search bar
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_item_list)
        self.search_entry = ctk.CTkEntry(self.main_content, placeholder_text="Search items...", textvariable=self.search_var)
        self.search_entry.pack(pady=10, fill="x")

        # Display area
        self.item_listbox = ctk.CTkTextbox(self.main_content, height=200)
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

    def analytics(self):
        title = ctk.CTkLabel(self.main_content, text="this is the analytics dashboard")
        title.pack(pady=20)

    def Sales_history(self):
        title = ctk.CTkLabel(self.main_content, text="This is the sales history")
        title.pack(pady=20)

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
