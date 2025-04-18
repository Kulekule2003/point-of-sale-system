import customtkinter as ctk

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter Dashboard")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Main content area
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Sidebar title
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_title.pack(pady=20)

        # Sidebar buttons
        self.create_sidebar_buttons()

        self.inventory_expanded = False
        # Show default page
        self.show_dashboard("Home")

    def create_sidebar_buttons(self):
        dashboards = ["Home", "Sales","Reports", "Settings"]
        for name in dashboards:
            btn = ctk.CTkButton(
                self.sidebar,
                text=name,
                command=lambda n=name: self.show_dashboard(n),
                corner_radius=5,
                width=180
            )
            btn.pack(pady=5)

        #inventory expandable
        self.inventory_btn = ctk.CTkButton(
            self.sidebar, text="Manage inventory ▸", command=self.toggle_inventory_submenu
        )

        self.inventory_btn.pack(pady=(20,5), fill="x")

        #sub menu buttons hidden by default
        self.inventory_submeu_fram = ctk.CTkFrame(self.sidebar, fg_color ="transparent")
        self.inventory_btn = []

        submenu_items = ["item list", "analytics","sales history"]
        for item in submenu_items:
            btn = ctk.CTkButton(self.inventory_submeu_fram,
                                text=f" . {item}",
                                command= lambda n = item: self.show_dashboard(n),
                                height=30,
                                fg_color="transparent",
                                anchor="w"
                                )
            btn.pack(fill="x", padx=10)
            self.invetory_buttons.append(btn)
    def toggle_inventory_submenu(self, name):
        self.inventory_expanded = not self.inventory_expanded
        if self.inventory_expanded:
            self.inventory_btn.configure(text = "Manage inventory ▼")
            self.inventory_submeu_fram.pack(fill = "x")
        else:
            self.inventory_btn.configure(text="Manage inventory ▸")
            self.inventory_submeu_fram.forget()

    def show_dashboard(self, name):
        # Clear current widgets
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Display selected dashboard
        title = ctk.CTkLabel(self.main_content, text=f"{name} Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        description = ctk.CTkLabel(self.main_content, text=f"You're now viewing the {name.lower()} section of the app.")
        description.pack(pady=10)

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
