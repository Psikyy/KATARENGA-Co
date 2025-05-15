# settings.py

# Traductions
translations = {
    "Français": {
        "settings": "Paramètres",
        "language": "Langue",
        "back": "Retour",
        "start_game": "Lancer le jeu",
        "quit": "Quitter",
        "rules": "Règles",
        "validate": "Valider",
        "player1": "Joueur 1 (Rouge)",
        "player2": "Joueur 2 (Bleu)",
        "select_game": "Sélection du jeu",
        "katarenga": "Katarenga",
        "congress": "Congress",
        "isolation": "Isolation",
        "mode_local": "Mode Local (2 joueurs)",
        "mode_online": "Mode Online (à venir)",
        "mode_bot": "Contre un Bot",
        "enter_names": "Entrez les noms des joueurs sans espaces ni caractères spéciaux.",
    },
    "English": {
        "settings": "Settings",
        "language": "Language",
        "back": "Back",
        "start_game": "Start Game",
        "quit": "Quit",
        "rules": "Rules",
        "validate": "Validate",
        "player1": "Player 1 (Red)",
        "player2": "Player 2 (Blue)",
        "select_game": "Game Selection",
        "katarenga": "Katarenga",
        "congress": "Congress",
        "isolation": "Isolation",
        "mode_local": "Local Mode (2 players)",
        "mode_online": "Online Mode (coming soon)",
        "mode_bot": "Play Against Bot",
        "enter_names": "Enter player names without spaces or special characters.",
    }
}

# Langue par défaut
settings = {
    "language": "Français",
}

current_language = settings["language"]

def set_language(lang):
    global current_language, settings
    current_language = lang
    settings["language"] = lang
    save_settings(settings)

def save_settings(updated_settings):
    # Tu peux enregistrer dans un fichier .json si tu veux que ça persiste
    global settings, current_language
    settings.update(updated_settings)
    current_language = settings["language"]

# Fonction de traduction
def t(key):
    return translations.get(current_language, {}).get(key, key)
