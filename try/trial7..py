import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DashboardApp(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Levite Hardware")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20)

        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_title.pack(pady = 20)

        self.inventory_expanded = False #track toggle state

    def side_bar_buttons(self):

        home_btn = ctk.CTkButton(self.sidebar, text="Home")
        manage_inventory_btn = ctk.CTkButton(self.sidebar, text="Manage Inventory")
        item_list_btn = ctk.CTkButton()
        analytics_btn = ctk.CTkButton()
        sales_btn = ctk.CTkButton()