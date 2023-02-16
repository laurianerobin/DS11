# -*- coding: utf-8 -*-
"""application.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SD9UeVXLPcqvKz0vqEPPhrNFFW5-wvxo

DS11 - Adélie Cleenewerck, Raphaël Crespo-Pereira, Mélanie Lobjois, Lauriane Robin

# Importation
"""

import pandas as pd
sample_submission = pd.read_csv("/content/sample_submission.csv")
test = pd.read_csv("/content/test.csv")
train = pd.read_csv("/content/train.csv")

# Dimensions des sous-ensembles de test et de d'apprentissage
variable_dict = {'table de train': train, 'table de test' : test}
for i in ['table de train', 'table de test']:
    print('Les dimensions (lignes x colonnes) de la %s sont : ' %i, variable_dict[i].shape)

sample_submission.head()

train.head()
test.head()

# vérifier qu'elles sont dans le bon type 
print("les variables numériques sont", train.select_dtypes(include=['float64','int64']).columns)
print("les variables catégorielles sont", train.select_dtypes(include=['object']).columns)

"""## 1. Préparation des données

### Traitement des valeurs manquantes
"""

# Valeurs manquantes
valeurs_manquantes=train.isna().sum().reset_index()
valeurs_manquantes.columns=(['Variables','Valeurs manquantes'])
valeurs_manquantes.reset_index(drop=True).sort_values(by='Valeurs manquantes',ascending=False).head(19)

train_na = (train.isnull().sum() / len(train)) * 100      
train_na = train_na.drop(train_na[train_na == 0].index).sort_values(ascending=False)[:30]
missing_data = pd.DataFrame({'Pourcentage de valeurs manquantes' :train_na})
missing_data.head(19)

import matplotlib.pyplot as plt
vars_with_na = [var for var in train.columns if train[var].isnull().sum() > 0]
train[vars_with_na].isnull().mean().sort_values(
    ascending=False).plot.bar(figsize=(10, 4))
plt.ylabel('Pourcentage de données manquantes')

plt.show()

import missingno as msno
import matplotlib.pyplot as plt
msno.heatmap(train)
plt.show()

# Remplacer les valeurs manquantes dans TRAIN

# Remplacer par "None"
train["FireplaceQu"] = train["FireplaceQu"].fillna("None")
train["GarageYrBlt"] = train["GarageYrBlt"].fillna("None")
train["GarageCond"] = train["GarageCond"].fillna("None")
train["GarageType"] = train["GarageType"].fillna("None")
train["GarageFinish"] = train["GarageFinish"].fillna("None")
train["GarageQual"] = train["GarageQual"].fillna("None")
train["BsmtFinType2"] = train["BsmtFinType2"].fillna("None")
train["BsmtExposure"] = train["BsmtExposure"].fillna("None")
train["BsmtQual"] = train["BsmtQual"].fillna("None")
train["BsmtCond"] = train["BsmtCond"].fillna("None")
train["BsmtFinType1"] = train["BsmtFinType1"].fillna("None")
train["MasVnrType"] = train["MasVnrType"].fillna("None")

# Supprimer variables dont les modalités sont sur-représentées
train = train.drop(columns=['PoolQC'])
train = train.drop(columns=['MiscFeature'])
train = train.drop(columns=['Alley'])
train = train.drop(columns=['Fence'])

# Remplacer par la moyenne les variables numériques pouvant être remplacé
train["LotFrontage"] = train.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.mean()))
train["MasVnrArea"] = train.groupby("Neighborhood")["MasVnrArea"].transform(lambda x: x.fillna(x.mean()))
train['Electrical'] = train['Electrical'].fillna(train['Electrical'].mode()[0])

# Remplacer les valeurs manquantes dans TEST

# Remplacer par "None"
test["FireplaceQu"] = test["FireplaceQu"].fillna("None")
test["GarageYrBlt"] = test["GarageYrBlt"].fillna("None")
test["GarageCond"] = test["GarageCond"].fillna("None")
test["GarageType"] = test["GarageType"].fillna("None")
test["GarageFinish"] = test["GarageFinish"].fillna("None")
test["GarageQual"] = test["GarageQual"].fillna("None")
test["BsmtFinType2"] = test["BsmtFinType2"].fillna("None")
test["BsmtExposure"] = test["BsmtExposure"].fillna("None")
test["BsmtQual"] = test["BsmtQual"].fillna("None")
test["BsmtCond"] = test["BsmtCond"].fillna("None")
test["BsmtFinType1"] = test["BsmtFinType1"].fillna("None")
test["MasVnrType"] = test["MasVnrType"].fillna("None")


# Supprimer variables dont les modalités sont sur-représentées
test = test.drop(columns=['PoolQC'])
test = test.drop(columns=['MiscFeature'])
test = test.drop(columns=['Alley'])
test = test.drop(columns=['Fence'])

# Remplacer par la moyenne les variables numériques pouvant être remplacé
test["LotFrontage"] = test.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.mean()))
test["MasVnrArea"] = test.groupby("Neighborhood")["MasVnrArea"].transform(lambda x: x.fillna(x.mean()))
test['Electrical'] = test['Electrical'].fillna(test['Electrical'].mode()[0])
test['TotalBsmtSF'] = test['TotalBsmtSF'].fillna(test['TotalBsmtSF'].mode()[0])
test['KitchenQual'] = test['KitchenQual'].fillna(test['KitchenQual'].mode()[0])
test['GarageCars'] = test['GarageCars'].fillna(test['GarageCars'].mode()[0])

"""### Outliers"""

import seaborn as sns
s = sns.scatterplot(data=train,x='GrLivArea',y='SalePrice')
s.set(xlabel ="Surface", ylabel = "Prix", title ='Le prix des maisons en fonction de la surface')

# supprimer observations "aberrantes" (maisons avec prix anormalement élevés)
train=train.drop(train[(train['GrLivArea']>4000) & (train['SalePrice']<300000)].index)

"""# 2. Statistiques descriptives"""

# Prix
import matplotlib.pyplot as plt
print("Moyenne du prix :", round(train["SalePrice"].mean(),0))
print("Médiane du prix :", train["SalePrice"].median())

train["SalePrice"].hist(bins=50, grid=False)
plt.title("Prix");

"""# 3. Sélection des variables

### Préparation de la data avant la sélection des variables : on recode les variables catégorielles en numérique ordonnée
"""

train["GarageCond"] = train["GarageCond"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
train["GarageQual"] = train["GarageQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
train["GarageFinish"] = train["GarageFinish"].replace({"Fin": 3, "RFn": 2, "Unf": 1, "None": 0})
train["FireplaceQu"] = train["FireplaceQu"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
train["KitchenQual"] = train["KitchenQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
train["HeatingQC"] = train["HeatingQC"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
train["BsmtFinType1"] = train["BsmtFinType1"].replace({"GLQ": 6, "ALQ": 5, "BLQ": 4, "Rec": 3, "LwQ": 2, "Unf": 1, "None": 0})
train["BsmtExposure"] = train["BsmtExposure"].replace({"Gd": 5, "Av": 4, "Mn": 3, "No": 2, "None": 1})
train["BsmtCond"] = train["BsmtCond"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
train["BsmtQual"] = train["BsmtQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
train["ExterCond"] = train["ExterCond"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
train["ExterQual"] = train["ExterQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
train["HeatingQC"] = train["HeatingQC"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})

train["Street"] = train["Street"].replace({"Grvl": 1, "Paved": 2})
train["LandContour"] = train["LandContour"].replace({"Lvl": 4, "Bnk": 3, "HLS" : 2, "Low": 1})
train["LotShape"] = train["LotShape"].replace({"IR3": 1,"IR2": 2, "IR1": 3, "Reg" : 4})
train["Utilities"] = train["Utilities"].replace({"ELO": 1,"NoSeWa": 2, "NoSewr": 3, "AllPub" : 4})
train["LandSlope"] = train["LandSlope"].replace({"Gtl": 1,"Mod": 2, "Sev": 3})
train["CentralAir"] = train["CentralAir"].replace({"N": 0, "Y": 1})
train["GarageFinish"] = train["GarageFinish"].replace({"None": 0,"Unf": 1, "RFn": 2, "Fin" : 3})

test["GarageCond"] = test["GarageCond"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
test["GarageQual"] = test["GarageQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
test["GarageFinish"] = test["GarageFinish"].replace({"Fin": 3, "RFn": 2, "Unf": 1, "None": 0})
test["FireplaceQu"] = test["FireplaceQu"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
test["KitchenQual"] = test["KitchenQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
test["HeatingQC"] = test["HeatingQC"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
test["BsmtFinType1"] = test["BsmtFinType1"].replace({"GLQ": 6, "ALQ": 5, "BLQ": 4, "Rec": 3, "LwQ": 2, "Unf": 1, "None": 0})
test["BsmtExposure"] = test["BsmtExposure"].replace({"Gd": 5, "Av": 4, "Mn": 3, "No": 2, "None": 1})
test["BsmtCond"] = test["BsmtCond"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
test["BsmtQual"] = test["BsmtQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1, "None": 0})
test["ExterCond"] = test["ExterCond"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
test["ExterQual"] = test["ExterQual"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})
test["HeatingQC"] = test["HeatingQC"].replace({"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1})

test["Street"] = test["Street"].replace({"Grvl": 1, "Paved": 2})
test["LandContour"] = test["LandContour"].replace({"Lvl": 4, "Bnk": 3, "HLS" : 2, "Low": 1})
test["LotShape"] = test["LotShape"].replace({"IR3": 1,"IR2": 2, "IR1": 3, "Reg" : 4})
test["Utilities"] = test["Utilities"].replace({"ELO": 1,"NoSeWa": 2, "NoSewr": 3, "AllPub" : 4})
test["LandSlope"] = test["LandSlope"].replace({"Gtl": 1,"Mod": 2, "Sev": 3})
test["CentralAir"] = test["CentralAir"].replace({"N": 0, "Y": 1})
test["GarageFinish"] = test["GarageFinish"].replace({"None": 0,"Unf": 1, "RFn": 2, "Fin" : 3})

"""### Création de variables"""

#création de dummies pour les catégorielles non ordonnées 
modalities = ['A', 'C', 'FV', 'I', 'RH', 'RL', 'RP', 'RM']

# Fonction pour créer une série de variables dummies
def create_dummies(row, modalities):
    dummies = pd.Series([0] * len(modalities))
    modality = row['MSZoning']
    if modality in modalities:
        dummies[modalities.index(modality)] = 1
    return dummies

# Création des variables dummies sur le TRAIN
dummies_df = train.apply(lambda x: create_dummies(x, modalities), axis=1)
dummies_df.columns = ["MS_zoning_" + modality for modality in modalities]
train = pd.concat([train, dummies_df], axis=1)

# Création des variables dummies sur le TEST
dummies_df = test.apply(lambda x: create_dummies(x, modalities), axis=1)
dummies_df.columns = ["MS_zoning_" + modality for modality in modalities]
test = pd.concat([test, dummies_df], axis=1)

# création de la variable de la modernité de la maison dans TRAIN
# différence entre la date de vente - date de rénovation

train["ModernityInYears"] = train["YrSold"] - train["YearRemodAdd"]
time = train[["YrSold", "YearRemodAdd", "ModernityInYears"]]
### vérifier la cohérence de la soustraction dans un dataframe time
time

test["ModernityInYears"] = test["YrSold"] - test["YearRemodAdd"]

# vérifier qu'elles sont dans le bon type 
print("les variables numériques sont", train.select_dtypes(include=['float64','int64']).columns)
print("les variables catégorielles sont", train.select_dtypes(include=['object']).columns)

train = train.drop(columns=['MSZoning', 'Street', 'LotConfig', 'Neighborhood', 'Condition1',
       'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl',
       'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation',
       'BsmtFinType2', 'Heating', 'Electrical', 'Functional', 'GarageType',
       'GarageYrBlt', 'PavedDrive', 'SaleType', 'SaleCondition', 'MS_zoning_A', 'MS_zoning_C', 'MS_zoning_I', 'MS_zoning_RP'])

test = test.drop(columns=['MSZoning', 'Street', 'LotConfig', 'Neighborhood', 'Condition1',
       'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl',
       'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation',
       'BsmtFinType2', 'Heating', 'Electrical', 'Functional', 'GarageType',
       'GarageYrBlt', 'PavedDrive', 'SaleType', 'SaleCondition', 'MS_zoning_A', 'MS_zoning_C', 'MS_zoning_I', 'MS_zoning_RP'])

"""### Variables corrélées avec la variable cible : avec méthode 1, statistiques univariées"""

import matplotlib.pyplot as plot
import seaborn as sns
import matplotlib.ticker as ticker

train_matrix = train.drop(columns=['Id'])

corr = train_matrix.corr()
fig1 = plot.figure(figsize=(40, 18))
sns.heatmap(train_matrix.corr(), annot=True, annot_kws={'weight':'bold'},fmt=".1", linewidths=.5, cmap='RdPu')

nocorr_features = list(corr[corr['SalePrice']>0.2].index)
nocorr_features

# matrice de corrélation avec les variables dont la corrélation > 0.2 avec la cible
import matplotlib.pyplot as plot
import seaborn as sns
import matplotlib.ticker as ticker

train_matrix = train[['LotFrontage',
 'LotArea',
 'OverallQual',
 'YearBuilt',
 'YearRemodAdd',
 'MasVnrArea',
 'ExterQual',
 'BsmtQual',
 'BsmtCond',
 'BsmtExposure',
 'BsmtFinType1',
 'BsmtFinSF1',
 'BsmtUnfSF',
 'TotalBsmtSF',
 'HeatingQC',
 'CentralAir',
 '1stFlrSF',
 '2ndFlrSF',
 'GrLivArea',
 'BsmtFullBath',
 'FullBath',
 'HalfBath',
 'KitchenQual',
 'TotRmsAbvGrd',
 'Fireplaces',
 'FireplaceQu',
 'GarageFinish',
 'GarageCars',
 'GarageArea',
 'GarageQual',
 'GarageCond',
 'WoodDeckSF',
 'OpenPorchSF',
 'SalePrice',
 'MS_zoning_RL']]

corr = train_matrix.corr()
fig1 = plot.figure(figsize=(40, 18))
sns.heatmap(train_matrix.corr(), annot=True, annot_kws={'weight':'bold'},fmt=".1", linewidths=.5, cmap='RdPu')

"""### Variables corrélées avec la variable cible : avec méthode 2, basée sur un modèle

confirme le tri précédent avec la matrice de corrélation
& permet de préciser dans l'ordre les variables les plus importantes
"""

# Modèle de Forêt Aléatoire pour sélectionner les variables selon la valeur d'importance
from scipy.stats import f_oneway
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor

# Target
y_train = train['SalePrice']

# Data
train_randomForest = train.drop(columns=['Id', 'SalePrice'])

# Modèle
# random_state pour garder le même modèle à chaque relance du code
rf_cat = RandomForestRegressor(n_estimators=100, criterion='mse', max_features='sqrt', random_state=12)
rf_cat.fit(train_randomForest, y_train)

# Graphique des valeurs d'importance - Top 10 des valeurs expliquant le plus la variable cible 
# confirme le tri précédent avec la matrice de corrélation
# permet de préciser dans l'ordre les variables les plus importantes 

rf_cat_feature_importance_df = pd.DataFrame(rf_cat.feature_importances_, train_randomForest.columns, columns=['Importance_Value'])
rf_cat_top10_features = rf_cat_feature_importance_df.sort_values(by = ['Importance_Value'], ascending=False).head(10)

sns.heatmap(data = rf_cat_top10_features, annot=True, cmap="Blues")
plt.title('Variables catégorielles triées selon leur valeur d''importance de la variable')

"""### Variables corrélées avec la variable cible : avec méthode 3,  basée sur l'élimination des caractéristiques récursives (ECR ou RFE en anglais)

https://www.kaggle.com/code/arthurtok/feature-ranking-rfe-random-forest-linear-models
"""

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
import numpy as np

# Target
y_train = train['SalePrice']

# Data
train_randomForest_RFE = train.drop(columns=['Id', 'SalePrice'])

# Définir un dictionnaire pour stocker nos classements
ranks = {}
# Créer notre fonction qui stocke les classements des fonctionnalités dans le dictionnaire des classements
def ranking(ranks, names, order=1):
    minmax = MinMaxScaler()
    ranks = minmax.fit_transform(order*np.array([ranks]).T).T[0]
    ranks = map(lambda x: round(x,2), ranks)
    return dict(zip(names, ranks))

colnames = train_randomForest_RFE.columns

# Enlever les warnings
import warnings
warnings.filterwarnings('ignore')

# Construction du modèle RandomForest
# random_state pour garder le même modèle à chaque relance du code
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
import numpy as np

rf = RandomForestRegressor(n_estimators=100, criterion='mse', max_features='sqrt', random_state = 28)
rf.fit(train_randomForest_RFE, y_train)

# Arrêter l'algorithme lorsqu'il ne reste que la dernière variable
# verbose : faire apparaître ce que l'algorithme fait, 3 pour affichage type slow
rfe = RFE(rf, n_features_to_select=1, verbose = 8)
rfe.fit(train_randomForest_RFE,y_train)

ranks["RFE"] = ranking(list(map(float, rfe.ranking_)), colnames, order=-1)

rfe_data = pd.DataFrame(ranks)
rfe_data = rfe_data[["RFE"]]
rfe_top10_features = rfe_data.sort_values(by = ['RFE'], ascending=False).head(10)
sns.heatmap(data = rfe_top10_features, annot=True, cmap="Blues")
plt.title('Variables catégorielles triées selon leur valeur d''importance de la variable avec RFE')

"""### Variables corrélées entre elles"""

def find_correlated_features(df, threshold=0.3):
    correlated_features = {}
    correlation_matrix = df.corr().abs()
    for column in correlation_matrix.columns:
        correlated_features[column] = list(correlation_matrix.index[correlation_matrix[column] > threshold])
    return correlated_features

correlated_features = find_correlated_features(train_matrix)
for feature, correlated_list in correlated_features.items():
    print(f"{feature} is correlated with: {correlated_list}")

"""### Base finale avec variables sélectionnées"""

train = train[['LotArea',
 'OverallQual',
 'ExterQual',
 'BsmtQual',
 'TotalBsmtSF',
 'HeatingQC',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'KitchenQual',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageCond',
 'WoodDeckSF',
 'OpenPorchSF',
 'SalePrice',
 'MS_zoning_RL',
 'ModernityInYears']]

test = pd.merge(test, sample_submission, on="Id")
test = test[['LotArea',
 'OverallQual',
 'ExterQual',
 'BsmtQual',
 'TotalBsmtSF',
 'HeatingQC',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'KitchenQual',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageCond',
 'WoodDeckSF',
 'OpenPorchSF',
 'SalePrice',
 'MS_zoning_RL',
 'ModernityInYears']]

# Dimensions des sous-ensembles de test et de d'apprentissage
variable_dict = {'table de train': train, 'table de test' : test}
for i in ['table de train', 'table de test']:
    print('Les dimensions (lignes x colonnes) de la %s sont : ' %i, variable_dict[i].shape)

"""# 4. Modèles"""

X_train = train[['LotArea',
 'OverallQual',
 'ExterQual',
 'BsmtQual',
 'TotalBsmtSF',
 'HeatingQC',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'KitchenQual',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageCond',
 'WoodDeckSF',
 'OpenPorchSF',
 'MS_zoning_RL',
 'ModernityInYears']]

y_train = train[['SalePrice']]

X_test = test[['LotArea',
 'OverallQual',
 'ExterQual',
 'BsmtQual',
 'TotalBsmtSF',
 'HeatingQC',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'KitchenQual',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageCond',
 'WoodDeckSF',
 'OpenPorchSF',
 'MS_zoning_RL',
 'ModernityInYears']]

y_test = test[['SalePrice']]

"""### Régression logistique"""

from sklearn.linear_model import LinearRegression 
reg = LinearRegression()
reg.fit(X_train, y_train)
print("Training score ", reg.score(X_train, y_train))
print("Test score ", reg.score(X_test, y_test))

"""# 5. Application

https://www.google.com/search?q=d%C3%A9ployer+un+mod%C3%A8le+Machine+Learning+dans+une+application+web+python&rlz=1C1GCEA_enFR1040FR1040&sxsrf=AJOqlzUoKc2uoDsDPeJ6oE8fX-ylcHoxAA:1676554155784&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmwZv3kpr9AhWXY6QEHYnACsMQ_AUoAXoECAIQAw&biw=1280&bih=569&dpr=1.5#fpstate=ive&vld=cid:b07ffca4,vid:u0Syto1oAGA
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install streamlit

import streamlit as st

st.write('''
# Bienvenue dans l'application
Cet outil permet de prédire le prix de votre futur maison.
''')

st.sidebar.header("Les paramètres d'entrée")

def user_input():
 LotArea=st.sidebar.slider("LotArea", 1000,5000,10000,15000,20000,30000)
 OverallQual("OverallQual", 0,1,2,3,4,5,6,7,8,9,10)
 ExterQual("ExterQual", 0,1,2,3,4,5,6,7,8,9,10)
 BsmtQual("BsmtQual", 0,1,2,3,4,5,6,7,8,9,10)
 TotalBsmtSF("TotalBsmtSF", 1000,2000,3000)
 HeatingQC("HeatingQC", 0,1,2,3,4,5)
 GrLivArea("GrLivArea", 1000,2000,4000)
 FullBath("FullBath", 0,1,2,3)
 HalfBath("HalfBath", 0,1,2,3)
 KitchenQual("KitchenQual", 0,1,2,3,4,5,6,7,8,9,10)
 TotRmsAbvGrd("TotRmsAbvGrd", 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)
 Fireplaces("Fireplaces", 0,1,2,3)
 GarageCars("Fireplaces", 0,1,2,3,4)
 GarageCond("GarageCond", 0,1,2,3,4,5,6,7,8,9,10)
 WoodDeckSF("WoodDeckSF", 0,100,200,300,400,500,600,700,800)
 OpenPorchSF("OpenPorchSF", 0,100,200,300,400,500,600)
 MS_zoning_RL("MS_zoning_RL", 0,1)
 ModernityInYears("ModernityInYears", 0,5,10,20,30,40,50,60)
 
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
    'ModernityInYears':ModernityInYears}
    
    maison_parametre=pd.DataFrame(data,index=[0])

    return maison_parametre
  
df=user_input()

st.subheader("On veut trouver le prix de la maison")
st.write(df)

