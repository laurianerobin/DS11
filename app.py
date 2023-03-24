# -*- coding: utf-8 -*-
"""app

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ERKrZrEZwNGUfl04C0BRvmhcyHzsHo9s

**M2 SIAD groupe DS11**

> Adélie Cleenewerck, Raphaël Crespo-Pereira, Mélanie Lobjois, Lauriane Robin

Ce script vise à créer **l'application pour permettre à un utilisateur de pouvoir utiliser le modèle de prédiction du prix de sa maison dans son propre intérêt**. Il est donc question de pouvoir produire un site, qui prend à la fois les données utilisées et le modèle de machine learning élaboré dans le code d'analyse des données. 

Un autre objectif est de rendre cette **application utile et facile d'utilisation pour un vendeur comme un acheteur d'un bien immobilier**. Un design d'interface a été pensé.

Ceci est réalisé par l'intermédiaire de [Streamlit](https://streamlit.io).

Les **étapes de production de cette application** sont les suivantes : 
> 1. Créer le compte Github et créer le nouveau projet. 
2. Cloner le projet Github sur l'ordinateur en utilisant la commande Git clone.
3. Installer Streamlit en utilisant la commande pip install streamlit.
4. Créer un fichier Python qui contient le code Streamlit.
5. Ajouter ce fichier au projet Github. Le projet est disponible sur ce [dépôt public](https://github.com/laurianerobin/DS11) (laurianerobin/DS11).
6. Faire un commit et push pour enregistrer les changements sur Github.
7. Accéder au projet Github dans un navigateur et ouvrir l'application Streamlit.
"""

### Installation de streamlit
# Enlever lors de l'exécution de l'application

# !pip install streamlit

### Librairies nécessaires
# Les librairies dont l'installation est requise sont mentionnées dans le fichier "requirement.txt" dans le github

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

### Design de l'application

# Ajouter une vidéo en bannière
st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house.gif")

# Description
st.write('''
### Un prix, une maison, l'outil.
Bienvenue chez _BringItOnHome_, l'agence immobilière innovante qui vous aide à **estimer la valeur de votre propriété en toute simplicité**. Nous comprenons que la vente ou l'achat d'une propriété est une décision importante, c'est pourquoi nous sommes déterminés à vous fournir les informations les plus précises possibles pour vous aider à prendre une **décision éclairée**.''')

st.write(f"<span style='color:#2B92A5;'><b>Utilisez le volant déroulant à gauche pour nous décrire votre maison</b></span>. Il vous suffit de renseigner les caractéristiques de votre propriété, telles que la taille, l'emplacement et les équipements, pour obtenir une estimation immédiate.", unsafe_allow_html=True)

st.write("Notre outil de prédiction de prix utilise les dernières technologies d'apprentissage automatique pour fournir des estimations précises et fiables, en se basant sur des données du **marché immobilier américain**.")

### L'utilisateur répond à des questions et entre les paramètres correspondant à son souait, selon des variables regroupées 
### selon un "thème", comme l'aspect général de la maison, ses extérieurs, ou sa modernité.

st.sidebar.header("C'est ici que l'on dessine les traits de votre chez vous.")

def user_input():

  ############### ASPECT GENERAL
  st.sidebar.header("Si l'on commençait par son aspect général ?")


  #### GrLivArea : surface habitable au-dessus du sol (en mètres carrés)
  GrLivArea_metre = st.sidebar.text_input("Surface habitable (en mètres carrés)", value = "150")

  # Vérifier que la saisie est valide
  GrLivArea = 0
  try:
    # Convertit la valeur en pieds carrés
    if GrLivArea_metre.replace(".", "", 1).isdigit():
      if float(GrLivArea_metre) < 10 or float(GrLivArea_metre) > 10000:
        st.sidebar.warning("Veuillez saisir une surface comprise entre 10 et 10 000 mètres carrés.")
        GrLivArea = 0
      else:
        GrLivArea = float(GrLivArea_metre) * 10.7639
  except ValueError:
    st.sidebar.warning("Veuillez saisir une valeur numérique.")
    GrLivArea = 0


  #### MS_zoning_RL : densité de l'endroit résidentiel
  labels_MS_zoning_RL = [0,1]
  options_MS_zoning_RL = {
      1 :'Forte densité résidentielle',
      0 : 'Faible densité résidentielle'
      }
  MS_zoning_RL = st.sidebar.radio("Densité du quartier", labels_MS_zoning_RL, format_func=lambda x: options_MS_zoning_RL[x])


  #### GardenSize : taille de la surface du jardin
  # Ajouter une case à cocher pour permettre à l'utilisateur de choisir si oui ou non il souhaite un extérieur
  oui_garden = st.sidebar.checkbox("Un espace extérieur entourant la maison ?")
  
  # Si la case est cochée, demander à l'utilisateur de saisir la surface en mètres carrés
  if oui_garden:
        GardenSize_metrecarre = st.sidebar.number_input("Indiquez sa taille (en mètres carrés)", value = 40, min_value=10, max_value=30000, step=10)
        if GardenSize_metrecarre:
          # Convertir la surface de mètres carrés en pieds carrés
          GardenSize = GardenSize_metrecarre * 10.7639
        else:
          st.sidebar.sidebar.warning("Veuillez saisir une surface comprise entre 10 et 30 000 mètres carrés.")
  else:
        GardenSize = 0


  ############### INTERIEUR
  st.sidebar.header("Passons à l'intérieur. Après vous.")


  #### TotRmsAbvGrd : nombre de pièces
  TotRmsAbvGrd = st.sidebar.number_input("Nombre de pièce(s)", value = 4, step = 1, min_value=1, max_value=None)


  #### FullBath : nombre de salle(s) de bain
  FullBath = st.sidebar.number_input("Nombre de salle(s) de bain", value = 1, step = 1, min_value=1, max_value=None)
  

  #### HalfBath : nombre de toilette(s) séparées
  HalfBath = st.sidebar.number_input("Nombre de toilettes séparées", value = 1, step = 1, min_value=1, max_value=None)



  ############### EQUIPEMENTS
  st.sidebar.header("Des remarques sur les équipements ?")

  #### OverQual : qualité générale
  OverallQual=st.sidebar.slider("Qualité du matériau global et de la finition sur 10", 0,10, value = 5)


  #### KitchenQual : qualité de la cuisine
  KitchenQual=st.sidebar.slider("Qualité de la cuisine sur 10", 0,10, value = 5)


  #### HeatingQC : qualité du chauffage
  labels_HeatingQC= [1, 2, 3, 4, 5]
  defaultHeat=3
  options_HeatingQC = {
              1 :'Excellent',
              2 : 'Bon',
              3 : 'Moyen',
              4 : 'Faible',
              5 : 'Pauvre'
          }
  HeatingQC = st.sidebar.radio("Qualité et condition du chauffage et de la consommation énergétique", labels_HeatingQC, 
                               format_func=lambda x: options_HeatingQC[x], index=labels_HeatingQC.index(defaultHeat))


  #### Fireplaces : nombre de cheminée(s)
  # On utilise st.checkbox() pour afficher une case à cocher
  Fireplaces_want_option = st.sidebar.checkbox("Vous chauffez-vous aussi avec une cheminée ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if Fireplaces_want_option:
    Fireplaces=st.sidebar.number_input("Précisez-nous combien de cheminée(s)", step=1, value=0, min_value=0, max_value=None)
  else:
      Fireplaces = 0 


  #### TotalBsmtSF : taille de la surface du sous-sol 
  # Ajouter une case à cocher pour permettre à l'utilisateur de répondre ou non à la question de la surface
  oui_bsmt = st.sidebar.checkbox("Un sous-sol est une surface supplémentaire. Qu'en dites-vous ?")
  
  # Si la case est cochée, demander à l'utilisateur de saisir la surface en mètres carrés
  if oui_bsmt:

      # TotalBsmtSF : taille
      TotalBsmtSF_metrecarre = st.sidebar.number_input("Précisez la taille de cette surface (en mètres carrés)", min_value=10, max_value=10000)
      if TotalBsmtSF_metrecarre:
          # Convertir la surface de mètres carrés en pieds carrés
          TotalBsmtSF = TotalBsmtSF_metrecarre * 10.7639
      else:
          st.sidebar.warning("Veuillez saisir une surface comprise entre 10 et 10 000 mètres carrés.")
      
      #### BsmtQual : qualité du sous-sol
      BsmtQual=st.sidebar.slider("Jugez la qualité de cet espace sur 10", 0, 10, value = 5)

  else:
    TotalBsmtSF = 0
    BsmtQual = 0 


  #### GarageCars : capacité du garage en nombre de voiture
  # On utilise st.checkbox() pour afficher une case à cocher
  oui_garage = st.sidebar.checkbox("Un garage pour une voiture ou du bricolage ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if oui_garage:
      GarageCars = st.sidebar.number_input("Pour combien de voitures à mettre à l'abri ?", value = 1, step = 1, min_value=0, max_value=None)
      GarageCond = st.sidebar.slider("Et quelle note donneriez-vous sur 10 pour sa qualité ?", 0,10, value = 5)
  else:
      GarageCars = 0
      GarageCond = 0


  ############### EXTERIEUR
  st.sidebar.header("Terminons par un tour de l'extérieur.")


  #### ExterQual : qualité extérieure
  ExterQual=st.sidebar.slider("Qualité du matériau extérieur sur 10", 0, 10, value = 5)


  #### ModernityInYears : dernière rénovation
  ModernityInYears=st.sidebar.slider("Nombre d'années avant la dernière rénovation", 0,60, value = 10)


  #### WoodDeckSF : taille de la terrasse (en mètres carrés)
  # Ajouter une case à cocher pour permettre à l'utilisateur de répondre ou non à la question de la terrasse
  oui_terrasse = st.sidebar.checkbox("Une terrasse ?")
  
  # Si la case est cochée, demander à l'utilisateur de saisir la surface en mètres carrés
  if oui_terrasse:
      WoodDeckSF_metrecarre = st.sidebar.number_input("Quelle taille donc (en mètres carrés) ?", value = 10, step = 1, min_value=0, max_value=None)
      if WoodDeckSF_metrecarre:
          # Convertir la surface de mètres carrés en pieds carrés
          WoodDeckSF = WoodDeckSF_metrecarre * 10.7639
      else:
          st.sidebar.warning("Veuillez saisir une surface comprise valide entre 10 et 30 000 mètres carrés.")
  else:
    WoodDeckSF = 0


  #### OpenPorchSF : taille de la véranda (en mètres carrés)
  # Ajouter une case à cocher pour permettre à l'utilisateur de répondre ou non à la question de la véranda
  oui_veranda = st.sidebar.checkbox("Et une véranda ?")
  
  # Si la case est cochée, demander à l'utilisateur de saisir la surface en mètres carrés
  if oui_veranda:
      OpenPorchSF_metrecarre = st.sidebar.number_input("C'est noté ! Dites-nous sa taille (en mètres carrés)", value = 10, step = 1, min_value=0, max_value=None)
      if OpenPorchSF_metrecarre:
          # Convertir la surface de mètres carrés en pieds carrés
          OpenPorchSF = OpenPorchSF_metrecarre * 10.764
      else:
          st.sidebar.warning("Veuillez saisir une valeur valide entre 10 et 500 mètres carrés.")
  else:
    OpenPorchSF = 0


  ############### Faire correspondre les input précédents dans un dataframe. Ce dataframe sera utilisé pour la prédiction du prix en fonction des valeurs choisies

  data={'GardenSize':GardenSize,
        'OverallQual':OverallQual,
        'ExterQual':ExterQual,
        'BsmtQual':BsmtQual,
        'TotalBsmtSF':TotalBsmtSF,
        'HeatingQC':HeatingQC,
        'GrLivArea':GrLivArea,
        'FullBath':FullBath,
        'HalfBath':HalfBath,
        'KitchenQual':KitchenQual,
        'TotRmsAbvGrd':TotRmsAbvGrd,
        'Fireplaces':Fireplaces,
        'GarageCars':GarageCars,
        'GarageCond':GarageCond,
        'WoodDeckSF':WoodDeckSF,
        'OpenPorchSF':OpenPorchSF,
        'MS_zoning_RL':MS_zoning_RL,
        'ModernityInYears':ModernityInYears
        }
  maison_parametre=pd.DataFrame(data,index=[0])
  return maison_parametre

df=user_input()


### Créer le dictionnaire de correspondance entre les noms de colonnes actuels et les noms de colonnes souhaités
noms_colonnes = {
    'GardenSize': 'Taille du jardin',
        'OverallQual':'Qualité globale',
        'ExterQual':'Qualité de l\'extérieur',
        'BsmtQual':'Qualité du sous-sol',
        'TotalBsmtSF':'Surface du sous-sol',
        'HeatingQC':'Qualité du chauffage',
        'GrLivArea':'Surface habitable',
        'FullBath':'Nombre de salle(s) de bain',
        'HalfBath':'Nombre de toilettes séparées',
        'KitchenQual':'Qualité de la cuisine',
        'TotRmsAbvGrd':'Nombre de pièce(s)',
        'Fireplaces':'Nombre de cheminée(s)',
        'GarageCars':'Capacité du garage en voiture',
        'GarageCond':'Qualité du garage',
        'WoodDeckSF':'Surface de la terrasse',
        'OpenPorchSF':'Surface de la véranda',
        'MS_zoning_RL':'Densité résidentielle',
        'ModernityInYears':'Années avant la dernière rénovation'
}

### Renommer les colonnes du DataFrame pour une utilisation claire (termes en français non raccourcis)
df_renomme = df.rename(columns=noms_colonnes)

### Chargement des ensembles de test et d'apprentissage
# Streamlit puise les données depuis Github

url_Xtrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/X_train.csv'
X_train = pd.read_csv(url_Xtrain,parse_dates=[0])

url_ytrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/y_train.csv'
y_train = pd.read_csv(url_ytrain,parse_dates=[0])

url_Xtest = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/X_test.csv'
X_test = pd.read_csv(url_Xtest,parse_dates=[0])

url_ytest = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/y_test.csv'
y_test = pd.read_csv(url_ytest,parse_dates=[0])

### Prédiction du prix avec les données sélectionnées par l'utilisateur

# Application du meilleur modèle retenu

model_best = GradientBoostingRegressor(learning_rate=0.05, n_estimators=300, random_state = 42)
model_best.fit(X_train, y_train)

# Prédiction sur les données sélectionnées par l'utilisateur (user_input de df)

prediction=model_best.predict(df)
pred = np.exp(prediction)

# Afficher la prédiction
import locale
import streamlit as st
from babel.numbers import format_decimal

# Arrondir la prédiction
pred_rounded = np.round(pred, 0)

# Formater la prédiction avec des espaces tous les milliers
formatted_pred = format_decimal(int(pred_rounded), format='#,##0', locale='fr')

st.write('''
### Voici la vôtre.
D'après ce que vous nous avez dit, le prix de votre maison est estimé à''',  f'<span style="color:#2B92A5; font-size:21px"><b>{formatted_pred} $</b></span>.', unsafe_allow_html=True)
st.write(df_renomme)

### Afficher le bouton pour voir une maison similaire à ce prix
# Pour ajouter une réponse davantage concrète et plus profonde qu'une simple estimation de prix
# Une image correspondant à une maison dans la ville d'Ames (Iowa, États-Unis) est affichée selon une plage de prix correspondante
# Ces images proviennent du site https://www.homes.com/ames-ia/houses-for-sale/?gclsrc=aw.ds&gclid=Cj0KCQjw8e-gBhD0ARIsAJiDsaWQ2kw7d6R69_3_pKlMXEd7Mlt9Wpk9wWPW0PY0lwfGMZbhgfIFBUEaAuLjEALw_wcB 

# défiler une image, puis un aperçu de Google Maps où on peut zoomer, et une vue de Street View sur Streamlit 
# en utilisant des bibliothèques telles que streamlit_embedcode, googlemaps, et google_streetview.

st.write(f'''
### Et voici ce à quoi elle pourrait ressembler. 
''')

# Conditionner l'affichage de l'image en fonction de la valeur de la prédiction
if pred_rounded >= 100000 and pred_rounded < 150000:
  lienhomes = "https://www.homes.com/property/3110-oakland-st-ames-ia/ewmmx3md3nv1v/"
  homes = "actuellement en vente ici"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house140.gif")
elif pred_rounded >= 150000  and pred_rounded < 230000:
  lienhomes = "https://www.homes.com/property/1115-orchard-dr-ames-ia/z1ze8vl58blgv/"
  homes = "actuellement en vente ici"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house225.gif")
elif pred_rounded >= 230000 and pred_rounded < 260000:
  lienhomes = "https://www.homes.com/property/1214-garfield-cir-ames-ia/s05cvk2j4gh7n/"
  homes = "actuellement en vente ici"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house250.gif")
elif pred_rounded >= 260000 and pred_rounded < 280000:
  lienhomes = "https://www.homes.com/property/6516-prairie-ridge-rd-ames-ia/ey78yn0483e9l/"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  homes = "actuellement en vente ici"
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house275.gif")
elif pred_rounded >= 280000 and pred_rounded < 320000:
  lienhomes = "https://www.homes.com/property/5334-543rd-ave-ames-ia/3ezh3gv5x1bnl/"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  homes = "actuellement en vente ici"
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house300.gif")
elif pred_rounded >= 320000 and pred_rounded < 350000:
  lienhomes = "https://www.homes.com/property/5308-clemens-blvd-ames-ia/zevydzvc4x05n/"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  homes = "actuellement en vente ici"
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house345.gif")
elif pred_rounded >= 350000 and pred_rounded < 410000:
  lienhomes = "https://www.homes.com/property/5521-westfield-dr-ames-ia/z88vnx2ze4rsw/"
  st.write(f"Il semblerait que votre recherche soit proche de cette maison similaire, <a href='{lienhomes}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{homes}</a> par l'agence immobilière américaine Homes.", unsafe_allow_html=True)
  homes = "actuellement en vente ici"
  st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house400.gif")
else:
  st.write("Désolé, nous n'avons pas trouvé de maison similaire actuellement en vente dans cette fourchette de prix à Ames (Iowa).")

### Ajouter un bouton "En savoir plus"
# Ce bouton activé permet à l'utilisateur de lire un court paragraphe sur les données utilisées et 
# le travail effectué en amont pour élaborer le modèle de prédiction aboutissant à la prédiction obtenue

score_train = model_best.score(X_train, y_train)
score_test = model_best.score(X_test, y_test)

# Définir une variable de session pour stocker l'état du bouton
if "show_info" not in st.session_state:
    st.session_state.show_info = False

# Afficher le bouton "En savoir plus"
if st.button("En savoir plus sur notre expertise"):
    st.session_state.show_info = not st.session_state.show_info

# Afficher le texte si la variable de session est définie sur True
  # lien hypertexte vers le concours kaggle
lien = "https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data"
texte = "données constituées"

if st.session_state.show_info:
  st.write(f"Notre outil de prédiction est basé sur un modèle d'apprentissage dit de régresseur à _gradient boosting_. Ce dernier utilise plusieurs arbres de décision pour prédire les valeurs. À titre informatif, ce modèle a été entraîné sur l'analyse de plus d'un millier de maisons résidentielles à Ames dans l'Iowa, <a href='{lien}' style='color:#2B92A5; font-weight:bold; text-decoration:none;'>{texte}</a> par l'Association Statistique Américaine.", unsafe_allow_html=True)  
  st.write("Sur ces données, nos équipes de data analysts sont parvenus à prédire correctement", round(score_test*100,1)," % sur des données de tests et ", round(score_train*100,2), " % sur des données servant à la construction du modèle.")