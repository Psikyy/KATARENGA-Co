import tkinter as tk
from tkinter import messagebox
import re

def validate_entry(entry_text):
    # Allow only alphanumeric characters and limit to 15 characters
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
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add new buttons
    new_game_button = tk.Button(fenetre, text="Katarenga", command=katarenga, width=20, height=2)
    new_game_button.pack(pady=10)
    
    continue_game_button = tk.Button(fenetre, text="Congress", command=congress, width=20, height=2)
    continue_game_button.pack(pady=10)
    
    multiplayer_button = tk.Button(fenetre, text="Isolation", command=isolation, width=20, height=2)
    multiplayer_button.pack(pady=10)
    
    # Add Home button at the bottom left
    home_button = tk.Button(fenetre, text="Accueil", command=show_main_menu, width=20, height=2)
    home_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)

def katarenga():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add labels and entry fields
    play_label = tk.Label(fenetre, text="Jouer", font=("Helvetica", 18))
    play_label.pack(pady=10)
    
    pseudo_label = tk.Label(fenetre, text="Pseudos", font=("Helvetica", 18))
    pseudo_label.pack(pady=10)
    
    pseudo_entry1 = tk.Entry(fenetre, width=30)
    pseudo_entry1.pack(pady=10)
    pseudo_entry1.insert(0, "Player 1")
    
    pseudo_entry2 = tk.Entry(fenetre, width=30)
    pseudo_entry2.pack(pady=10)
    pseudo_entry2.insert(0, "Player 2")
    
    def on_start():
        pseudo1 = pseudo_entry1.get()
        pseudo2 = pseudo_entry2.get()
        
        if not validate_entry(pseudo1):
            pseudo1 = "Player 1"
        if not validate_entry(pseudo2):
            pseudo2 = "Player 2"
        
        unique_names = get_unique_names([pseudo1, pseudo2])
        
        messagebox.showinfo("Starting Game", f"Players: {unique_names[0]}, {unique_names[1]}")
    
    start_button = tk.Button(fenetre, text="Start", command=on_start, width=20, height=2)
    start_button.pack(pady=10)
    
    # Add Home button at the bottom left
    home_button = tk.Button(fenetre, text="Accueil", command=show_main_menu, width=20, height=2)
    home_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)
    
    # Add Rules button
    rules_button = tk.Button(fenetre, text="Règles", command=show_rules_katarenga, width=20, height=2)
    rules_button.pack(pady=10)

def show_rules_katarenga():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add rules text
    rules_text = tk.Label(fenetre, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", wraplength=600, justify="left")
    rules_text.pack(pady=10)
    
    # Add Back button
    back_button = tk.Button(fenetre, text="Retour", command=katarenga, width=20, height=2)
    back_button.pack(pady=10)

def congress():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Congress", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add labels and entry fields
    play_label = tk.Label(fenetre, text="Jouer", font=("Helvetica", 18))
    play_label.pack(pady=10)

    pseudo_label = tk.Label(fenetre, text="Pseudos", font=("Helvetica", 18))
    pseudo_label.pack(pady=10)
    
    pseudo_entry1 = tk.Entry(fenetre, width=30)
    pseudo_entry1.pack(pady=10)
    pseudo_entry1.insert(0, "Player 1")
    
    pseudo_entry2 = tk.Entry(fenetre, width=30)
    pseudo_entry2.pack(pady=10)
    pseudo_entry2.insert(0, "Player 2")
    
    def on_start():
        pseudo1 = pseudo_entry1.get()
        pseudo2 = pseudo_entry2.get()
        
        if not validate_entry(pseudo1):
            pseudo1 = "Player 1"
        if not validate_entry(pseudo2):
            pseudo2 = "Player 2"
        
        unique_names = get_unique_names([pseudo1, pseudo2])
        
        messagebox.showinfo("Starting Game", f"Players: {unique_names[0]}, {unique_names[1]}")

    start_button = tk.Button(fenetre, text="Start", command=on_start, width=20, height=2)
    start_button.pack(pady=10)
    
    # Add Home button at the bottom left
    home_button = tk.Button(fenetre, text="Accueil", command=show_main_menu, width=20, height=2)
    home_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)
    # Add Rules button
    rules_button = tk.Button(fenetre, text="Règles", command=show_rules_congress, width=20, height=2)
    rules_button.pack(pady=10)


def show_rules_congress():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Congress", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add rules text
    rules_text = tk.Label(fenetre, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", wraplength=600, justify="left")
    rules_text.pack(pady=10)
    
    # Add Back button
    back_button = tk.Button(fenetre, text="Retour", command=congress, width=20, height=2)
    back_button.pack(pady=10)

def isolation():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Isolation", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add labels and entry fields
    play_label = tk.Label(fenetre, text="Jouer", font=("Helvetica", 18))
    play_label.pack(pady=10)
    
    pseudo_label = tk.Label(fenetre, text="Pseudos", font=("Helvetica", 18))
    pseudo_label.pack(pady=10)
    
    pseudo_entry1 = tk.Entry(fenetre, width=30)
    pseudo_entry1.pack(pady=10)
    pseudo_entry1.insert(0, "Player 1")
    
    pseudo_entry2 = tk.Entry(fenetre, width=30)
    pseudo_entry2.pack(pady=10)
    pseudo_entry2.insert(0, "Player 2")
    
    def on_start():
        pseudo1 = pseudo_entry1.get()
        pseudo2 = pseudo_entry2.get()
        
        if not validate_entry(pseudo1):
            pseudo1 = "Player 1"
        if not validate_entry(pseudo2):
            pseudo2 = "Player 2"
        
        unique_names = get_unique_names([pseudo1, pseudo2])
        
        messagebox.showinfo("Starting Game", f"Players: {unique_names[0]}, {unique_names[1]}")

    start_button = tk.Button(fenetre, text="Start", command=on_start, width=20, height=2)
    start_button.pack(pady=10)
    
    # Add Home button at the bottom left
    home_button = tk.Button(fenetre, text="Accueil", command=show_main_menu, width=20, height=2)
    home_button.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.SW)

    # Add Rules button
    rules_button = tk.Button(fenetre, text="Règles", command=show_rules_isolation, width=20, height=2)
    rules_button.pack(pady=10)

def show_rules_isolation():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Add title
    title_label = tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Add rules text
    rules_text = tk.Label(fenetre, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.", wraplength=600, justify="left")
    rules_text.pack(pady=10)
    
    # Add Back button
    back_button = tk.Button(fenetre, text="Retour", command=katarenga, width=20, height=2)
    back_button.pack(pady=10)

def load_game():
    messagebox.showinfo("Load Game", "Loading the game...")

def settings():
    messagebox.showinfo("Settings", "Opening settings...")

def quit_game():
    fenetre.quit()

def show_main_menu():
    # Clear the current widgets
    for widget in fenetre.winfo_children():
        widget.destroy()
    
    # Game title
    title_label = tk.Label(fenetre, text="Katarenga", font=("Helvetica", 24))
    title_label.pack(pady=20)
    
    # Start Game button
    start_button = tk.Button(fenetre, text="Start Game", command=start_game, width=20, height=2)
    start_button.pack(pady=10)
    
    # Load Game button
    load_button = tk.Button(fenetre, text="Load Game", command=load_game, width=20, height=2)
    load_button.pack(pady=10)
    
    # Settings button
    settings_button = tk.Button(fenetre, text="Settings", command=settings, width=20, height=2)
    settings_button.pack(pady=10)
    
    # Quit button
    quit_button = tk.Button(fenetre, text="Quit", command=quit_game, width=20, height=2)
    quit_button.pack(pady=10)

fenetre = tk.Tk()
fenetre.geometry("800x600")
fenetre.title("Menu Principal")
fenetre.resizable(width=False, height=False)

show_main_menu()

fenetre.mainloop()