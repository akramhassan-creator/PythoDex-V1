from _pyrepl.commands import clear_screen

import pandas as pd
import customtkinter as ctk
import matplotlib
from customtkinter import CTkImage
from PIL import Image
import pokebase as pb
import requests
from io import BytesIO
import threading

ctk.deactivate_automatic_dpi_awareness()

df = pd.read_csv('pokemondata.csv', sep=',', header=0)

print(df.to_string())

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Pokedex Tracker")
app.geometry("1280x800")
app.wm_iconbitmap('pokeball.ico')

progressbar = ctk.CTkProgressBar(app, orientation="horizontal")
progressbar.start()
progressbar.pack_forget()

my_font = ctk.CTkFont(family="<Helvetica>", size=20)
font = ctk.CTkFont(family="<Helvetica>", size=30)
afont = ctk.CTkFont(family="<Helvetica>", size=15)
tfont = ctk.CTkFont(family="<Helvetica>", size=20)
bold_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
pold_font = ctk.CTkFont(family="Helvetica", size=30, weight="bold")
statfont = ctk.CTkFont(family="Helvetica", size=15)

progressbar = ctk.CTkProgressBar(app, orientation="horizontal")

label = ctk.CTkLabel(app, font=tfont, text="Welcome to")
label.pack(pady=50)

poke_image = ctk.CTkImage(dark_image=Image.open("C:\\Users\\Learner\\PycharmProjects\\Pokedex-V1\\Pokedex_logo.png"),
                          size=(387, 140))

poke_label = ctk.CTkLabel(app, image=poke_image, text="")
poke_label.pack(pady=(20, 0))

close_button = ctk.CTkButton(
    app,
    text="Close",
    command=app.destroy,
    font=afont,
    fg_color="red",
    hover_color="darkred")
close_button.place(relx=0.85, rely=0.95, anchor="nw")

scrollable_frame = ctk.CTkScrollableFrame(app, width=500, height=500)
scrollable_frame.pack(side="left", padx=20, pady=20)


def clear_scrollable_frames():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()


def show_loading():
    clear_scrollable_frames()

    ctk.CTkLabel(app, text="Loading Pokemon...",
                 font=bold_font,
                 ).pack(pady=(20, 0))

    progressbar.pack_forget()
    progressbar.start()


def hide_loading():
    progressbar.stop()
    progressbar.pack_forget()


def show_pokemon_threaded(p):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    show_loading()

    def task():
        show_pokemon(p)
        app.after(0, hide_loading)

    threading.Thread(target=task).start()


def show_pokemon(p):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(scrollable_frame, font=pold_font, text=p['Name']).pack()

    pokemon_name = p['Name'].lower()
    pokemon = pb.pokemon(pokemon_name)

    sprite_url = pokemon.sprites.front_default

    if pd.notna(p['Type 2']):
        type2_text = p['Type 2']
    else:
        type2_text = "Not Applicable"

    if sprite_url:
        response = requests.get(sprite_url)
        image_data = Image.open(BytesIO(response.content))

        sprite_image = ctk.CTkImage(
            dark_image=image_data,
            size=(150, 150)
        )

        sprite_label = ctk.CTkLabel(
            scrollable_frame,
            image=sprite_image,
            text=""
        )
        sprite_label.image = sprite_image
        sprite_label.pack(pady=10)
    else:
        ctk.CTkLabel(scrollable_frame, text="No Sprite Found").pack()
        ctk.CTkLabel(scrollable_frame, text="No Sprite Found").pack()

    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Type 1: {p['Type 1']}").pack()
    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Type 2: {type2_text}").pack()
    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Legendary: {p['Legendary']}").pack(pady=3)
    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Generation: {int(p['Generation'])}").pack(pady=3)

    ctk.CTkLabel(scrollable_frame, font=bold_font, text="Base Stats").pack(pady=15, padx=5)

    stats = [
        ("HP", int(p['HP'])),
        ("Attack", int(p['Attack'])),
        ("Defense", int(p['Defense'])),
        ("Sp. Atk", int(p['Sp. Atk'])),
        ("Sp. Def", int(p['Sp. Def'])),
        ("Speed", int(p['Speed']))
    ]

    for stat_name, stat_value in stats:
        stat_frame = ctk.CTkFrame(scrollable_frame)
        stat_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(stat_frame, text=f"{stat_name}:", font=statfont).pack(side="left")
        ctk.CTkLabel(stat_frame, text=str(stat_value), font=statfont).pack(side="right")


def button_click_event():
    dialog = ctk.CTkInputDialog(text="Enter Pokemon name:")
    name = dialog.get_input()

    if not name:
        return

    result = df[df['Name'].str.lower() == name.lower()]

    if result.empty:
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(scrollable_frame, text="No Sprite Found", text_color="red").pack()
        return

    show_pokemon_threaded(result.iloc[0])


button = ctk.CTkButton(app, text="Search 🔍", command=button_click_event)
button.pack(padx=20, pady=20)
button.place(relx=0.02, rely=0.37, anchor="sw")


def optionmenu_callback(choice=None):
    if choice is None:
        choice = optionmenu.get()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if choice == "All":
        filtered_df = df
    else:
        filtered_df = df[(df['Type 1'] == choice) | (df['Type 2'] == choice)]

    ctk.CTkLabel(scrollable_frame, text=f"{choice} Type({len(filtered_df)} Pokemon)", font=bold_font).pack(pady=20)

    for idx, row in filtered_df.head(15).iterrows():
        ctk.CTkButton(
            scrollable_frame,
            text=f"{row['Name']}",
            command=lambda p=row: show_pokemon(p),
            width=300
        ).pack(pady=20)


optionmenu = ctk.CTkOptionMenu(app, values=["All", "Fire", "Water", "Grass", "Normal", "Electric", "Ice", "Fighting",
                                            "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon",
                                            "Dark", "Steel", "Fairy"], command=optionmenu_callback)
optionmenu.set("All")
optionmenu.pack(padx=20, pady=20)
optionmenu.place(relx=0.14, rely=0.37, anchor="sw")

app.mainloop()
