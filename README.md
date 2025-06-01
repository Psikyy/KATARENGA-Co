
# Katarenga&Co

## 🎮 Présentation

Katarenga&Co est une adaptation numérique de trois jeux de stratégie abstraite : **Katarenga**, **Congress** et **Isolation**. Il s'agit d'une application multiplateforme (Windows, macOS, Linux) développée en Python avec Pygame, qui vous permet de jouer seul contre une IA ou à deux en local.

---

## 🧩 Règles rapides

### 🟥 Types de cases (communs aux 3 jeux)

Le plateau est une grille de 10x10 cases, divisée en quadrants de différentes couleurs :

- 🔴 Rouge : déplacements orthogonaux (haut, bas, gauche, droite)
- 🟡 Jaune : déplacements en diagonale
- 🟢 Vert : déplacements en L (comme un cavalier aux échecs)
- 🔵 Bleu : déplacements dans toutes les directions mais d’une seule case (comme un roi)

---

### 1. **Katarenga**
- Chaque joueur a 8 pions.
- Les pions se déplacent en fonction de la couleur de la case où ils arrivent.
- Objectif : capturer les deux coins adverses **ou** éliminer tous les pions de l’adversaire.

### 2. **Congress**
- Objectif : rassembler tous ses pions en un bloc connecté orthogonalement.
- Pas de captures.
- Jeu de regroupement pur.

### 3. **Isolation**
- Les joueurs placent leurs pions à tour de rôle.
- Un pion ne peut pas être placé sur une case occupée.
- Le dernier à pouvoir jouer gagne.

---

## 🚀 Installation et lancement

### Prérequis
- Python 3.11 ou plus
- Pygame (`pip install pygame`)

### Étapes

1. **Cloner le dépôt** ou **télécharger l'archive ZIP** :
```bash
git clone https://github.com/votre-repo/katarenga-co.git
```

2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

3. **Lancer le jeu** :
```bash
python main.py
```

---

## 🕹️ Utilisation

- **Menu principal** : choisissez entre les 3 jeux.
- **Modes de jeu** :
  - Joueur vs Joueur (local)
  - Joueur vs IA (bot aléatoire)
- **Éditeur de plateau** : personnalisez les quadrants utilisés dans les parties.
- **Musique et sons** : activables/désactivables depuis les options.

---

## 📸 Captures d'écran

*(à ajouter dans le README du dépôt GitHub ou dans un dossier /screenshots)*

---

## 💡 Astuces

- Cliquez sur un pion pour voir ses déplacements possibles.
- Utilisez l’éditeur pour créer des plateaux uniques et les tester.
- Le jeu sauvegarde vos configurations temporairement, mais pas les parties.

---

## 📦 Dossier du projet

Voici les fichiers importants :
```
main.py         → Lance le jeu
menu/           → Menus du jeu
games/          → Logique des jeux Katarenga, Congress, Isolation
ui/             → Graphisme et boutons
design_case/    → Éditeur de quadrants
```

---

## 🤝 Auteurs

- Berteloot Tom  
- Martin Thomas  
- Mennechet Simon  
- Omar Arthur  
(SUPINFO Lille, 1ère année)

---

## 📜 Licence

Ce projet a été réalisé dans un cadre académique. Toute réutilisation extérieure nécessite autorisation.
