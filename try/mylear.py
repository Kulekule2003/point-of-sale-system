import customtkinter as ctk

def button_callback():
    print("button clicked")

def love():
    print("i love you so much")

app = ctk.CTk()
app.geometry("400x150")

button = ctk.CTkButton(app, text="my button", command=button_callback)
button.pack(padx=20, pady=20)
button1 = ctk.CTkButton(app, text="love button", command=love )
button1.pack()

app.mainloop()