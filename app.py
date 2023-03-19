# -*- coding: utf-8 -*-
"""app

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ERKrZrEZwNGUfl04C0BRvmhcyHzsHo9s

https://www.google.com/search?q=d%C3%A9ployer+un+mod%C3%A8le+Machine+Learning+dans+une+application+web+python&rlz=1C1GCEA_enFR1040FR1040&sxsrf=AJOqlzUoKc2uoDsDPeJ6oE8fX-ylcHoxAA:1676554155784&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmwZv3kpr9AhWXY6QEHYnACsMQ_AUoAXoECAIQAw&biw=1280&bih=569&dpr=1.5#fpstate=ive&vld=cid:b07ffca4,vid:u0Syto1oAGA

# 1. Librairies nécessaires
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

"""# 2. Design général

"""

# Design de l'application

# Ajouter une vidéo en bannière

#st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Description

st.title("L'application blabla")

st.write('''
# Bienvenue.
Cet outil vous permet de prédire le prix de votre futur maison.
''')

"""# Choix des paramètres de la maison

L'utilisateur répond à des questions et entre les paramètres correspondant à son souait, selon des variables regroupées selon un "thème", comme l'aspect général de la maison, ses extérieurs, ou sa modernité.
"""

st.sidebar.header("Quelles caractéristiques votre future maison doit-elle présenter ?")

def user_input():
  #### LotArea : taille de la surface 
  # Demander à l'utilisateur de saisir la valeur de la surface
  min_value = 10
  max_value = 3000
  LotArea = st.sidebar.text_input("Taille de la maison avec son extérieur (en mètres carrés)", value = 100)
  # Vérifier que la saisie est valide
  try:
    selected_value = int(LotArea)
    if selected_value < min_value or selected_value > max_value:
      raise ValueError
  except ValueError:
        st.warning(f'Veuillez saisir un nombre entier entre {min_value} et {max_value}.')
  else:
        LotArea
  if not LotArea.isnumeric() and not LotArea.replace('.', '', 1).isnumeric():
    st.error('La saisie doit être un nombre décimal valide.')
  else:
        # Convertir la saisie en float
        LotArea_float = float(LotArea)
        
  #### OverQual : qualité générale
  OverallQual=st.sidebar.slider("Qualité du matériau global et de la finition sur 10", 0,10, value = 5)
  
  #### ExterQual : qualité extérieure
  ExterQual=st.sidebar.slider("Qualité du matériau extérieur sur 10", 0, 10, value = 5)
  
  #### BsmtQual : qualité du sous-sol
  BsmtQual=st.sidebar.slider("Qualité du sous-sol sur 10", 0, 10, value = 5)
  
  #### TotalBsmtSF : taille du sous-sol
  TotalBsmtSF=st.sidebar.slider("Taille de la surface du sous-sol (en mètres carrés)", 0,600, value = 20)
  
  #### HeatingQC : qualité du chauffage
  labels_HeatingQC= [1, 2, 3, 4, 5]
  options_HeatingQC = {
              1 :'Ex',
              2 : 'Gd',
              3 : 'TA',
              4 : 'Fa',
              5 : 'Po'
          }
  HeatingQC = st.sidebar.radio("Qualité et condition du chauffage", labels_HeatingQC, format_func=lambda x: options_HeatingQC[x])
  
  #### GrLivArea : surface habitable au-dessus du sol (en mètres carrés)
  GrLivArea=st.sidebar.slider("Surface habitable au-dessus du sol (en mètres carrés)", 10,4000)
  
  #### FullBath : nombre de salle(s) de bain
  FullBath=st.sidebar.slider("Nombre de salle(s) de bain", 0,5)
  
  #### HalfBath : nombre de toilette(s) séparées
  HalfBath=st.sidebar.slider("Nombre de toilette(s) séparées", 0,5)
  
  #### KitchenQual : qualité de la cuisine
  KitchenQual=st.sidebar.slider("Qualité de la cuisine sur 10", 0,10)
  
  #### KitchenQual : nombre de pièces
  TotRmsAbvGrd=st.sidebar.slider("Nombre de pièces", 0,14)
  
  #### Fireplaces : nombre de cheminée(s)
  Fireplaces=st.sidebar.slider("Nombre de cheminée(s)", 0,4)
  
  #### GarageCars : capacité du garage en nombre de voiture
  GarageCars=st.sidebar.slider("Capacité du garage en nombre de voiture", 0,4)
  
  #### GarageCond : capacité du garage en nombre de voiture
  GarageCond=st.sidebar.slider("Qualité du garage sur 10", 0,10)
  
  #### WoodDeckSF : taille de la terasse (en mètres carrés)
  WoodDeckSF=st.sidebar.slider("Taille de la terasse (en mètres carrés)", 0,800)
  
  #### OpenPorchSF : taille de la véranda (en mètres carrés)
  OpenPorchSF=st.sidebar.slider("Taille de la véranda (en mètres carrés)", 0,600)
  
  #### MS_zoning_RL : densité de l'endroit résidentiel
  labels_MS_zoning_RL = [0,1]
  options_MS_zoning_RL = {
      1 :'Forte densité résidentielle',
      0 : 'Faible densité résidentielle'
      }
  MS_zoning_RL = st.sidebar.radio("Densité du quartier", labels_MS_zoning_RL, format_func=lambda x: options_MS_zoning_RL[x])
  
  #### ModernityInYears : dernière rénovation
  ModernityInYears=st.sidebar.slider("Nombre d'années avant la dernière rénovation", 0,60)
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

"""# 3. Exécution du modèle retenu"""

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
