# sales_history.py

import customtkinter as ctk
import sqlite3
from sales.receipt_generator import generate_receipt

DB_NAME = "store.db"

class SalesHistoryPage:
    def __init__(self, master):
        self.master = master

        # Title
        title = ctk.CTkLabel(master, text="Sales History", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10)

        # Scrollable frame for receipts
        self.scroll_frame = ctk.CTkFrame(master)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Use a canvas and a frame for scrolling
        canvas = ctk.CTkCanvas(self.scroll_frame)
        scrollbar = ctk.CTkScrollbar(self.scroll_frame, orientation="vertical", command=canvas.yview)
        self.inner_frame = ctk.CTkFrame(canvas)

        self.inner_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.populate_receipts()

    def populate_receipts(self):
        sales = self.get_all_sales()
        if not sales:
            ctk.CTkLabel(self.inner_frame, text="No sales found.").pack(pady=20)
            return

        for sale in sales:
            sale_id, sale_date, total = sale
            # Header for each sale
            header = ctk.CTkFrame(self.inner_frame, fg_color="#f0f0f0")
            header.pack(fill="x", pady=5, padx=5)

            # Sale summary
            summary = f"Receipt #{sale_id} | Date: {sale_date} | Total: {total:.2f}"
            ctk.CTkLabel(header, text=summary, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)

            # View Receipt Button
            ctk.CTkButton(
                header,
                text="View Receipt",
                fg_color="#bcbcbc",
                hover_color="#a0a0a0",
                command=lambda sid=sale_id: self.show_receipt_popup(sid)
            ).pack(side="right", padx=10)

    def show_receipt_popup(self, sale_id):
        # Fetch sale items
        items = self.get_sale_items(sale_id)  # List of (item_name, quantity, amount)
        sale_items = [
            {"description": desc, "quantity": qty, "amount": amt}
            for desc, qty, amt in items
        ]
        receipt_text = generate_receipt(sale_items)

        # Popup window
        popup = ctk.CTkToplevel(self.master)
        popup.title(f"Receipt #{sale_id}")
        popup.geometry("400x400")

        text_box = ctk.CTkTextbox(popup, font=("Consolas", 10))
        text_box.insert("1.0", receipt_text)
        text_box.configure(state="disabled")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=5)

    def get_all_sales(self):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, sale_date, total FROM sales ORDER BY sale_date DESC")
            return cursor.fetchall()

    def get_sale_items(self, sale_id):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT item_name, quantity, amount FROM sale_items WHERE sale_id = ?",
                (sale_id,)
            )
            return cursor.fetchall()
