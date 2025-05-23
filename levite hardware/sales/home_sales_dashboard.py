import customtkinter as ctk
from sales import receipt_generator
from CustomTkinterMessagebox import CTkMessagebox
from database import update_inventory_quantity, record_sale, get_inventory

class HomeSalesDashboard:
    def __init__(self, master):
        self.master = master
        self.refresh_inventory()  # Load inventory from DB
        self.sale_rows = []

        # Header
        header = ctk.CTkLabel(master, text="home/sale dashboard", font=ctk.CTkFont(size=16), anchor="w")
        header.pack(fill="x", pady=(0, 10))

        # Search bar
        search_frame = ctk.CTkFrame(master, fg_color="white")
        search_frame.pack(fill="x", padx=10)
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_search_results)
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="search", width=140, font=ctk.CTkFont(weight="bold"), fg_color="#e5e5e5")
        search_entry.pack(side="right", padx=2, pady=2)

        # Search results list
        self.results_frame = ctk.CTkFrame(master, fg_color="white", height=100)
        self.results_frame.pack(fill="x", padx=10, pady=10)
        self.results_list = []

        # Table headers
        table_frame = ctk.CTkFrame(master, fg_color="white")
        table_frame.pack(fill="x", padx=10, pady=5)
        headers = ["item", "quantity", "unitcost", "cost", ""]
        for i, h in enumerate(headers):
            ctk.CTkLabel(table_frame, text=h, font=ctk.CTkFont(weight="bold"), fg_color="#CCC7C7", width=120 if h == "item" else 80).grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        # Dynamic sales rows
        self.rows_frame = ctk.CTkFrame(master, fg_color="white")
        self.rows_frame.pack(fill="x", padx=10)

        # Controls (clear list, make purchase)
        controls_frame = ctk.CTkFrame(master, fg_color="white")
        controls_frame.pack(fill="x", padx=10, pady=(5, 0))
        ctk.CTkButton(controls_frame, text="clear list", fg_color="#e15555", hover_color="#f10a0a", command=self.clear_all_rows).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(controls_frame, text="make purchase", fg_color="#3ea942", hover_color="#107e16", command=self.make_purchase).pack(side="right", padx=5, pady=5)

        # Total cost display
        total_frame = ctk.CTkFrame(master, fg_color="white")
        total_frame.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(total_frame, text="TOTAL COST", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=(0, 10))
        self.total_cost_label = ctk.CTkLabel(total_frame, text="0", font=ctk.CTkFont(size=28, weight="bold"), fg_color="#e5e5e5", width=120)
        self.total_cost_label.pack(side="right")

        # Receipt button
        ctk.CTkButton(master, text="receipt", fg_color="#bcbcbc", hover_color="#a0a0a0", command=self.print_receipt).pack(pady=5)

        self.update_search_results()

    def refresh_inventory(self):
        # Load inventory from database and store as list of dicts
        self.inventory_items = [
            {"id": row[0], "name": row[1], "quantity": row[2], "price": row[3], "unit_cost": row[4]}
            for row in get_inventory()
        ]

    def update_search_results(self, *args):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.results_list = []

        search_text = self.search_var.get().strip().lower()
        if not search_text:
            return

        for item in self.inventory_items:
            if search_text in item["name"].lower():
                btn = ctk.CTkButton(
                    self.results_frame, text=item["name"],
                    fg_color="#e5e5e5", text_color="black",
                    command=lambda i=item: self.add_sale_row(i)
                )
                btn.pack(side="left", padx=2, pady=2)
                self.results_list.append(btn)

    def add_sale_row(self, item):
        for row in self.sale_rows:
            if row["item_name"].get() == item["name"]:
                return

        row = {}
        row["item"] = item
        row["item_name"] = ctk.CTkEntry(self.rows_frame, fg_color="#e5e5e5", width=160)
        row["item_name"].insert(0, item["name"])
        row["item_name"].configure(state="readonly")
        row["quantity"] = ctk.CTkEntry(self.rows_frame, fg_color="#e5e5e5", width=80)
        row["quantity"].insert(0, "1")
        row["unitcost"] = ctk.CTkEntry(self.rows_frame, fg_color="#e5e5e5", width=80)
        row["unitcost"].insert(0, str(item.get("unit_cost", "")))
        row["cost"] = ctk.CTkLabel(self.rows_frame, text="", fg_color="#e5e5e5", width=80)
        row["remove"] = ctk.CTkButton(self.rows_frame, text="remove", fg_color="#ff6f6f", hover_color="#e05a5a", width=60, command=lambda r=row: self.remove_row(r))

        idx = len(self.sale_rows)
        row["item_name"].grid(row=idx, column=0, padx=2, pady=2, sticky="nsew")
        row["quantity"].grid(row=idx, column=1, padx=2, pady=2, sticky="nsew")
        row["unitcost"].grid(row=idx, column=2, padx=2, pady=2, sticky="nsew")
        row["cost"].grid(row=idx, column=3, padx=2, pady=2, sticky="nsew")
        row["remove"].grid(row=idx, column=4, padx=2, pady=2, sticky="nsew")

        row["quantity"].bind("<KeyRelease>", lambda e, r=row: self.update_row_cost(r))
        row["unitcost"].bind("<KeyRelease>", lambda e, r=row: self.update_row_cost(r))

        self.sale_rows.append(row)
        self.update_row_cost(row)

    def update_row_cost(self, row):
        try:
            qty = int(row["quantity"].get())
            unitcost = float(row["unitcost"].get())
            cost = qty * unitcost
            row["cost"].configure(text=str(int(cost)))
        except ValueError:
            row["cost"].configure(text="")
        self.update_total_cost()

    def update_total_cost(self):
        total = 0
        for row in self.sale_rows:
            try:
                cost = float(row["cost"].cget("text"))
                total += cost
            except ValueError:
                continue
        self.total_cost_label.configure(text=str(int(total)))

    def remove_row(self, row):
        for widget in row.values():
            if hasattr(widget, "grid_remove"):
                widget.grid_remove()
            elif hasattr(widget, "destroy"):
                widget.destroy()
        self.sale_rows.remove(row)
        for idx, r in enumerate(self.sale_rows):
            r["item_name"].grid(row=idx, column=0, padx=2, pady=2, sticky="nsew")
            r["quantity"].grid(row=idx, column=1, padx=2, pady=2, sticky="nsew")
            r["unitcost"].grid(row=idx, column=2, padx=2, pady=2, sticky="nsew")
            r["cost"].grid(row=idx, column=3, padx=2, pady=2, sticky="nsew")
            r["remove"].grid(row=idx, column=4, padx=2, pady=2, sticky="nsew")
        self.update_total_cost()

    def clear_all_rows(self):
        for row in self.sale_rows[:]:
            self.remove_row(row)
        self.update_total_cost()

    def make_purchase(self):
        sale = []
        for row in self.sale_rows:
            name = row["item_name"].get().strip()
            qty = row["quantity"].get().strip()
            unitcost = row["unitcost"].get().strip()
            item_ref = row["item"]
            if name and qty and unitcost:
                try:
                    qty = int(qty)
                    unitcost = float(unitcost)
                    cost = qty * unitcost
                    if qty > item_ref["quantity"]:
                        CTkMessagebox.messagebox("Stock Error", f"Not enough '{name}' in stock.")
                        return
                    # Update stock in DB
                    new_quantity = item_ref["quantity"] - qty
                    update_inventory_quantity(item_ref["id"], new_quantity)
                    sale.append({"description": name, "quantity": qty, "amount": cost})
                except ValueError:
                    continue
        if not sale:
            CTkMessagebox.messagebox("No items", "Please add at least one item to make a purchase.")
            return
        total = sum(item["amount"] for item in sale)
        record_sale(sale, total)
        self.clear_all_rows()
        self.total_cost_label.configure(text="0")
        CTkMessagebox.messagebox("Success", "Purchase completed!")
        self.refresh_inventory()  # Reload inventory from DB

    def print_receipt(self):
        sale_items = []
        for row in self.sale_rows:
            try:
                description = row["item_name"].get()
                quantity = int(row["quantity"].get())
                amount = float(row["cost"].cget("text"))
                sale_items.append({
                    "description": description,
                    "quantity": quantity,
                    "amount": amount
                })
            except Exception:
                continue

        receipt_text = receipt_generator.generate_receipt(sale_items)
        CTkMessagebox.messagebox("Receipt", receipt_text)
