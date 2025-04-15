import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x150")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callbck)
        self.button.pack(padx=20, pady=20)

    def button_callbck(self):
        print("button clicked")
    
    def create_ui(self):
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill='y')

        self.sell_btn = ctk.CTkButton(self.sidebar, text="sell", fg_color="#d3d3d3", text_color="black",command=self.show_sell)
        self.sell_btn.pack(pady=10, fill="x")

        self.manage_inv_btn = ctk.CTkButton(self.sidebar, text="manage inventory", fg_color="#d3d3d3", text_color="black", command=self.show_inventory)
        self.manage_inv_btn.pack(pady=10, fill="x")

        self.admin_btn = ctk.CTkButton(self.sidebar, text="Admin",fg_color="#d3d3d3", text_color="black", command=self.login )
        self.admin_btn.pack(pady=10, fill="x")

app = App()
app.mainloop()