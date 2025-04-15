import customtkinter as ctk


class InventoryView(ctk.CTkFrame):
    def __init__(self, master, item_list, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.item_list = item_list
        self.configure(fg_color="white")

        self.build_ui()

    def build_ui(self):
        # Top stats
        stats_frame = ctk.CTkFrame(self, fg_color="white")
        stats_frame.pack(fill="x", padx=20, pady=10)

        total_items = len(self.item_list.item_list)
        restock_items = len([v for v in self.item_list.item_list.values() if v['quantity'] <= 5])

        self.total_items_box = self._stat_box(stats_frame, "total unique items", total_items)
        self.total_items_box.pack(side="left", padx=20)

        self.restock_items_box = self._stat_box(stats_frame, "items for restocking", restock_items)
        self.restock_items_box.pack(side="left", padx=20)

        # Restocking section
        ctk.CTkLabel(self, text="items for restocking", anchor="w", text_color="black").pack(fill="x", padx=20)
        restock_search_frame = ctk.CTkFrame(self, fg_color="white")
        restock_search_frame.pack(fill="x", padx=20)
        ctk.CTkEntry(restock_search_frame, placeholder_text="search", fg_color="#d9d9d9").pack(side="right")

        self.restock_list_frame = ctk.CTkFrame(self, fg_color="white")
        self.restock_list_frame.pack(fill="x", padx=20, pady=5)

        # Available items section
        ctk.CTkLabel(self, text="Available items", anchor="w", text_color="black").pack(fill="x", padx=20, pady=(20, 0))
        avail_search_frame = ctk.CTkFrame(self, fg_color="white")
        avail_search_frame.pack(fill="x", padx=20)
        ctk.CTkEntry(avail_search_frame, placeholder_text="search", fg_color="#d9d9d9").pack(side="right")

        self.avail_list_frame = ctk.CTkFrame(self, fg_color="white")
        self.avail_list_frame.pack(fill="x", padx=20, pady=5)

        self.refresh_lists()

    def _stat_box(self, master, title, number):
        frame = ctk.CTkFrame(master, width=150, height=100, corner_radius=10, fg_color="#d9d9d9")
        frame.pack_propagate(False)
        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=12, weight="bold")).pack()
        ctk.CTkLabel(frame, text=str(number), font=ctk.CTkFont(size=32, weight="bold")).pack()
        return frame

    def refresh_lists(self):
        for widget in self.restock_list_frame.winfo_children():
            widget.destroy()
        for widget in self.avail_list_frame.winfo_children():
            widget.destroy()

        for name, info in self.item_list.item_list.items():
            label = ctk.CTkLabel(self.avail_list_frame, text=f"{name} - Qty: {info['quantity']}", fg_color="#d9d9d9", anchor="w")
            label.pack(fill="x", pady=2)

            if info['quantity'] <= 5:
                restock_label = ctk.CTkLabel(self.restock_list_frame, text=f"{name} - Qty: {info['quantity']}", fg_color="#d9d9d9", anchor="w")
                restock_label.pack(fill="x", pady=2)
    