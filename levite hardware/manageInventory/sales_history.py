# sales_history.py
import customtkinter as ctk

class SalesHistoryPage:
    def __init__(self, master):
        title = ctk.CTkLabel(master, text="This is the sales history")
        title.pack(pady=20)
