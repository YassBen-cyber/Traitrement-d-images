# Projet : Dijkstra sur Image (Segmentation)

Ce projet implémente l'algorithme de **Dijkstra** appliqué au traitement d'image. Il permet de trouver le chemin de moindre coût visuel entre deux pixels, agissant comme un outil de "Ciseaux Intelligents" pour le détourage automatique.

Il a été réalisé en **Python** dans le cadre du module d'Algorithmique Avancée.

## Fonctionnalités

*   **Interface Graphique (GUI)** : Application complète pour charger et interagir avec les images.
*   **Segmentation Interactive** :
    *   Chargement d'images (JPG, PNG).
    *   Sélection intuitive du point de **Départ (Vert)** et d'**Arrivée (Rouge)** à la souris.
*   **Algorithme de Dijkstra Adaptation** :
    *   Graphe implicite en 4-connexité.
    *   Poids basés sur la différence d'intensité (Niveaux de gris).
    *   Contournement automatique des obstacles contrastés.
*   **Exportation** : Sauvegarde de l'image avec le chemin tracé en surbrillance.

1.  **Installer les dépendances :**
    Le projet nécessite `numpy` pour les matrices et `Pillow` pour la gestion d'image.
    ```bash
    pip install numpy pillow
    ```
    *(Note : Tkinter est généralement inclus avec Python sur Windows).*

## Utilisation

1.  **Lancer l'application :**
    ```bash
    python gui_app.py
    ```

2.  **Dans l'interface :**
    *   Cliquez sur **"Charger Image"** pour ouvrir une photo.
    *   **Clic Gauche** sur l'image pour placer le point de **Départ** (Rond Vert).
    *   **Clic Gauche** à nouveau pour placer le point d'**Arrivée** (Rond Rouge).
    *   Cliquez sur **"Lancer Dijkstra"**.
    *   Le chemin optimal s'affiche en **Bleu**.
    *   Utilisez **"Sauvegarder"** pour enregistrer le résultat.

## Structure du Projet


MiniProjet/
├── README.md               # Ce fichier
├── gui_app.py              # Application principale (Interface Tkinter)
├── dijkstra_image.py       # Coeur algorithmique (Graphe + Dijkstra)
├── mona_lisa.png           # Image de test (N&B)
└── mona_lisaColor.png      # Image de test (Couleur)


## Auteur

**BENOUFELLA MOHAMED YACINE**

