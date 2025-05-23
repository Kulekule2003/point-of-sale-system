import customtkinter as ctk
from dashboard_app import DashboardApp

from database import create_tables

create_tables()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = DashboardApp()
    app.mainloop()
