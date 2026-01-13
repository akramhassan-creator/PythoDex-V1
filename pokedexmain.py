import PIL.Image
import pandas as pd
import customtkinter as ctk
import matplotlib
from customtkinter import CTkImage
from fontTools.misc.cython import returns
from PIL import Image

df = pd.read_csv('pokemondata.csv', sep=',', header=0)

print(df.to_string())

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Pokedex Tracker")
app.geometry("1280x720")
app.wm_iconbitmap('pokeball.ico')

my_font = ctk.CTkFont(family="<Helvetica>", size=20)
font = ctk.CTkFont(family="<Helvetica>", size=30)
afont = ctk.CTkFont(family="<Helvetica>", size=15)

label = ctk.CTkLabel(app, font=font, text="Welcome to Pokedex Tracker! 🙊")
label.pack(pady=50)

label2 = ctk.CTkLabel(app, font=afont, text="Enter your Pokemon Name:")
label2.pack(pady=20)

close_button = ctk.CTkButton(app, font=my_font, text="Close", command=app.destroy)
close_button.place(relx=0.85, rely=0.95, anchor="nw")

def clear_scrollable_frames():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def button_click_event():
    dialog = ctk.CTkInputDialog(text="Type the name of the pokemon to track:")
    name = dialog.get_input()

    if not name:
         return

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    image_label.place_forget()

    result = df[df['Name'].str.lower() == name.lower()]

    if result.empty:
        ctk.CTkLabel(scrollable_frame, text="No Pokemon Found").pack()
        return

    p = result.iloc[0]

    sprite_path = f"pokemon sprites/{p['Name'].lower()}.png"

    try:
        image = ctk.CTkImage(
            dark_image=Image.open(sprite_path),
            size=(100, 100),
        )

        image_label.configure(image=image, text="")
        image_label.image = image
        image_label.pack(padx=2, pady=2)

    except FileNotFoundError:
        image_label.configure(text="Image not found", image="")



    ctk.CTkLabel(scrollable_frame, text=p['Name']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Type 1']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Type 2']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['HP']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Defense']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Sp. Atk']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Sp. Def']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Speed']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Generation']).pack()
    ctk.CTkLabel(scrollable_frame, text=p['Legendary']).pack()


button = ctk.CTkButton(app, text="Search 🔍", command=button_click_event)
button.pack(padx=20, pady=20)

scrollable_frame = ctk.CTkScrollableFrame(app, width=300, height=300)
scrollable_frame.pack(padx=20, pady=20)


image = ctk.CTkImage(dark_image=Image.open("C:\\Users\\Learner\\PycharmProjects\\Pokedex-V1\\pokemon sprites\\pikachu.png"),
size=(500, 500))

image_label = ctk.CTkLabel(app, text="")
image_label.pack(padx=20, pady=20)

app.mainloop()
