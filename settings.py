import json
import os

def load_translations():
    try:
        with open('translations.json', "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Fichier de traductions non trouvé.")
        return {"Français": {}}

# Sauvegarder les paramètres
def save_settings(settings):
    with open('settings.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file)

# Charger les paramètres
def load_settings():
    try:
        with open('settings.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        default_settings = {"volume": 0.5, "language": "Français", "fullscreen": False}
        save_settings(default_settings)
        return default_settings

translations = load_translations()
settings = load_settings()
current_language = settings["language"]

def t(key):
    return translations[current_language].get(key, key)