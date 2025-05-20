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

        self.create_sidebar_buttons()
        self.show_dashboard("Home")

    def create_sidebar_buttons(self):
        # Regular dashboard buttons
        dashboards = ["Home"]
        for name in dashboards:
            btn = ctk.CTkButton(self.sidebar, text=name, command= self.sales_dashboard())
            btn.pack(pady=5, fill="x")

        # Inventory (expandable)
        self.inventory_btn = ctk.CTkButton(
            self.sidebar, text="Manage Inventory ▸", command=self.toggle_inventory_submenu
        )
        self.inventory_btn.pack(pady=(20, 5), fill="x")

        # Submenu buttons (hidden by default)
        self.inventory_submenu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.inventory_buttons = []

        """
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
        """
        item_list_btn = ctk.CTkButton(self.inventory_submenu_frame,
                text="",
                command= self.add_item(),
                height= 30,
                fg_color= "transparent",
                anchor="w")
        item_list_btn.pack(fill="x", padx=10)
        """
        analytics_btn = ctk.CTkButton(self.inventory_submenu_frame,
                text="",
                command= self.show_analytics(),
                height= 30,
                fg_color= "transparent",
                anchor="w")
        analytics_btn.pack(fill="x", padx=10)
        
        Sales_his_btn = ctk.CTkButton(self.inventory_submenu_frame,
                text="",
                command= self.show_dashboard(n),
                height= 30,
                fg_color= "transparent",
                anchor="w")
        Sales_his_btn.pack(fill="x", padx=10)
    """
    def toggle_inventory_submenu(self):
        self.inventory_expanded = not self.inventory_expanded
        if self.inventory_expanded:
            self.inventory_btn.configure(text="Manage Inventory ▼")
            self.inventory_submenu_frame.pack(fill="x")
        else:
            self.inventory_btn.configure(text="Manage Inventory ▸")
            self.inventory_submenu_frame.forget()

    def show_dashboard(self, name):
        # Clear current widgets
        for widget in self.main_content.winfo_children():
            widget.destroy()
        #display selected dashboard 


        # Display selected dashboard
        title = ctk.CTkLabel(self.main_content, text=f"{name} Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        description = ctk.CTkLabel(self.main_content, text=f"You're now viewing the {name.lower()} section of the app.")
        description.pack(pady=10)

    def add_item(self):
        self.item_name = ctk.CTkEntry(self.main_content, text = "item name")
        self.item_quantity = ctk.CTkEntry(self.main_content, text = "item quantity")

    def 

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
