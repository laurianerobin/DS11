{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOloEnQIwdE3C4QBnaa6YsX",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/laurianerobin/DS11/blob/main/test.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "https://www.google.com/search?q=d%C3%A9ployer+un+mod%C3%A8le+Machine+Learning+dans+une+application+web+python&rlz=1C1GCEA_enFR1040FR1040&sxsrf=AJOqlzUoKc2uoDsDPeJ6oE8fX-ylcHoxAA:1676554155784&source=lnms&tbm=vid&sa=X&ved=2ahUKEwjmwZv3kpr9AhWXY6QEHYnACsMQ_AUoAXoECAIQAw&biw=1280&bih=569&dpr=1.5#fpstate=ive&vld=cid:b07ffca4,vid:u0Syto1oAGA"
      ],
      "metadata": {
        "id": "mWev83xWdVAA"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import pandas as pd"
      ],
      "metadata": {
        "id": "Q2dVrDoldQdo"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "st.write('''\n",
        "# Bienvenue dans l'application\n",
        "Cet outil permet de prédire le prix de votre futur maison.\n",
        "''')\n",
        "\n",
        "st.sidebar.header(\"Les paramètres d'entrée\")\n",
        "\n",
        "def user_input():\n",
        "  LotArea=st.sidebar.slider(\"LotArea\", 1000,30000)\n",
        "  OverallQual=st.sidebar.slider(\"OverallQual\", 0,10)\n",
        "  ExterQual=st.sidebar.slider(\"ExterQual\", 0,10)\n",
        "  BsmtQual=st.sidebar.slider(\"BsmtQual\", 0,10)\n",
        "  TotalBsmtSF=st.sidebar.slider(\"TotalBsmtSF\", 1000,3000)\n",
        "  HeatingQC=st.sidebar.slider(\"HeatingQC\", 0,5)\n",
        "  GrLivArea=st.sidebar.slider(\"GrLivArea\", 1000,4000)\n",
        "  FullBath=st.sidebar.slider(\"FullBath\", 0,3)\n",
        "  HalfBath=st.sidebar.slider(\"HalfBath\", 0,3)\n",
        "  KitchenQual=st.sidebar.slider(\"KitchenQual\", 0,10)\n",
        "  TotRmsAbvGrd=st.sidebar.slider(\"TotRmsAbvGrd\", 0,14)\n",
        "  Fireplaces=st.sidebar.slider(\"Fireplaces\", 0,3)\n",
        "  GarageCars=st.sidebar.slider(\"Fireplaces\", 0,4)\n",
        "  GarageCond=st.sidebar.slider(\"GarageCond\", 0,10)\n",
        "  WoodDeckSF=st.sidebar.slider(\"WoodDeckSF\", 0,800)\n",
        "  OpenPorchSF=st.sidebar.slider(\"OpenPorchSF\", 0,600)\n",
        "  MS_zoning_RL=st.sidebar.slider(\"MS_zoning_RL\", 0,1)\n",
        "  ModernityInYears=st.sidebar.slider(\"ModernityInYears\", 0,60)\n",
        " \n",
        "  data={\n",
        "        'LotArea':LotArea,\n",
        "        'OverallQual':OverallQual,\n",
        "        'ExterQual':ExterQual,\n",
        "        'BsmtQual':BsmtQual,\n",
        "        'TotalBsmtSF':TotalBsmtSF,\n",
        "        'HeatingQC':HeatingQC,\n",
        "        'GrLivArea':GrLivArea,\n",
        "        'FullBath':FullBath,\n",
        "        'HalfBath':HalfBath,\n",
        "        'KitchenQual':KitchenQual,\n",
        "        'TotRmsAbvGrd':TotRmsAbvGrd,\n",
        "        'Fireplaces':Fireplaces,\n",
        "        'GarageCars':GarageCars,\n",
        "        'GarageCond':GarageCond,\n",
        "        'WoodDeckSF':WoodDeckSF,\n",
        "        'OpenPorchSF':OpenPorchSF,\n",
        "        'MS_zoning_RL':MS_zoning_RL,\n",
        "        'ModernityInYears':ModernityInYears\n",
        "        }\n",
        "  maison_parametre=pd.DataFrame(data,index=[0])\n",
        "  return maison_parametre\n",
        "  \n",
        "df=user_input()\n",
        "\n",
        "st.subheader(\"On veut trouver le prix de la maison\")\n",
        "st.write(df)"
      ],
      "metadata": {
        "id": "8AruHS7TdUNh"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "url_Xtrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/X_train.csv'\n",
        "X_train = pd.read_csv(url_Xtrain,parse_dates=[0])\n",
        "\n",
        "url_ytrain = 'https://raw.githubusercontent.com/laurianerobin/DS11/main/y_train.csv'\n",
        "y_train = pd.read_csv(url_ytrain,parse_dates=[0])"
      ],
      "metadata": {
        "id": "AccD59YFdh69"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from sklearn.linear_model import LinearRegression \n",
        "reg = LinearRegression()\n",
        "reg.fit(X_train, y_train)\n",
        "\n",
        "prediction=reg.predict(df)\n",
        "\n",
        "st.subheader(\"Le prix de la maison est :\")\n",
        "st.write(prediction)"
      ],
      "metadata": {
        "id": "ylkFUCozo9fG"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "mxNLq2f93gC3"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}