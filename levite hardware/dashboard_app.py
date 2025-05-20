import customtkinter as ctk
from sidebar import Sidebar
from manageInventory.item_list import ItemListPage
from manageInventory.analytics import AnalyticsPage
from manageInventory.sales_history import SalesHistoryPage

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Levite Hardware")
        self.geometry("900x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.items = []

        # Sidebar
        self.sidebar = Sidebar(self, self.show_dashboard)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main content area
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        self.show_dashboard("Home")

    def show_dashboard(self, name):
        for widget in self.main_content.winfo_children():
            widget.destroy()

        if name == "Home":
            label = ctk.CTkLabel(self.main_content, text="This is the home dashboard")
            label.pack(pady=20)
        elif name == "Item List":
            ItemListPage(self.main_content, self.items)
        elif name == "analytics":
            AnalyticsPage(self.main_content)
        elif name == "Sales History":
            SalesHistoryPage(self.main_content)

