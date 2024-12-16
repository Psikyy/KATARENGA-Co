import tkinter as tk
from tkinter import messagebox
import re

def validate_entry(entry_text):
    return re.match("^[a-zA-Z0-9]{0,15}$", entry_text) is not None

def get_unique_names(names):
    unique_names = []
    name_count = {}
    for name in names:
        if name in name_count:
            name_count[name] += 1
            unique_names.append(f"{name}({name_count[name]})")
        else:
            name_count[name] = 0
            unique_names.append(name)
    return unique_names

def start_game():
    for widget in fenetre.winfo_children():
        widget.destroy()

    tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24)).pack(pady=20)

    game_buttons = [
        ("Katarenga", katarenga),
        ("Congress", congress),
        ("Isolation", isolation)
    ]

    for text, command in game_buttons:
        tk.Button(fenetre, text=text, command=command, width=20, height=2).pack(pady=10)

    tk.Button(fenetre, text="Accueil", command=show_main_menu, width=20, height=2).pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)

def katarenga():
    setup_game_screen("Katarenga", show_rules_katarenga)

def congress():
    setup_game_screen("Congress", show_rules_congress)

def isolation():
    setup_game_screen("Isolation", show_rules_isolation)

def setup_game_screen(title, rules_command):
    for widget in fenetre.winfo_children():
        widget.destroy()

    tk.Label(fenetre, text=title, font=("Helvetica", 24)).pack(pady=20)
    tk.Label(fenetre, text="Jouer", font=("Helvetica", 18)).pack(pady=10)
    tk.Label(fenetre, text="Pseudos", font=("Helvetica", 18)).pack(pady=10)

    pseudo_entry1 = tk.Entry(fenetre, width=30)
    pseudo_entry1.pack(pady=10)
    pseudo_entry1.insert(0, "Player 1")

    pseudo_entry2 = tk.Entry(fenetre, width=30)
    pseudo_entry2.pack(pady=10)
    pseudo_entry2.insert(0, "Player 2")

    def on_start():
        pseudo1 = pseudo_entry1.get() if validate_entry(pseudo_entry1.get()) else "Player 1"
        pseudo2 = pseudo_entry2.get() if validate_entry(pseudo_entry2.get()) else "Player 2"
        unique_names = get_unique_names([pseudo1, pseudo2])
        messagebox.showinfo("Starting Game", f"Players: {unique_names[0]}, {unique_names[1]}")

    tk.Button(fenetre, text="Start", command=on_start, width=20, height=2).pack(pady=10)
    tk.Button(fenetre, text="Accueil", command=show_main_menu, width=20, height=2).pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)
    tk.Button(fenetre, text="Règles", command=rules_command, width=20, height=2).pack(pady=10)

def show_rules_katarenga():
    show_rules("Katarenga", katarenga)

def show_rules_congress():
    show_rules("Congress", congress)

def show_rules_isolation():
    show_rules("Isolation", isolation)

def show_rules(title, back_command):
    for widget in fenetre.winfo_children():
        widget.destroy()

    tk.Label(fenetre, text=title, font=("Helvetica", 24)).pack(pady=20)
    tk.Label(fenetre, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", wraplength=600, justify="left").pack(pady=10)
    tk.Button(fenetre, text="Retour", command=back_command, width=20, height=2).pack(pady=10)

def load_game():
    messagebox.showinfo("Load Game", "Loading the game...")

def settings():
    messagebox.showinfo("Settings", "Opening settings...")

def quit_game():
    fenetre.quit()

def show_main_menu():
    for widget in fenetre.winfo_children():
        widget.destroy()

    tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24)).pack(pady=20)

    main_menu_buttons = [
        ("Start Game", start_game),
        ("Load Game", load_game),
        ("Settings", settings),
        ("Quit", quit_game)
    ]

    for text, command in main_menu_buttons:
        tk.Button(fenetre, text=text, command=command, width=20, height=2).pack(pady=10)

fenetre = tk.Tk()
fenetre.geometry("800x600")
fenetre.title("Menu Principal")
fenetre.resizable(width=False, height=False)

show_main_menu()
fenetre.mainloop()
