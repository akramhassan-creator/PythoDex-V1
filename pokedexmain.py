
import pandas as pd
import customtkinter as ctk
import matplotlib
matplotlib.use('agg')
from customtkinter import CTkImage
from PIL import Image
import pokebase as pb
import requests
from io import BytesIO
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.deactivate_automatic_dpi_awareness()



df = pd.read_csv('pokemondata.csv', sep=',', header=0)
df['Name'] = df['Name'].str.replace(r'^.*?(?=Mega)', '', regex=True)
print(df)
print(df.to_string())

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Pokedex Tracker")
app.geometry("1920x1080")
app.wm_iconbitmap('pokeball.ico')

spinner_angle = 0
spinner_running = False
spinner_label = None
spinner_image_original = Image.open("rotpoke.png")



my_font = ctk.CTkFont(family="<Helvetica>", size=20)
font = ctk.CTkFont(family="<Helvetica>", size=30)
afont = ctk.CTkFont(family="<Helvetica>", size=15)
tfont = ctk.CTkFont(family="<Helvetica>", size=20)
bold_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
pold_font = ctk.CTkFont(family="Helvetica", size=30, weight="bold")
statfont = ctk.CTkFont(family="Helvetica", size=15)
abfont = ctk.CTkFont(family="Pokemon Solid", size=13)
newfont = ctk.CTkFont(family="Pokemon Hollow", size=30, weight="bold")
hfont = ctk.CTkFont(family="Pokemon Hollow", size=8, weight="bold")
pfont = ctk.CTkFont(family="Pokemon Solid", size=20, weight="bold")
ffont = ctk.CTkFont(family="Helvetica", size=20)

label = ctk.CTkLabel(app, font=ffont, text="Welcome to")
label.pack(pady=50)

poke_image = ctk.CTkImage(dark_image=Image.open("C:\\Users\\akybo\\PycharmProjects\\Pokedex-V1\\Pokedex_logo.png"),
                          size=(387, 140))



poke_label = ctk.CTkLabel(app, image=poke_image, text="")
poke_label.pack(pady=(10, 0))

control_frame = ctk.CTkFrame(app, fg_color="#2B2B2B", height=80)
control_frame.pack(side="top", fill="x", padx=20, pady=(10, 5))


close_button = ctk.CTkButton(
    app,
    text="Close",
    command=app.destroy,
    font=afont,
    fg_color="red",
    hover_color="darkred")
close_button.place(relx=0.90, rely=0.96, anchor="nw")


scrollable_frame = ctk.CTkScrollableFrame(app, width=450, height=700)
scrollable_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)


scrollable_frame_right = ctk.CTkScrollableFrame(app, width=700, height=700, fg_color="#2b2b2b")
scrollable_frame_right.pack(side="right", padx=10, pady=10, fill="both", expand=True)


poke_header = ctk.CTkLabel(scrollable_frame_right, text="Stats & Charts", font=pold_font, text_color="#FFDE00")
poke_header.pack(pady=20)



def clear_scrollable_frames():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

def rotate_spinner():
    global spinner_angle, spinner_running

    if not spinner_running:
        return

    spinner_angle = (spinner_angle + 10) % 360

    rotated = spinner_image_original.rotate(spinner_angle)

    spinner_ctk_image = CTkImage(dark_image=rotated, size=(100, 100))

    if spinner_label and spinner_label.winfo_exists():
        spinner_label.configure(image=spinner_ctk_image)
        spinner_label.image = spinner_ctk_image

    if spinner_running:
        app.after(50, rotate_spinner)

def start_spinner():
    global spinner_running, spinner_label, spinner_angle

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    spinner_angle = 0

    ctk.CTkLabel(scrollable_frame, text = 'Loading Pokemon...', font=pfont, text_color="yellow").pack(pady=20)

    spinner_ctk_image = ctk.CTkImage(
        dark_image=spinner_image_original, size=(100, 100))

    spinner_label = ctk.CTkLabel(
        scrollable_frame,
        image=spinner_ctk_image,
        text="",
    )
    spinner_label.image = spinner_ctk_image
    spinner_label.pack(pady=20)

    spinner_running = True
    rotate_spinner()


def stop_spinner():
    global spinner_running, spinner_label
    spinner_running = False

    if spinner_label and spinner_label.winfo_exists():
        spinner_label.destroy()
        spinner_label = None


def show_pokemon_threaded(p):
    start_spinner()

    def task():
        try:
            show_pokemon(p)
        finally:

            app.after(0, lambda: stop_spinner())

    threading.Thread(target=task, daemon=True).start()


def poke_header():
    for widget in scrollable_frame_right.winfo_children():
        if widget != poke_header:
            widget.destroy()


def show_pokemon(p):

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

    for widget in scrollable_frame.winfo_children():
            widget.destroy()

    for widget in scrollable_frame_right.winfo_children():
        if widget != poke_header:
            widget.destroy()

    ctk.CTkLabel(scrollable_frame, font=pold_font, text=p['Name']).pack()

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

    for widget in scrollable_frame_right.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 5))

    stat_names = [stat[0] for stat in stats]
    stat_values = [stat[1] for stat in stats]

    ax.bar(stat_names, stat_values, color="red", edgecolor="black")

    ax.set_ylabel('Stat Value')
    ax.set_title(f' {p["Name"]} Base Stats')
    ax.set_ylim(0, max(stat_values) + 20)

    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=scrollable_frame_right)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20, padx=20, fill="both", expand=True)

    plt.close(fig)

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

label = ctk.CTkLabel(control_frame, text="Search for Pokémon", font=abfont, fg_color="transparent")
label.bind("<Button-1>", button_click_event)
label.pack(pady=20)
label.place(relx=0.025, rely=0.46, anchor="sw")

button = ctk.CTkButton(control_frame, text="Search 🔍", command=button_click_event)
button.pack(padx=10, pady=10)
button.place(relx=0.02, rely=0.9, anchor="sw")


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
            command=lambda p=row: show_pokemon_threaded(p),
            width=300
        ).pack(pady=20)


optionmenu = ctk.CTkOptionMenu(control_frame, values=["Fire", "Water", "Grass", "Normal", "Electric", "Ice", "Fighting",
                                            "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon",
                                            "Dark", "Steel", "Fairy"], command=optionmenu_callback)

label = ctk.CTkLabel(control_frame, text="Filter by Type", font=afont, fg_color="transparent")
label.bind("<Button-1>", optionmenu)
label.pack(pady=20)
label.place(relx=0.133, rely=0.305, anchor="sw")

optionmenu.set("Choose Type")
optionmenu.pack(padx=20, pady=20)
optionmenu.place(relx=0.12, rely=0.37, anchor="sw")


def generation_callback(choice=None):
    if choice is None:
        choice = generationmenu.get()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if choice == "All":
        filtered_df = df

    else:
        filtered_df = df[df['Generation'] == int(choice)]

    ctk.CTkLabel(scrollable_frame, text=f"Generation {choice} ({len(filtered_df)} Pokemon)", font=bold_font).pack(pady=20)

    for idx, row in filtered_df.head(15).iterrows():
            ctk.CTkButton(
                scrollable_frame,
                text=f"{row['Name']}",
                command=lambda p=row: show_pokemon_threaded(p),
                width=300
            ).pack(pady=20)


generationmenu = ctk.CTkOptionMenu(control_frame, values=["All"] + [str(i) for i in range(1,7)], command=generation_callback)

label = ctk.CTkLabel(app, font=abfont, text="Filter by Gen")
label.bind("<Button-1>", generationmenu)
label.pack(pady=20)
label.place(relx=0.233, rely=0.339, anchor="sw")

generationmenu.set("Choose Gen")
generationmenu.pack(padx=30, pady=30)
generationmenu.place(relx=0.22, rely=0.37, anchor="sw")


app.mainloop()
