# -*- coding: utf-8 -*-
"""app

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ERKrZrEZwNGUfl04C0BRvmhcyHzsHo9s

https://www.google.com/search?q=d%C3%A9ployer+un+mod%C3%A8le+Machine+Learning+dans+une+application+web+python&rlz=1C1GCEA_enFR1040FR1040&sxsrf=AJOqlzUoKc2uoDsDPeJ6oE8fX-ylcHoxAA:1676554155784&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmwZv3kpr9AhWXY6QEHYnACsMQ_AUoAXoECAIQAw&biw=1280&bih=569&dpr=1.5#fpstate=ive&vld=cid:b07ffca4,vid:u0Syto1oAGA
"""

# Librairies nécessaires
# Les librairies dont l'installatione est requise sont mentionnées dans le fichier "requirement.txt" dans le github

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

# Choix des paramètres pour la maison
# Utilisation d'une sidebar : les informations peuvent être choisies à l'aide curseurs
# Des valeurs pré-rentrées sont définies avec value, ou index

st.sidebar.header("Quelles caractéristiques votre future maison doit-elle présenter ?")

def user_input():
  LotArea=st.sidebar.slider("Taille de la surface de la maison et de l'extérieur (en mètres carrés)", 50, 20000, value = 100)
  
  OverallQual=st.sidebar.slider("Qualité du matériau global et de la finition sur 10", 0,10, value = 5)
  
  ExterQual=st.sidebar.slider("Qualité du matériau extérieur sur 10", 0, 10, value = 5)
  
  BsmtQual=st.sidebar.slider("Qualité du sous-sol sur 10", 0, 10, value = 5)
  
  TotalBsmtSF=st.sidebar.slider("Taille de la surface du sous-sol (en mètres carrés)", 0,600, value = 20)
  
  labels_HeatingQC= [1, 2, 3, 4, 5]
  options_HeatingQC = {
    1 :'Ex',
    2 : 'Gd',
    3 : 'TA',
    4 : 'Fa',
    5 : 'Po'
}

  HeatingQC = st.sidebar.radio("Qualité et condition du chauffage", labels_HeatingQC, format_func=lambda x: options_HeatingQC[x])

  GrLivArea=st.sidebar.slider("GrLivArea", 1000,4000)
  FullBath=st.sidebar.slider("FullBath", 0,3)
  HalfBath=st.sidebar.slider("HalfBath", 0,3)
  KitchenQual=st.sidebar.slider("KitchenQual", 0,10)
  TotRmsAbvGrd=st.sidebar.slider("TotRmsAbvGrd", 0,14)
  Fireplaces=st.sidebar.slider("Fireplaces", 0,3)
  GarageCars=st.sidebar.slider("Fireplaces", 0,4)
  GarageCond=st.sidebar.slider("GarageCond", 0,10)
  WoodDeckSF=st.sidebar.slider("WoodDeckSF", 0,800)
  OpenPorchSF=st.sidebar.slider("OpenPorchSF", 0,600)
  MS_zoning_RL=st.sidebar.slider("MS_zoning_RL", 0,1)
  ModernityInYears=st.sidebar.slider("ModernityInYears", 0,60)
 
  data={
        'LotArea':LotArea,
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
