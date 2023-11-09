import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import seaborn as sns
from pprint import pprint

# Carregue os dados do arquivo CSV em um DataFrame
df = pd.read_csv("cardiovascular_data.csv", sep=';', encoding='utf-8')

# Converter a coluna de idade de dias para anos (supondo 365 dias por ano)
df['age_y'] = df['age']/365 

# Remover valores muito elevados das colunas especificar
limite_superior_hi = 450  # Define o limite superior para ap_hi
limite_superior_lo = 300  # Define o limite superior para ap_lo
df['ap_hi'] = df['ap_hi'].apply(lambda x: x if x <= limite_superior_hi else np.nan)
df['ap_lo'] = df['ap_lo'].apply(lambda x: x if x <= limite_superior_lo else np.nan)

#Colunas para não plotar diretamente
colunas_bin = ['age','gender','cholesterol','gluc','smoke','alco','active','cardio']

#Para armazenados dados
valores_estat_pop = {}
valores_estat_amostrais = {}

#Dados Amostrais e tamanho
coluna_amostral = ['age', 'gluc', 'smoke', 'alco', 'cardio'] # colunas para amostrar
n_amostral = 1 # quantidade n de amostras (100 mil é o exercícios, fazer os testes com menos, python demora)
tamanho_amostral = [5,35] # tamanhos de cada amostra
amostras_pop = {} #dic/armazenamento

for col in df.columns:

    data = df[col].dropna()
    media = data.mean()
    variancia = data.var()
    desvio = data.std()
    valores_estat_pop[col] = (media, variancia, desvio) #armazenando dados populacionais
    
    #Inicio
    amostras_pop[col] = {}
    valores_estat_amostrais[col] = {}

    # Coleta das amostras
    for tamanho in tamanho_amostral:
        amostras_pop[col][tamanho] = []
        valores_estat_amostrais[col][tamanho] = {"media": [], "variancia": [], "desvio": []}

        for _ in range(n_amostral):
            amostra = df[col].sample(n = tamanho, replace=True).values
            amostras_pop[col][tamanho].append(amostra)

            media_amostral = np.mean(amostra)
            variancia_amostral = np.var(amostra)
            desvio_amostral = np.std(amostra)

            valores_estat_amostrais[col][tamanho]["media"].append(media_amostral)
            valores_estat_amostrais[col][tamanho]["variancia"].append(variancia_amostral)
            valores_estat_amostrais[col][tamanho]["desvio"].append(desvio_amostral)

pprint(valores_estat_pop)
pprint(valores_estat_amostrais)