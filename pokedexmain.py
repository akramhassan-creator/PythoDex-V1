import PIL.Image
import pandas as pd
import customtkinter as ctk
import matplotlib
from customtkinter import CTkImage
from fontTools.misc.cython import returns
from PIL import Image


ctk.deactivate_automatic_dpi_awareness()

df = pd.read_csv('pokemondata.csv', sep=',', header=0)

print(df.to_string())

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Pokedex Tracker")
app.geometry("1280x800")
app.wm_iconbitmap('pokeball.ico')

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

poke_image = ctk.CTkImage(dark_image=Image.open("C:\\Users\\akybo\\PycharmProjects\\Pokedex-V1\\Pokedex_logo.png"),
size=(387, 140))

poke_label = ctk.CTkLabel(app, image=poke_image, text="")
poke_label.pack(pady=(20, 0))
label.pack(pady=(5, 10))


close_button = ctk.CTkButton(
            app,
            text="Close",
            command=app.destroy,
            font=afont,
            fg_color="red",
            hover_color="darkred")
close_button.place(relx=0.85, rely=0.95, anchor="nw")

scrollable_frame = ctk.CTkScrollableFrame(app, width=500, height=500)
scrollable_frame.pack(side= "left", padx=20, pady=20)


def clear_scrollable_frames():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def show_pokemon(p):
    for widget in scrollable_frame.winfo_children():
           widget.destroy()

    ctk.CTkLabel(scrollable_frame, font=pold_font, text=p['Name']).pack()

    sprite_image = ctk.CTkImage(
        dark_image=Image.open("C:\\Users\\akybo\\PycharmProjects\\Pokedex-V1\\pokemon sprites\\pikachu.png"),
        size=(500, 500))

    sprite_path = f"pokemon sprites/{p['Name'].lower()}.png"

    try:
        sprite_image = ctk.CTkImage(
            dark_image=Image.open(sprite_path),
            size=(150, 150),

        )
        sprite_label = ctk.CTkLabel(scrollable_frame, image=sprite_image, text="", compound="center")
        sprite_label.image = sprite_image
        sprite_label.pack(pady=10)

    except FileNotFoundError:
        ctk.CTkLabel(scrollable_frame, text="No Sprite Found").pack()

    if pd.notna(p['Type 2']):
        type2_text = p['Type 2']
    else:
        type2_text = "None"

    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Type 1: {p['Type 1']}").pack()
    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Type 2: {p['Type 2']}").pack()
    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Legendary: {p['Legendary']}").pack(pady=3)
    ctk.CTkLabel(scrollable_frame, font=statfont, text=f"Generation: {int(p['Generation'])}").pack(pady=3)


    ctk.CTkLabel(scrollable_frame, font= bold_font, text="Base Stats").pack(pady=15, padx=5)

    stats = [
        ("HP", int(p['HP'])),
        ("Attack", int(p['Attack'])),
        ("Defense", int(p['Defense'])),
        ("Sp. Atk", int(p['Sp. Atk'])),
        ("Sp. Def", int(p['Sp. Def'])),
        ("Speed", int(p['Speed']))
    ]

    for stat_name, stat_value in stats:
        stat_frame = ctk.CTkLabel(scrollable_frame, text=stat_name, font=statfont)
        stat_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(stat_frame, text=f"{stat_name}:", font=statfont).pack(side="left", pady=15)
        ctk.CTkLabel(stat_frame, text=str(stat_value), font=statfont).pack(side="right", pady=15)


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

            show_pokemon(result.iloc[0])


button = ctk.CTkButton(app, text="Search 🔍", command=button_click_event)
button.pack(padx=20, pady=20)
button.place(relx=0.02, rely=0.29, anchor="sw")

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

    for idx,row in filtered_df.head(15).iterrows():
        ctk.CTkButton(
            scrollable_frame,
            text=f"{row['Name']}",
            command=lambda p=row: show_pokemon(p),
            width=300
        ).pack(pady=20)


optionmenu = ctk.CTkOptionMenu(app, values=["All", "Fire", "Water", "Grass", "Normal", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"], command=optionmenu_callback)
optionmenu.set("All")
optionmenu.pack(padx=20, pady=20)
optionmenu.place(relx=0.14, rely=0.29, anchor="sw")


app.mainloop()
