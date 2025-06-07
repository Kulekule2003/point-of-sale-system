import customtkinter as ctk
from sales import receipt_generator
from CustomTkinterMessagebox import CTkMessagebox
from database import update_inventory_quantity, record_sale, get_inventory
from PIL import Image

class HomeSalesDashboard:
    def __init__(self, master):
        self.master = master
        self.refresh_inventory()
        self.sale_rows = []

        # Color scheme for professional look
        self.colors = {
            'primary': '#2E86C1',      # Professional blue
            'secondary': '#F8F9FA',    # Light gray
            'success': '#28A745',      # Green
            'danger': '#DC3545',       # Red
            'warning': '#FFC107',      # Yellow
            'dark': '#343A40',         # Dark gray
            'light': '#E9ECEF',        # Very light gray
            'white': '#FFFFFF'
        }

        try:
            self.search_icon = ctk.CTkImage(light_image=Image.open("icons/search.png"), size=(20, 20))
        except:
            self.search_icon = None

        self.setup_ui()

    def setup_ui(self):
        # Main header with gradient-like effect
        header_frame = ctk.CTkFrame(self.master, fg_color=self.colors['primary'], corner_radius=0)
        header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.08)
        
        header_label = ctk.CTkLabel(
            header_frame, 
            text="SALES DASHBOARD", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['white']
        )
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        # Subtitle
        subtitle_frame = ctk.CTkFrame(self.master, fg_color=self.colors['secondary'], corner_radius=0)
        subtitle_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.04)
        
        subtitle = ctk.CTkLabel(
            subtitle_frame, 
            text="Point of Sale System", 
            font=ctk.CTkFont(size=14),
            text_color=self.colors['dark']
        )
        subtitle.place(relx=0.5, rely=0.5, anchor="center")

        # Enhanced search section
        search_container = ctk.CTkFrame(self.master, fg_color="transparent")
        search_container.place(relx=0.1, rely=0.14, relwidth=0.8, relheight=0.12)

        search_title = ctk.CTkLabel(
            search_container, 
            text="Search Inventory", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['dark']
        )
        search_title.place(relx=0.5, rely=0.1, anchor="center")

        # Professional search bar
        search_frame = ctk.CTkFrame(search_container, fg_color=self.colors['white'], corner_radius=25)
        search_frame.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.5)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_search_results)

        if self.search_icon:
            icon_label = ctk.CTkLabel(search_frame, image=self.search_icon, text="")
            icon_label.place(relx=0.02, rely=0.2, relwidth=0.08, relheight=0.6)
            entry_x = 0.12
        else:
            entry_x = 0.05

        self.search_entry = ctk.CTkEntry(
            search_frame, 
            textvariable=self.search_var, 
            placeholder_text="Type to search products...",
            text_color=self.colors['dark'], 
            font=ctk.CTkFont(size=14),
            fg_color=self.colors['light'],
            border_width=0,
            corner_radius=20
        )
        self.search_entry.place(relx=entry_x, rely=0.1, relwidth=0.88-entry_x, relheight=0.8)

        # Search results with better styling
        self.results_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        self.results_frame.place(relx=0.05, rely=0.27, relwidth=0.9, relheight=0.08)
        self.results_list = []

        # Professional table design
        table_container = ctk.CTkFrame(self.master, fg_color=self.colors['white'], corner_radius=15)
        table_container.place(relx=0.05, rely=0.36, relwidth=0.9, relheight=0.35)

        # Table header with better styling
        table_header = ctk.CTkFrame(table_container, fg_color=self.colors['primary'], corner_radius=10)
        table_header.place(relx=0.02, rely=0.05, relwidth=0.96, relheight=0.15)

        headers = [
            ("Product Name", 0.3),
            ("Quantity", 0.15),
            ("Unit Price", 0.15),
            ("Total Cost", 0.15),
            ("Action", 0.2)
        ]
        
        x_pos = 0.02
        for header, width in headers:
            ctk.CTkLabel(
                table_header, 
                text=header, 
                text_color=self.colors['white'], 
                font=ctk.CTkFont(size=14, weight="bold")
            ).place(relx=x_pos, rely=0.2, relwidth=width-0.01, relheight=0.6)
            x_pos += width

        # Scrollable rows area
        self.rows_frame = ctk.CTkScrollableFrame(
            table_container, 
            fg_color="transparent",
            corner_radius=10
        )
        self.rows_frame.place(relx=0.02, rely=0.22, relwidth=0.96, relheight=0.75)

        # Professional control buttons
        controls_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        controls_frame.place(relx=0.05, rely=0.73, relwidth=0.9, relheight=0.08)

        clear_btn = ctk.CTkButton(
            controls_frame, 
            text="🗑️ Clear All", 
            fg_color=self.colors['danger'], 
            hover_color="#B02A2A",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=25,
            command=self.clear_all_rows
        )
        clear_btn.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.8)

        purchase_btn = ctk.CTkButton(
            controls_frame, 
            text="💳 Complete Sale", 
            fg_color=self.colors['success'], 
            hover_color="#1E7E34",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=25,
            command=self.make_purchase
        )
        purchase_btn.place(relx=0.78, rely=0.1, relwidth=0.22, relheight=0.8)

        # Enhanced total display
        total_container = ctk.CTkFrame(self.master, fg_color=self.colors['white'], corner_radius=15)
        total_container.place(relx=0.05, rely=0.82, relwidth=0.9, relheight=0.1)

        total_bg = ctk.CTkFrame(total_container, fg_color=self.colors['primary'], corner_radius=10)
        total_bg.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.7)

        ctk.CTkLabel(
            total_bg, 
            text="TOTAL AMOUNT", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['white']
        ).place(relx=0.05, rely=0.2, relwidth=0.4, relheight=0.6)

        self.total_cost_label = ctk.CTkLabel(
            total_bg, 
            text="$0.00", 
            text_color=self.colors['white'], 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.total_cost_label.place(relx=0.55, rely=0.2, relwidth=0.4, relheight=0.6)

        # Professional receipt button
        receipt_btn = ctk.CTkButton(
            self.master, 
            text="🧾 Generate Receipt", 
            fg_color=self.colors['warning'], 
            hover_color="#D39E00",
            text_color=self.colors['dark'],
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=25,
            command=self.print_receipt
        )
        receipt_btn.place(relx=0.4, rely=0.94, relwidth=0.2, relheight=0.05)

        self.update_search_results()

    def refresh_inventory(self):
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

        matching = [item for item in self.inventory_items if search_text in item["name"].lower()]
        
        if not matching:
            no_results = ctk.CTkLabel(
                self.results_frame, 
                text="No products found",
                text_color=self.colors['dark'],
                font=ctk.CTkFont(size=12)
            )
            no_results.place(relx=0.5, rely=0.5, anchor="center")
            return

        btn_width = min(0.25, 1 / len(matching))
        for idx, item in enumerate(matching):
            btn = ctk.CTkButton(
                self.results_frame, 
                text=f"{item['name']}\n(Stock: {item['quantity']})",
                fg_color=self.colors['secondary'], 
                text_color=self.colors['dark'],
                hover_color=self.colors['light'],
                font=ctk.CTkFont(size=12),
                corner_radius=10,
                command=lambda i=item: self.add_sale_row(i)
            )
            btn.place(relx=idx*btn_width, rely=0, relwidth=btn_width-0.01, relheight=1)
            self.results_list.append(btn)

    def add_sale_row(self, item):
        # Check if item already exists
        for row in self.sale_rows:
            if row["item_name"].get() == item["name"]:
                CTkMessagebox(title="Duplicate Item", message="This item is already in your cart!")
                return

        row = {}
        idx = len(self.sale_rows)
        row["item"] = item

        # Create a frame for this row
        row_frame = ctk.CTkFrame(self.rows_frame, fg_color=self.colors['light'], corner_radius=8)
        row_frame.pack(fill="x", padx=5, pady=2)

        # Product name (readonly)
        row["item_name"] = ctk.CTkEntry(
            row_frame, 
            fg_color=self.colors['secondary'], 
            text_color=self.colors['dark'],
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        row["item_name"].place(relx=0.02, rely=0.1, relwidth=0.28, relheight=0.8)
        row["item_name"].configure(state="normal")
        row["item_name"].insert(0, item["name"])
        row["item_name"].configure(state="readonly")

        # Quantity input
        row["quantity"] = ctk.CTkEntry(
            row_frame, 
            fg_color=self.colors['white'], 
            text_color=self.colors['dark'],
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        row["quantity"].place(relx=0.32, rely=0.1, relwidth=0.13, relheight=0.8)
        row["quantity"].insert(0, "1")

        # Unit cost input
        row["unitcost"] = ctk.CTkEntry(
            row_frame, 
            fg_color=self.colors['white'], 
            text_color=self.colors['dark'],
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        row["unitcost"].place(relx=0.47, rely=0.1, relwidth=0.13, relheight=0.8)
        row["unitcost"].insert(0, f"{item.get('unit_cost', 0):.2f}")

        # Total cost display
        row["cost"] = ctk.CTkLabel(
            row_frame, 
            text="$0.00", 
            text_color=self.colors['dark'], 
            fg_color=self.colors['secondary'],
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=5
        )
        row["cost"].place(relx=0.62, rely=0.1, relwidth=0.13, relheight=0.8)

        # Remove button
        row["remove"] = ctk.CTkButton(
            row_frame, 
            text="Remove", 
            fg_color=self.colors['danger'], 
            hover_color="#B02A2A",
            font=ctk.CTkFont(size=11),
            corner_radius=15,
            command=lambda r=row, rf=row_frame: self.remove_row(r, rf)
        )
        row["remove"].place(relx=0.77, rely=0.1, relwidth=0.2, relheight=0.8)

        # Bind events for real-time calculation
        row["quantity"].bind("<KeyRelease>", lambda e, r=row: self.update_row_cost(r))
        row["unitcost"].bind("<KeyRelease>", lambda e, r=row: self.update_row_cost(r))

        row["frame"] = row_frame
        self.sale_rows.append(row)
        self.update_row_cost(row)

    def update_row_cost(self, row):
        try:
            qty = int(row["quantity"].get() or "0")
            unitcost = float(row["unitcost"].get() or "0")
            cost = qty * unitcost
            row["cost"].configure(text=f"${cost:.2f}")
        except ValueError:
            row["cost"].configure(text="$0.00")
        self.update_total_cost()

    def update_total_cost(self):
        total = 0
        for row in self.sale_rows:
            try:
                cost_text = row["cost"].cget("text").replace("$", "")
                cost = float(cost_text)
                total += cost
            except ValueError:
                continue
        self.total_cost_label.configure(text=f"${total:.2f}")

    def remove_row(self, row, row_frame):
        row_frame.destroy()
        self.sale_rows.remove(row)
        self.update_total_cost()

    def clear_all_rows(self):
        if not self.sale_rows:
            CTkMessagebox(title="Empty Cart", message="Your cart is already empty!")
            return
            
        for row in self.sale_rows[:]:
            row["frame"].destroy()
        self.sale_rows = []
        self.update_total_cost()
        CTkMessagebox(title="Cart Cleared", message="All items removed from cart!")

    def make_purchase(self):
        if not self.sale_rows:
            CTkMessagebox(title="Empty Cart", message="Please add items to your cart before making a purchase.")
            return

        sale = []
        for row in self.sale_rows:
            name = row["item_name"].get().strip()
            try:
                qty = int(row["quantity"].get().strip())
                unitcost = float(row["unitcost"].get().strip())
                cost = qty * unitcost
                item_ref = row["item"]
                
                if qty <= 0:
                    CTkMessagebox(title="Invalid Quantity", message=f"Please enter a valid quantity for '{name}'.")
                    return
                    
                if qty > item_ref["quantity"]:
                    CTkMessagebox(title="Insufficient Stock", 
                                message=f"Not enough '{name}' in stock.\nAvailable: {item_ref['quantity']}, Requested: {qty}")
                    return
                
                # Update stock in DB
                new_quantity = item_ref["quantity"] - qty
                update_inventory_quantity(item_ref["id"], new_quantity)
                sale.append({"description": name, "quantity": qty, "amount": cost})
                
            except ValueError:
                CTkMessagebox(title="Invalid Input", message=f"Please enter valid numbers for '{name}'.")
                return

        total = sum(item["amount"] for item in sale)
        record_sale(sale, total)
        
        # Clear the cart
        for row in self.sale_rows[:]:
            row["frame"].destroy()
        self.sale_rows = []
        self.total_cost_label.configure(text="$0.00")
        
        CTkMessagebox(title="Sale Completed", 
                     message=f"Purchase successful!\nTotal: ${total:.2f}\n\nInventory has been updated.")
        self.refresh_inventory()

    def print_receipt(self):
        if not self.sale_rows:
            CTkMessagebox(title="No Items", message="Please add items to generate a receipt.")
            return
            
        sale_items = []
        for row in self.sale_rows:
            try:
                description = row["item_name"].get()
                quantity = int(row["quantity"].get())
                cost_text = row["cost"].cget("text").replace("$", "")
                amount = float(cost_text)
                sale_items.append({
                    "description": description,
                    "quantity": quantity,
                    "amount": amount
                })
            except Exception:
                continue

        if sale_items:
            receipt_text = receipt_generator.generate_receipt(sale_items)
            CTkMessagebox(title="Receipt Preview", message=receipt_text)
        else:
            CTkMessagebox(title="Error", message="Unable to generate receipt. Please check your entries.")