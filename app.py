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

#st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Description

st.title("L'application blabla")

st.write('''
# Bienvenue.
Cet outil vous permet de prédire le prix de votre futur maison.
''')

# L'utilisateur répond à des questions et entre les paramètres correspondant à son souait, selon des variables regroupées 
# selon un "thème", comme l'aspect général de la maison, ses extérieurs, ou sa modernité.

def user_input():

  ############### ASPECT GENERAL
  st.sidebar.header("Si l'on commençait par son aspect général ?")
  
  #### LotArea : taille de la surface 
  # Demander à l'utilisateur de saisir la valeur de la surface
  min_value_LotArea = 10
  max_value_LotArea = 3000
  LotArea = st.sidebar.text_input("Taille de la maison avec son extérieur (en mètres carrés)", value = 100)
  
  # Vérifier que la saisie est valide
  try:
    selected_value = int(LotArea)
    if selected_value < min_value_LotArea or selected_value > max_value_LotArea:
      raise ValueError
  except ValueError:
      st.sidebar.warning(f'Veuillez saisir un nombre entier entre {min_value_LotArea} et {max_value_LotArea}.')
  else:
      LotArea
  
  # Vérifier le type rentré
  if not LotArea.isnumeric() and not LotArea.replace('.', '', 1).isnumeric():
      st.sidebar.error('La surface en mètres carrés doit être inscrite en nombre décimal.')
  else:
        # Convertir la saisie en float
        LotArea_float = float(LotArea)

  #### GrLivArea : surface habitable au-dessus du sol (en mètres carrés)
  # Demander à l'utilisateur de saisir la valeur de la surface
  min_value_GrLivArea = 10
  max_value_GrLivArea = 3000
  GrLivArea = st.sidebar.text_input("Surface habitable au-dessus du sol (en mètres carrés)", value = 100)
  
  # Vérifier que la saisie est valide
  try:
    selected_value = int(GrLivArea)
    if selected_value < min_value_GrLivArea or selected_value > max_value_GrLivArea:
      raise ValueError
  except ValueError:
      st.sidebar.warning(f'Veuillez saisir un nombre entier entre {min_value_GrLivArea} et {max_value_GrLivArea}.')
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
  

  ############### INTERIEUR
  st.sidebar.header("Passons à l'intérieur. Après vous.")

  #### KitchenQual : nombre de pièces
  TotRmsAbvGrd=st.sidebar.slider("Nombre de pièces", 0,14, value = 3)

  #### FullBath : nombre de salle(s) de bain
  FullBath=st.sidebar.slider("Nombre de salle(s) de bain", 0,5, value = 1)
  
  #### HalfBath : nombre de toilette(s) séparées
  HalfBath=st.sidebar.slider("Nombre de toilette(s) séparées", 0,5, value = 1)

  ############### EQUIPEMENTS
  st.sidebar.header("Des remarques sur les équipements ?")

  #### OverQual : qualité générale
  OverallQual=st.sidebar.slider("Qualité du matériau global et de la finition sur 10", 0,10, value = 5)

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
  
  #### KitchenQual : qualité de la cuisine
  KitchenQual=st.sidebar.slider("Qualité de la cuisine sur 10", 0,10, value = 5)

  #### Fireplaces : nombre de cheminée(s)
  Fireplaces=st.sidebar.slider("Nombre de cheminée(s)", 0,4, value = 0)
  

  #### GrLivArea : surface habitable au-dessus du sol (en mètres carrés)
  # Demander à l'utilisateur de saisir la valeur de la surface
  min_value_TotalBsmtSF = 0
  max_value_TotalBsmtSF = 600
  TotalBsmtSF = st.sidebar.text_input("Taille de la surface du sous-sol (en mètres carrés)", value = 20)
  
  # Vérifier que la saisie est valide
  try:
    selected_value = int(TotalBsmtSF)
    if selected_value <= min_value_TotalBsmtSF or selected_value > max_value_TotalBsmtSF:
      raise ValueError
  except ValueError:
      st.sidebar.warning(f'Veuillez saisir un nombre entier entre {min_value_TotalBsmtSF} et {max_value_TotalBsmtSF}.')
  else:
      TotalBsmtSF
  
  # Vérifier le type rentré
  if not TotalBsmtSF.isnumeric() and not TotalBsmtSF.replace('.', '', 1).isnumeric():
      st.sidebar.error('La surface en mètres carrés doit être inscrite en nombre décimal.')
  else:
        # Convertir la saisie en float
        TotalBsmtSF_float = float(TotalBsmtSF)

  #### BsmtQual : qualité du sous-sol
  BsmtQual=st.sidebar.slider("Qualité du sous-sol sur 10", 0, 10, value = 5)


  #### GarageCars : capacité du garage en nombre de voiture
  # On utilise st.checkbox() pour afficher une case à cocher
  Garage_want_option = st.sidebar.checkbox("Un garage pour une voiture ou du bricolage ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if Garage_want_option:
      GarageCars = st.sidebar.number_input("Pour combien de voitures à mettre à l'abri ?", value = 10, step = 1)
      GarageCond = st.sidebar.slider("Qualité du garage sur 10", 0,10, value = 5)
  else:
      GarageCars = 0
      GarageCond = 0


  ############### EXTERIEUR
  st.sidebar.header("Terminons par un tour de l'extérieur.")

  #### ExterQual : qualité extérieure
  ExterQual=st.sidebar.slider("Qualité du matériau extérieur sur 10", 0, 10, value = 5)

  #### ModernityInYears : dernière rénovation
  ModernityInYears=st.sidebar.slider("Nombre d'années avant la dernière rénovation", 0,60, value = 10)

  #### WoodDeckSF : taille de la terasse (en mètres carrés)
  # On utilise st.checkbox() pour afficher une case à cocher
  terasse_want_option = st.sidebar.checkbox("Une terasse ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if terasse_want_option:
      WoodDeckSF = st.sidebar.number_input("Quelle taille donc (en mètres carrés) ?", value = 10, step = 1)
  else:
      WoodDeckSF = 0

  #### OpenPorchSF : taille de la véranda (en mètres carrés)
  # On utilise st.checkbox() pour afficher une case à cocher
  OpenPorchSF_want_option = st.sidebar.checkbox("Et une véranda ?")

  # Si la case est cochée, on affiche un curseur st.slider()
  if OpenPorchSF_want_option:
      OpenPorchSF = st.sidebar.number_input("C'est noté ! Dites-nous sa taille (en mètres carrés)", value = 10, step = 1)
  else:
      OpenPorchSF = 0

  data={'LotArea':LotArea,
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

st.write("D'après ce que vous nous avez dit, votre bien comportant")
st.write(df)

# Chargement des ensembles de test et d'apprentissage

url_Xtrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/X_train.csv'
X_train = pd.read_csv(url_Xtrain,parse_dates=[0])

url_ytrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/y_train.csv'
y_train = pd.read_csv(url_ytrain,parse_dates=[0])

# Application du meilleur modèle retenu

model_best = GradientBoostingRegressor(learning_rate = 0.1, max_depth = 3, n_estimators = 100)
model_best.fit(X_train, y_train)

# Prédiction sur les données sélectionnées

prediction=model_best.predict(df)
pred = np.exp(prediction)

st.subheader("Le prix de la maison est :")
st.write(pred)