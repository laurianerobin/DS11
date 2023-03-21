# -*- coding: utf-8 -*-
"""app

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ERKrZrEZwNGUfl04C0BRvmhcyHzsHo9s

https://www.google.com/search?q=d%C3%A9ployer+un+mod%C3%A8le+Machine+Learning+dans+une+application+web+python&rlz=1C1GCEA_enFR1040FR1040&sxsrf=AJOqlzUoKc2uoDsDPeJ6oE8fX-ylcHoxAA:1676554155784&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmwZv3kpr9AhWXY6QEHYnACsMQ_AUoAXoECAIQAw&biw=1280&bih=569&dpr=1.5#fpstate=ive&vld=cid:b07ffca4,vid:u0Syto1oAGA
"""

# Installation de streamlit
# Enlever lors de l'exécution de l'application

# !pip install streamlit

# Librairies nécessaires
# Les librairies dont l'installation est requise sont mentionnées dans le fichier "requirement.txt" dans le github

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

# Design de l'application

# Ajouter une vidéo en bannière
st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/house.gif")

# Description
st.write('''
### Une maison, un prix, l'outil.
Bienvenue chez _**BringItOnHome**_, l'agence immobilière innovante qui vous aide à **estimer la valeur de votre propriété en toute simplicité**. Nous comprenons que la vente ou l'achat d'une propriété est une décision importante, c'est pourquoi nous sommes déterminés à vous fournir les informations les plus précises possibles pour vous aider à prendre une **décision éclairée**.

Notre outil de prédiction de prix utilise les dernières technologies d'apprentissage automatique pour fournir des estimations précises et fiables, en se basant sur des données du marché immobilier américain. 

Il vous suffit de renseigner les caractéristiques de votre propriété, telles que la taille, l'emplacement et les équipements, pour obtenir une estimation immédiate. **Utilisez le volant déroulant à gauche pour nous décrire votre maison.**
''')

# L'utilisateur répond à des questions et entre les paramètres correspondant à son souait, selon des variables regroupées 
# selon un "thème", comme l'aspect général de la maison, ses extérieurs, ou sa modernité.

st.sidebar.header("C'est ici que l'on dessine les traits de votre chez vous.")


def user_input():

  ############### ASPECT GENERAL
  st.sidebar.header("Si l'on commençait par son aspect général ?")

  #### GrLivArea : surface habitable au-dessus du sol (en mètres carrés)
  # Demander à l'utilisateur de saisir la valeur de la surface
  min_value_GrLivArea = 10
  max_value_GrLivArea = 3000
  GrLivArea = st.sidebar.text_input("Surface habitable (en mètres carrés)", value = 100)
  
  # Vérifier que la saisie est valide
  try:
    selected_value = int(GrLivArea)
    if selected_value < min_value_GrLivArea or selected_value > max_value_GrLivArea:
      raise ValueError
  except ValueError:
      st.sidebar.warning(f'Veuillez saisir une surface comprise entre {min_value_GrLivArea} et {max_value_GrLivArea} mètres carrés.')
  else:
      GrLivArea
  
  # Vérifier le type rentré
  if not GrLivArea.isnumeric() and not GrLivArea.replace('.', '', 1).isnumeric():
      st.sidebar.error('La surface en mètres carrés doit être inscrite en nombre décimal.')
  else:
        # Convertir la saisie en float
        GrLivArea_float = float(GrLivArea)


  #### MS_zoning_RL : densité de l'endroit résidentiel
  labels_MS_zoning_RL = [0,1]
  options_MS_zoning_RL = {
      1 :'Forte densité résidentielle',
      0 : 'Faible densité résidentielle'
      }
  MS_zoning_RL = st.sidebar.radio("Densité du quartier", labels_MS_zoning_RL, format_func=lambda x: options_MS_zoning_RL[x])


  #### GardenSize : taille de la surface du jardin
  # On utilise st.checkbox() pour afficher une case à cocher
  GardenSize_want_option = st.sidebar.checkbox("Un espace extérieur entourant la maison ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if GardenSize_want_option:
      # Demander à l'utilisateur de saisir la valeur de la surface
    min_value_GardenSize = 10
    max_value_GardenSize = 3000
    GardenSize = st.sidebar.text_input("Précisez dans ce cas la surface extérieure (en mètres carrés)", value = 100)
    
    # Vérifier que la saisie est valide
    try:
      selected_value = int(GardenSize)
      if selected_value < min_value_GardenSize or selected_value > max_value_GardenSize:
        raise ValueError
    except ValueError:
        st.sidebar.warning(f'Veuillez saisir une surface comprise entre {min_value_GardenSize} et {max_value_GardenSize} mètres carrés.')
    else:
        GardenSize
    
    # Vérifier le type rentré
    if not GardenSize.isnumeric() and not GardenSize.replace('.', '', 1).isnumeric():
        st.sidebar.error('La surface en mètres carrés doit être inscrite en nombre entier.')
    else:
          # Convertir la saisie en float
          GardenSize_float = float(GardenSize)

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
  # On utilise st.checkbox() pour afficher une case à cocher
  TotalBsmtSF_want_option = st.sidebar.checkbox("Un sous-sol est une surface supplémentaire. Qu'en dites-vous ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if TotalBsmtSF_want_option:

    # Demander à l'utilisateur de saisir la valeur de la surface
    min_value_TotalBsmtSF = 5
    max_value_TotalBsmtSF = 600
    TotalBsmtSF = st.sidebar.number_input("Quelle est sa taille (en mètres carrés) ?", value = 20, step =1, min_value=5, max_value=None)

    #### BsmtQual : qualité du sous-sol
    BsmtQual=st.sidebar.slider("La qualité de cet espace sur 10", 0, 10, value = 5)  

  else:
      TotalBsmtSF = 0 
      BsmtQual = 0

  #### GarageCars : capacité du garage en nombre de voiture
  # On utilise st.checkbox() pour afficher une case à cocher
  Garage_want_option = st.sidebar.checkbox("Un garage pour une voiture ou du bricolage ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if Garage_want_option:
      GarageCars = st.sidebar.number_input("Pour combien de voitures à mettre à l'abri ?", value = 1, step = 1, min_value=0, max_value=None)
      GarageCond = st.sidebar.slider("Et vous jugeriez la qualité du garage sur 10", 0,10, value = 5)
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
  # On utilise st.checkbox() pour afficher une case à cocher
  terrasse_want_option = st.sidebar.checkbox("Une terrasse ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if terrasse_want_option:
      WoodDeckSF = st.sidebar.number_input("Quelle taille donc (en mètres carrés) ?", value = 10, step = 1, min_value=0, max_value=None)
  else:
      WoodDeckSF = 0

  #### OpenPorchSF : taille de la véranda (en mètres carrés)
  # On utilise st.checkbox() pour afficher une case à cocher
  OpenPorchSF_want_option = st.sidebar.checkbox("Et une véranda ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if OpenPorchSF_want_option:
      OpenPorchSF = st.sidebar.number_input("C'est noté ! Dites-nous sa taille (en mètres carrés)", value = 10, step = 1, min_value=0, max_value=None)
  else:
      OpenPorchSF = 0

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

# Créer le dictionnaire de correspondance entre les noms de colonnes actuels et les noms de colonnes souhaités
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

# Renommer les colonnes du DataFrame
df_renomme = df.rename(columns=noms_colonnes)

# Chargement des ensembles de test et d'apprentissage

url_Xtrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/X_train.csv'
X_train = pd.read_csv(url_Xtrain,parse_dates=[0])

url_ytrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/y_train.csv'
y_train = pd.read_csv(url_ytrain,parse_dates=[0])

url_Xtest = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/X_test.csv'
X_test = pd.read_csv(url_Xtest,parse_dates=[0])

url_ytest = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/y_test.csv'
y_test = pd.read_csv(url_ytest,parse_dates=[0])

# Application du meilleur modèle retenu

model_best = GradientBoostingRegressor(learning_rate=0.05, n_estimators=300, random_state = 42)
model_best.fit(X_train, y_train)

# Prédiction sur les données sélectionnées

prediction=model_best.predict(df)
pred = np.exp(prediction)

### Afficher la prédiction
import locale
import streamlit as st
from babel.numbers import format_decimal

# Arrondir la prédiction
pred_rounded = np.round(pred, 0)

# Formater la prédiction avec des espaces tous les milliers
formatted_pred = format_decimal(int(pred_rounded), format='#,##0', locale='fr')
# Afficher le dataframe sans l'index sous forme de tableau


st.write('''
### Voici la vôtre.
D'après ce que vous nous avez dit, le prix de la maison avec les critères suivants est estimé à''',  f'<span style="color: blue;"><b>{formatted_pred} $.</b></span>', unsafe_allow_html=True)
st.write(df_renomme)

# Afficher le bouton pour voir une maison similaire à ce prix

if st.button("Voir une maison similaire à ce prix"):
    # Conditionner l'affichage de l'image en fonction de la valeur de la prédiction
    if pred_rounded >= 10000 and pred_rounded < 140000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image0.jpg", caption="Maison similaire")
    elif pred_rounded >= 140000 and pred_rounded < 250000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image1.jpg", caption="Maison similaire")
    elif pred_rounded >= 250000 and pred_rounded < 369000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image2.jpg", caption="Maison similaire")
    elif pred_rounded >= 250000 and pred_rounded < 369000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image3.jpg", caption="Maison similaire")
    elif pred_rounded >= 369000 and pred_rounded < 456000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image4.jpg", caption="Maison similaire")
    elif pred_rounded >= 456000 and pred_rounded < 500000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image5.jpg", caption="Maison similaire")
    elif pred_rounded >= 500000 and pred_rounded < 756000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image6.jpg", caption="Maison similaire")
    elif pred_rounded >= 756000 and pred_rounded < 925000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image7.jpg", caption="Maison similaire")
    elif pred_rounded >= 925000 and pred_rounded < 1000000:
        st.image("https://raw.githubusercontent.com/laurianerobin/DS11/main/Image8.jpg", caption="Maison similaire")
    else:
        st.write("Désolé, il n'y a pas de maison similaire dans cette fourchette de prix")

# Ajouter un bouton "En savoir plus"

score_train = model_best.score(X_train, y_train)
score_test = model_best.score(X_test, y_test)

# Définir une variable de session pour stocker l'état du bouton
if "show_info" not in st.session_state:
    st.session_state.show_info = False

# Afficher le bouton "En savoir plus"
if st.button("En savoir plus sur notre expertise"):
    st.session_state.show_info = not st.session_state.show_info

# Afficher le texte si la variable de session est définie sur True
if st.session_state.show_info:
  st.write(''' Notre outil de prédiction est basée sur un modèle d'apprentissage. 
À titre informatif, ce modèle a été entraîné sur l'analyse de plus d'un millier de maisons résidentielles à Ames dans l'Iowa, données consitutées par l'Association Statistique Américaine (ASA).
''')  
  st.write("Sur ces données, nos équipes de data analysts sont parvenus à prédire correctement", round(score_test*100,1)," % sur des données de tests et ", round(score_train*100,2), " % sur des données servant à la construction du modèle.")