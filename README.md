# Katarenga&Co

## Table des matières

1. [Présentation générale](#présentation-générale)
2. [Matériel et plateau de jeu](#matériel-et-plateau-de-jeu)
3. [Règles des jeux](#règles-des-jeux)
4. [Installation](#installation)
5. [Guide d'utilisation](#guide-dutilisation)
6. [Fonctionnalités](#fonctionnalités)
7. [Structure du projet](#structure-du-projet)
8. [Équipe de développement](#équipe-de-développement)

---

## Présentation générale

Katarenga&Co est une adaptation numérique de trois jeux de stratégie abstraite développée dans le cadre d'un projet académique à SUPINFO Lille. Cette application multiplateforme (Windows, macOS, Linux) permet de jouer à **Katarenga**, **Congress** et **Isolation** en mode local ou contre une intelligence artificielle.

Le projet répond à une simulation d'appel à candidatures de la société fictive Smart Games, spécialisée dans l'édition de jeux de plateau de stratégie abstraite souhaitant se diversifier dans le jeu vidéo.

---

## Matériel et plateau de jeu

### Configuration du plateau

Le plateau de jeu est identique pour les trois jeux :
- Grille de 10x10 cases
- 4 quadrants de 4x4 cases chacun
- 4 cases utilisables dans les coins du plateau
- Chaque joueur dispose de 8 pions

### Types de cases et déplacements

Les déplacements des pions dépendent de la couleur de la case sur laquelle ils se trouvent :

**Case rouge** : Mouvements orthogonaux (haut, bas, gauche, droite) - inspirés de la tour aux échecs

**Case jaune** : Mouvements en diagonale - inspirés du fou aux échecs

**Case verte** : Mouvements en L - inspirés du cavalier aux échecs

**Case bleue** : Mouvements dans toutes les directions d'une distance d'une case - inspirés du roi aux échecs

---

## Règles des jeux

### Katarenga

**Objectif** : Être le premier à capturer les deux camps adverses situés dans les coins du plateau, ou éliminer suffisamment de pions adverses (il ne doit rester qu'un pion ou moins à l'adversaire).

**Déroulement** :
- Chaque joueur place ses 8 pions sur le plateau
- Les pions se déplacent selon la couleur de leur case de destination
- Un pion peut capturer un pion adverse en se déplaçant sur sa case
- La partie se termine par la conquête des camps ou l'élimination des pions

### Congress

**Objectif** : Rassembler tous ses pions en un bloc orthogonalement connecté.

**Particularités** :
- Aucune capture possible
- Aucune occupation de camps
- Jeu purement tactique de regroupement
- La victoire est obtenue dès que tous les pions du joueur forment un groupe connecté

### Isolation

**Objectif** : Être le dernier joueur capable de placer un pion sur le plateau.

**Déroulement** :
- Les joueurs placent leurs pions à tour de rôle sur un plateau initialement vide
- Aucun pion ne peut être capturé lors de son placement
- La partie se termine quand un joueur ne peut plus effectuer de placement légal
- Le dernier joueur à pouvoir jouer remporte la partie

---

## Installation

### Prérequis techniques

- Python 3.11 ou version ultérieure
- Pygame (installation automatique via requirements.txt)

### Procédure d'installation

1. **Récupération du code source**
   ```bash
   git clone https://github.com/votre-repo/katarenga-co.git
   cd katarenga-co
   ```

2. **Installation des dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancement du jeu**
   ```bash
   python main.py
   ```

---

## Guide d'utilisation

### Menu principal

Au lancement, vous accédez au menu principal proposant :
- **Lancer le jeu** : accès à la sélection des jeux
- **Paramètres** : configuration de la langue (français/anglais)
- **Quitter** : fermeture de l'application

### Sélection du jeu

Choisissez parmi les trois jeux disponibles :
- Katarenga
- Congress  
- Isolation

### Modes de jeu

Pour chaque jeu, trois modes sont proposés :
- **Mode local (2 joueurs)** : jeu sur la même machine
- **Mode en ligne (2 joueurs)** : fonctionnalité en développement
- **Jouer contre un robot** : adversaire IA avec coups aléatoires

### Configuration de partie

1. **Saisie des noms** : personnalisez les pseudonymes des joueurs
2. **Modification du plateau** : rotation des quadrants par clic (rotation de 90°)
3. **Éditeur avancé** : personnalisation complète des quadrants
4. **Validation** : lancement de la partie

### Interface de jeu

- Les pions noirs commencent toujours la partie
- Cliquez sur un pion pour afficher ses déplacements possibles
- Bouton "Règles" disponible pour consulter les règles en cours de partie
- Détection automatique des conditions de victoire

---

## Fonctionnalités

### Modes de jeu
- Joueur contre joueur local
- Joueur contre intelligence artificielle

### Jeux disponibles
- Katarenga : conquête stratégique
- Congress : connexion tactique
- Isolation : placement optimisé

### Personnalisation
- Éditeur de quadrants avec interface graphique
- Choix des couleurs par case
- Sauvegarde et chargement des créations personnalisées
- Configuration multilingue (français/anglais)

### Interface utilisateur
- Menus intuitifs et navigables
- Mise en évidence des coups légaux
- Messages de victoire automatiques
- Gestion des paramètres audio et visuels

---

## Structure du projet

```
Katarenga-Co/
├── main.py              # Point d'entrée principal
├── server.py            # Gestion réseau (en développement)
├── menu/                # Système de menus
├── games/               # Logique des trois jeux
│   ├── katarenga/
│   ├── congress/
│   ├── isolation/
│   └── common.py
├── ui/                  # Interface utilisateur
│   ├── animation.py
│   ├── buttons.py
│   ├── colors.py
│   └── fonts.py
├── design_case/         # Éditeur de quadrants
├── img/                 # Ressources graphiques
├── musique/             # Ressources audio
└── dev/                 # Scripts de développement
```

### Architecture technique

**Langage** : Python (multiplateforme, développement rapide, riche bibliothèque)

**Librairie graphique** : Pygame (gestion complète des événements et rendu 2D)

**Communication réseau** : Socket TCP intégré à Python

**Modèle orienté objet** :
- Game : gestion du déroulement des parties
- Player : données utilisateur et pions
- Board : cases et logique de déplacement  
- Piece : couleur, position et règles de mouvement

---

## Équipe de développement

**Projet réalisé par les étudiants de première année SUPINFO Lille :**

- Berteloot Tom
- Martin Thomas  
- Mennechet Simon
- Omar Arthur

**Date de réalisation** : 01/06/2025

---

## Notes techniques

### Limitations actuelles
- Mode en ligne en cours de développement (création de salles fonctionnelle)
- IA basique avec coups aléatoires
- Sauvegarde temporaire uniquement

### Améliorations prévues
- Finalisation du mode multijoueur en ligne
- Amélioration de l'intelligence artificielle
- Système de sauvegarde des parties
- Animations visuelles enrichies
- Éditeur de thèmes graphiques

---

**Licence** : Projet académique - Toute réutilisation extérieure nécessite autorisation.