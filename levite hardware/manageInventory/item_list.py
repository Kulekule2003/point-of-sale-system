import customtkinter as ctk
from database import add_inventory_item, get_inventory
import tkinter.messagebox as messagebox

class ItemListPage:
    def __init__(self, master):
        self.master = master
        
        # Configure master window
        self.master.configure(fg_color=("#f0f0f0", "#1a1a1a"))
        
        # Create scrollable frame as main container
        self.scrollable_frame = ctk.CTkScrollableFrame(
            master, 
            corner_radius=0, 
            fg_color="transparent",
            scrollbar_fg_color=("#bdc3c7", "#34495e"),
            scrollbar_button_color=("#3498db", "#2980b9"),
            scrollbar_button_hover_color=("#2980b9", "#3498db")
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create main container frame inside scrollable frame
        self.main_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create header
        self.create_header()
        
        # Create input section
        self.create_input_section()
        
        # Create search section
        self.create_search_section()
        
        # Create inventory display section
        self.create_inventory_section()
        
        # Initialize data
        self.update_item_list()

    def create_header(self):
        """Create professional header section"""
        header_frame = ctk.CTkFrame(self.main_frame, height=80, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Header title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📦 Inventory Management System",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2c3e50", "#ecf0f1")
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Manage your inventory items efficiently",
            font=ctk.CTkFont(size=14),
            text_color=("#7f8c8d", "#bdc3c7")
        )
        subtitle_label.pack(pady=(0, 10))

    def create_input_section(self):
        """Create professional input form section"""
        input_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        input_frame.pack(fill="x", pady=(0, 20))
        
        # Section title
        section_title = ctk.CTkLabel(
            input_frame,
            text="➕ Add New Item",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#2980b9", "#3498db")
        )
        section_title.pack(pady=(20, 15))
        
        # Create form grid
        form_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Configure grid
        form_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Input fields data
        fields = [
            ("Item Name", "Enter item name"),
            ("Quantity", "Enter quantity"),
            ("Total Price ($)", "0.00"),
            ("Unit Cost ($)", "0.00")
        ]
        
        self.entries = []
        
        for i, (label_text, placeholder) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            # Create field container
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.grid(row=row, column=col, padx=15, pady=10, sticky="ew")
            
            # Label
            label = ctk.CTkLabel(
                field_frame,
                text=label_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#34495e", "#ecf0f1"),
                anchor="w"
            )
            label.pack(fill="x", pady=(0, 5))
            
            # Entry
            entry = ctk.CTkEntry(
                field_frame,
                placeholder_text=placeholder,
                font=ctk.CTkFont(size=13),
                height=40,
                corner_radius=10,
                border_width=2,
                border_color=("#bdc3c7", "#34495e")
            )
            entry.pack(fill="x")
            self.entries.append(entry)
        
        # Assign entries to specific variables
        self.item_name, self.item_quantity, self.item_price, self.item_unit_cost = self.entries
        
        # Add auto-calculation for unit cost
        self.item_price.bind("<KeyRelease>", self.calculate_unit_cost)
        self.item_quantity.bind("<KeyRelease>", self.calculate_unit_cost)
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Buttons with improved styling
        self.add_button = ctk.CTkButton(
            button_frame,
            text="📦 Add Item",
            command=self.add_Item,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=("#27ae60", "#2ecc71"),
            hover_color=("#229954", "#58d68d")
        )
        self.add_button.pack(side="left", padx=(0, 15), fill="x", expand=True)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="🔄 Clear Form",
            command=self.clear_inputs,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color=("#95a5a6", "#7f8c8d"),
            hover_color=("#7f8c8d", "#95a5a6")
        )
        self.clear_button.pack(side="right", padx=(15, 0), fill="x", expand=True)
        
        # Status message label
        self.message_label = ctk.CTkLabel(
            input_frame,
            text="",
            font=ctk.CTkFont(size=12),
            height=25
        )
        self.message_label.pack(pady=(0, 15))

    def create_search_section(self):
        """Create search section"""
        search_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        search_frame.pack(fill="x", pady=(0, 20))
        
        # Search title
        search_title = ctk.CTkLabel(
            search_frame,
            text="🔍 Search Inventory",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#8e44ad", "#9b59b6")
        )
        search_title.pack(pady=(20, 10))
        
        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.update_item_list)
        
        search_container = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_container.pack(fill="x", padx=30, pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="🔍 Type to search items...",
            textvariable=self.search_var,
            font=ctk.CTkFont(size=14),
            height=45,
            corner_radius=12,
            border_width=2,
            border_color=("#9b59b6", "#8e44ad")
        )
        self.search_entry.pack(fill="x")

    def create_inventory_section(self):
        """Create inventory display section"""
        inventory_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, height=400)
        inventory_frame.pack(fill="x", pady=(0, 20))
        inventory_frame.pack_propagate(False)  # Maintain fixed height
        
        # Inventory title with stats
        title_frame = ctk.CTkFrame(inventory_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        inventory_title = ctk.CTkLabel(
            title_frame,
            text="📊 Current Inventory",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#e67e22", "#f39c12")
        )
        inventory_title.pack(side="left")
        
        self.stats_label = ctk.CTkLabel(
            title_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("#7f8c8d", "#bdc3c7")
        )
        self.stats_label.pack(side="right")
        
        # Inventory display with improved styling
        display_frame = ctk.CTkFrame(inventory_frame, fg_color="transparent")
        display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.item_listbox = ctk.CTkTextbox(
            display_frame,
            font=ctk.CTkFont(size=12, family="Consolas"),
            corner_radius=12,
            border_width=2,
            border_color=("#bdc3c7", "#34495e"),
            scrollbar_button_color=("#3498db", "#2980b9"),
            scrollbar_button_hover_color=("#2980b9", "#3498db")
        )
        self.item_listbox.pack(fill="both", expand=True)

    def calculate_unit_cost(self, event=None):
        """Auto-calculate unit cost based on price and quantity"""
        try:
            price = float(self.item_price.get() or 0)
            quantity = float(self.item_quantity.get() or 0)
            
            if quantity > 0:
                unit_cost = price / quantity
                self.item_unit_cost.delete(0, ctk.END)
                self.item_unit_cost.insert(0, f"{unit_cost:.2f}")
        except (ValueError, ZeroDivisionError):
            pass

    def add_Item(self):
        """Add item with improved validation and feedback"""
        name = self.item_name.get().strip()
        quantity = self.item_quantity.get().strip()
        price = self.item_price.get().strip()
        unit_cost = self.item_unit_cost.get().strip()

        # Validation
        if not all([name, quantity, price, unit_cost]):
            self.show_message("⚠️ Please fill in all fields", "error")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            unit_cost = float(unit_cost)
            
            if quantity <= 0 or price < 0 or unit_cost < 0:
                self.show_message("⚠️ Please enter valid positive numbers", "error")
                return
                
        except ValueError:
            self.show_message("⚠️ Please enter valid numbers for quantity, price, and unit cost", "error")
            return

        try:
            add_inventory_item(name, quantity, price, unit_cost)
            self.show_message(f"✅ Item '{name}' added successfully!", "success")
            self.clear_inputs()
            self.update_item_list()
        except Exception as e:
            self.show_message(f"❌ Error adding item: {str(e)}", "error")

    def show_message(self, message, msg_type="info"):
        """Show status message with appropriate color"""
        colors = {
            "success": ("#27ae60", "#2ecc71"),
            "error": ("#e74c3c", "#ec7063"),
            "info": ("#3498db", "#5dade2")
        }
        
        color = colors.get(msg_type, colors["info"])
        self.message_label.configure(text=message, text_color=color)
        
        # Clear message after 3 seconds
        self.master.after(3000, lambda: self.message_label.configure(text=""))

    def clear_inputs(self):
        """Clear all input fields"""
        for entry in self.entries:
            entry.delete(0, ctk.END)
        self.item_name.focus()

    def update_item_list(self, *args):
        """Update item list with improved formatting and statistics"""
        search_text = self.search_var.get().lower()
        self.item_listbox.delete("1.0", ctk.END)
        
        try:
            items = get_inventory()
            filtered_items = []
            total_value = 0
            
            # Header
            header = f"{'=' * 80}\n"
            header += f"{'ITEM NAME':<25} {'QTY':<8} {'PRICE':<12} {'UNIT COST':<12} {'TOTAL':<12}\n"
            header += f"{'=' * 80}\n"
            self.item_listbox.insert(ctk.END, header)
            
            for item in items:
                # item = (id, name, quantity, price, unit_cost)
                if search_text in item[1].lower():
                    filtered_items.append(item)
                    item_total = item[2] * item[4]  # quantity * unit_cost
                    total_value += item_total
                    
                    # Format item display
                    item_line = (
                        f"{item[1]:<25} "
                        f"{item[2]:<8} "
                        f"${item[3]:<11.2f} "
                        f"${item[4]:<11.2f} "
                        f"${item_total:<11.2f}\n"
                    )
                    self.item_listbox.insert(ctk.END, item_line)
            
            # Footer with statistics
            if filtered_items:
                footer = f"\n{'=' * 80}\n"
                footer += f"📊 SUMMARY: {len(filtered_items)} items found | Total Value: ${total_value:.2f}\n"
                footer += f"{'=' * 80}"
                self.item_listbox.insert(ctk.END, footer)
                
                # Update stats label
                self.stats_label.configure(text=f"Items: {len(filtered_items)} | Value: ${total_value:.2f}")
            else:
                if search_text:
                    self.item_listbox.insert(ctk.END, f"\n🔍 No items found matching '{search_text}'\n")
                else:
                    self.item_listbox.insert(ctk.END, f"\n📦 No items in inventory yet\n")
                self.stats_label.configure(text="Items: 0 | Value: $0.00")
                
        except Exception as e:
            self.item_listbox.insert(ctk.END, f"❌ Error loading inventory: {str(e)}")
            self.stats_label.configure(text="Error loading data")


# Example usage (if running as standalone)
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # or "light"
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Professional Inventory Management")
    root.geometry("1000x800")
    root.minsize(800, 600)
    
    app = ItemListPage(root)
    root.mainloop()