import customtkinter as ctk
from database import add_inventory_item, get_inventory

class ItemListPage:
    def __init__(self, master):
        self.master = master

        # Input Labels and Entries
        labels = ["Name:", "Quantity:", "Price:", "Unit Cost:"]
        self.entries = []

        for i, label in enumerate(labels):
            ctk.CTkLabel(master, text=label).place(x=10, y=10 + i * 40)
            entry = ctk.CTkEntry(master, placeholder_text=label.replace(":", "").lower(), width=200)
            entry.place(x=100, y=10 + i * 40)
            self.entries.append(entry)

        self.item_name, self.item_quantity, self.item_price, self.item_unit_cost = self.entries

        # Add and Clear Buttons
        self.add_item = ctk.CTkButton(master, text="Add Item", command=self.add_Item, width=90)
        self.add_item.place(x=10, y=190)

        self.clear_item = ctk.CTkButton(master, text="Clear Input", command=self.clear_inputs, width=90)
        self.clear_item.place(x=120, y=190)

        # Message Label
        self.message_label = ctk.CTkLabel(master, text="", text_color="green")
        self.message_label.place(x=10, y=230)

        # Search bar
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_item_list)
        self.search_entry = ctk.CTkEntry(
            master, placeholder_text="Search items...", textvariable=self.search_var, width=280
        )
        self.search_entry.place(x=10, y=260)

        # Item display list
        self.item_listbox = ctk.CTkTextbox(master, height=200, width=280)
        self.item_listbox.place(x=10, y=300)

        self.update_item_list()

    def add_Item(self):
        name = self.item_name.get()
        quantity = self.item_quantity.get()
        price = self.item_price.get()
        unit_cost = self.item_unit_cost.get()

        if not name or not quantity or not price or not unit_cost:
            self.message_label.configure(text="Please fill in all fields", text_color="red")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            unit_cost = float(unit_cost)
        except ValueError:
            self.message_label.configure(
                text="Quantity must be integer, price/unit cost must be numbers.", text_color="red"
            )
            return

        add_inventory_item(name, quantity, price, unit_cost)
        self.message_label.configure(text=f"Item '{name}' added successfully", text_color="green")
        self.clear_inputs()
        self.update_item_list()

    def clear_inputs(self):
        for entry in self.entries:
            entry.delete(0, ctk.END)

    def update_item_list(self, *args):
        search_text = self.search_var.get().lower()
        self.item_listbox.delete("1.0", ctk.END)
        items = get_inventory()
        for item in items:
            # item = (id, name, quantity, price, unit_cost)
            if search_text in item[1].lower():
                item_details = (
                    f"Name: {item[1]}, Quantity: {item[2]}, "
                    f"Price: {item[3]}, Unit Cost: {item[4]}\n"
                )
                self.item_listbox.insert(ctk.END, item_details)
