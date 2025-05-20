# analytics.py
import customtkinter as ctk

class AnalyticsPage:
    def __init__(self, master):
        title = ctk.CTkLabel(master, text="This is the analytics dashboard")
        title.pack(pady=20)
