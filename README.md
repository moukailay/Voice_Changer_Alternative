# Premiere alternative du projet Voice_Changer

# Résumé du Projet "logic.py"
Ce projet est un script Python conçu pour la manipulation audio.
Il intègre plusieurs fonctionnalités pour l'enregistrement, la modification et la lecture des sons.

# Fonctionnalités Principales
Enregistrement de sons : Permet la capture de sons et leur sauvegarde dans un fichier.
Modification de l'audio : Inclut le changement de hauteur (pitch), de vitesse et de volume des sons enregistrés.
Lecture de l'audio : Capacité à jouer les sons modifiés.
Changement de voix en temps réel : Offre la possibilité d'alterer la voix durant l'enregistrement.

# Flux de Travail
Le son est d'abord enregistré et stocké.
L'audio enregistré peut ensuite être modifié selon différents paramètres.
Les sons modifiés sont disponibles pour la lecture ou peuvent être sauvegardés.

# Technologies Utilisées

  Pyo

Bibliothèque Python pour le traitement audio numérique.
Utilisée pour créer des effets sonores et manipuler des flux audio.

  Pydub

Bibliothèque Python pour la manipulation de fichiers audio.
Permet des modifications audio telles que la modification de hauteur, de vitesse, et de volume.
Python Standard Libraries

  time: pour la gestion des délais.
  math: pour les calculs nécessaires dans le traitement audio.

# Utilité des Technologies

Pyo : Essentiel pour le traitement audio en temps réel.
Pydub : Simplifie la manipulation de fichiers audio.
Librairies Python : Fournissent des fonctionnalités de base pour la gestion du temps et des calculs.
Conclusion
Ce projet offre un outil complet pour l'enregistrement, la modification et la lecture d'audio. 
Il est adapté pour des applications variées telles que la création musicale, les podcasts, 
et les effets sonores dans les jeux ou applications multimédia.

# Deuxieme alternative du projet Voice_Changer
# Voice_Changer_Alternative

# Étape 1: Préparation de l'Environnement
Installer les bibliothèques nécessaires :
  PyQt5 pour l'interface utilisateur (UI).
  Pydub pour manipuler les fichiers audio.
  PYO pour le traitement audio en temps réel.

  pip install PyQt5 pydub pyo

# Étape 2: Création de l'Interface Utilisateur avec PyQt5
# Définir l'interface principale :

  Créer une fenêtre principale avec des boutons pour l'enregistrement, l'arrêt, la lecture, l'upload 
  et le téléchargement.
  Ajouter des widgets pour afficher la progression de l'enregistrement et du téléchargement.
  Gestion des événements :
  
  Connecter les boutons à leurs fonctions respectives (ex: démarrer l'enregistrement, arrêter, etc.).
  
# Étape 3: Fonctionnalité d'Enregistrement Audio
# Enregistrement audio avec PYO :

  Configurer un stream d'entrée pour l'enregistrement à l'aide de PYO.
  Stocker l'audio enregistré dans un fichier (WAV en l'occurrence).
  
  Gestion de la durée d'enregistrement :
  
  Utiliser un timer pour limiter l'enregistrement à une minute.
  Afficher une barre de progression pour indiquer le temps restant.
  
# Étape 4: Lecture et Manipulation de l'Audio
# Lecture de l'audio enregistré :

  Utiliser Pydub pour gérer la lecture du fichier audio.
  Mettre à jour l'interface pour refléter l'état de lecture.
  Upload et modification de la voix :
  
  Permettre à l'utilisateur de télécharger l'audio enregistré.
  Offrir des options pour modifier la voix (changer la vitesse, le ton, etc.).
  
# Étape 5: Finalisation et Test
# Téléchargement du fichier audio final :

  Ajouter un bouton pour permettre à l'utilisateur de télécharger la version finale de l'audio.
 
  
# Étape 6: Création du Fichier et Import des Bibliothèques
# Créer un fichier nommé user_interface.py.

  Importer les bibliothèques nécessaires 
  
# Étape 7: Définition de la Classe pour l'Interface Utilisateur
  Définir une classe pour l'interface 
  
# Étape 8: Ajout des Widgets à l'Interface
  Ajouter des boutons et des labels :

Boutons pour enregistrer, arrêter, jouer, uploader, et télécharger.
Un label pour afficher des messages à l'utilisateur.
Une barre de progression pour l'enregistrement et l'upload.

# Étape 9: Configuration des Événements
  Configurer les événements pour les boutons :
  
  Chaque bouton doit être connecté à une fonction.

installation de WxPython lien : https://wxpython.org/pages/downloads/index.html
  
  
