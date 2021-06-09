# Programme_extraction_prix
Extraction des informations produits sur le site Books to Scrape, revendeur de livres en ligne
- Version bêta

* Orphée analyste marketing chez Books Online 08/06/2021

 # Description :
Ce programme développé en python 3.9.5 a pour vocation, dans sa version bêta, d’extraire, en format csv, 
et de classer par catégorie les informations des produits distribués par Books to Scrape.

Informations extraites :
-	url du produit
-	Numéro de référence
-	Nom du produit
-	Prix TTC
-	Prit HT
-	Disponibilité en stock
-	Description
-	Catégorie
-	Note
-	Image de couverture

# Environnement virtuel : 

## Création :
Pour la procédure décrite ci-dessous vous devez disposer au minimum de la version Python 3.3.
Ouvrir un terminal et choisir un emplacement pour l’environnement virtuel
(si vous avez déjà téléchargé le programme accédé au dossier dans lequel vous l’avez enregistré)

- Sur Windows :
Python -m venv <non de l’environnement>
- Sur Unix et MacOS :
Python3 -m venv <non de l’environnement>     

## Activation :
- Sur Windows, :
env\Scripts\activate

- Sur Unix et MacOS  :
source tutorial-env/bin/activate
(Ce script est écrit pour le shell bash. Si vous utilisez csh ou fish, utilisez les variantes activate.csh ou activate.fish.)

# Installation des paquets nécessaires

pip install -r requirements.txt
  
# Exécution du code

- Sur Windows :
python  P2_01_codesource.py
- Sur Unix et MacOS :
python3  P2_01_codesource.py

