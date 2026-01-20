import pandas as pd

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("Pokedex Tracker")
app.geometry("1280x720")

root = ctk.CTk()
root.wm_iconbitmap('')

label = ctk.CTkLabel(app, text="Welcome to Pokedex Tracker!")
label.pack(pady=20)

button = ctk.CTkButton(app, text="Close", command=app.destroy)
button.pack(pady=10)

app.mainloop()