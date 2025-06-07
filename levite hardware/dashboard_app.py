import customtkinter as ctk

from sidebar import Sidebar
from manageInventory.item_list import ItemListPage
from manageInventory.analytics import AnalyticsPage
from manageInventory.sales_history import SalesHistoryPage
from sales.home_sales_dashboard import HomeSalesDashboard

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Levite Hardware")
        self.geometry("900x600")

        # Sidebar (left 18% of window)
        self.sidebar = Sidebar(self, self.show_dashboard)
        self.sidebar.place(relx=0, rely=0, relwidth=0.18, relheight=1)

        # Main content area (right 82% of window, with padding)
        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        # 2% padding left/right, 2% top, 2% bottom
        self.main_content.place(relx=0.20, rely=0.03, relwidth=0.78, relheight=0.94)

        self.show_dashboard("Home")

    def show_dashboard(self, name):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        if name == "Home":
            HomeSalesDashboard(self.main_content)
        elif name == "Item List":
            ItemListPage(self.main_content)
        elif name == "analytics":
            AnalyticsPage(self.main_content)
        elif name == "Sales History":
            SalesHistoryPage(self.main_content)
