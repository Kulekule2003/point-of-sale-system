import customtkinter as ctk
from PIL import Image

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, show_dashboard_callback):
        super().__init__(master, width=200, corner_radius=0)
        self.place(relx=0, rely=0, relwidth=0.18, relheight=1)  # Sidebar occupies left 18% of window

        #self.home_icon = ctk.CTkImage(light_image=Image.open(".\icons\home_button.png"), size=(24,24))
        self.show_dashboard_callback = show_dashboard_callback

        #self.manage_icon = ctk.CTkImage(light_image=Image.open(".\icons\manageInventory.png"), size=(24,24))

        # Title
        self.title = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        self.title.place(relx=0, rely=0.02, relwidth=1, relheight=0.07)

        # Regular dashboard buttons
        dashboards = ["Home"]
        self.dashboard_buttons = []
        for i, name in enumerate(dashboards):
            btn = ctk.CTkButton(
                self,
                text=name,
                command=lambda n=name: self.show_dashboard_callback(n),
                #image=self.home_icon, compound="left"
            )
            btn.place(relx=0.05, rely=0.12 + i * 0.08, relwidth=0.9, relheight=0.07)

            self.dashboard_buttons.append(btn)

        # Inventory (expandable)
        self.inventory_expanded = False
        self.inventory_btn = ctk.CTkButton(
            self,
            text="Manage Inventory ▸",
            command=self.toggle_inventory_submenu,
            #image=self.manage_icon,
            compound="left"
        )
        self.inventory_btn.place(relx=0.05, rely=0.22, relwidth=0.9, relheight=0.07)

        # Submenu frame (initially hidden)
        self.inventory_submenu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.submenu_items = ["Item List", "analytics", "Sales History"]
        self.inventory_buttons = []
        for i, item in enumerate(self.submenu_items):
            btn = ctk.CTkButton(
                self.inventory_submenu_frame,
                text=f" • {item}",
                command=lambda n=item: self.show_dashboard_callback(n),
                fg_color="transparent",
                anchor="w",
                text_color="black"
            )
            btn.place(relx=0.05, rely=i * 0.25, relwidth=0.9, relheight=0.22)
            self.inventory_buttons.append(btn)

    def toggle_inventory_submenu(self):
        self.inventory_expanded = not self.inventory_expanded
        if self.inventory_expanded:
            self.inventory_btn.configure(text="Manage Inventory ▼")
            self.inventory_submenu_frame.place(relx=0, rely=0.30, relwidth=1, relheight=0.20)
        else:
            self.inventory_btn.configure(text="Manage Inventory ▸")
            self.inventory_submenu_frame.place_forget()
