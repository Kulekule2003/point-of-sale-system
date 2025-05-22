import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, show_dashboard_callback):
        super().__init__(master, width=200, corner_radius=0)
        self.grid_propagate(False)
        self.show_dashboard_callback = show_dashboard_callback

        title = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20)

        # Regular dashboard buttons
        dashboards = ["Home"]
        for name in dashboards:
            btn = ctk.CTkButton(self,text=name, command=lambda n=name: self.show_dashboard_callback(n), height=40)
            btn.pack(pady=5, fill="x")

        # Inventory (expandable)
        self.inventory_expanded = False
        self.inventory_btn = ctk.CTkButton(
            self, text="Manage Inventory ▸", command=self.toggle_inventory_submenu, height=40
        )
        self.inventory_btn.pack(pady=(20, 5), fill="x")

        self.inventory_submenu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inventory_buttons = []

        submenu_items = ["Item List", "analytics", "Sales History"]
        for item in submenu_items:
            btn = ctk.CTkButton(
                self.inventory_submenu_frame,
                text=f"  • {item}",
                command=lambda n=item: self.show_dashboard_callback(n),
                height=40,
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
