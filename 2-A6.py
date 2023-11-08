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

#Colunas para não plotar
colunas_excluir = ['age','gender','cholesterol','gluc','smoke','alco','active','cardio']

#Para armazenados dados
valores_estat = {}
valores_estat_amostrais = {}

#Dados Amostrais e tamanho
coluna_amostral = ['age', 'gluc', 'smoke', 'cardio'] # colunas para amostrar
n_amostral = 100 # quantidade n de amostras (100 mil é o exercícios, fazer os testes com menos, python demora)
tamanho_amostral = [5,35] # tamanhos de cada amostra
amostras = {} #dic/armazenamento

# Itere sobre as colunas
for coluna in df.columns:

    data = df[coluna].dropna()
    media = data.mean() # media da coluna
    desvio = data.std() # desvio padra da coluna
    variancia = data.var() # variancia da coluna
    valores_estat[coluna] = (media, variancia, desvio) # coleta dos parametros da população

    x = np.linspace(data.min(), data.max(), 100)
    y = (1 / (np.sqrt(2 * np.pi * variancia))) * np.exp(-0.5 * ((x - media) / np.sqrt(variancia)) ** 2)

    if coluna not in colunas_excluir:
        plt.figure(figsize=(8, 6))  # Ajuste o tamanho da figura conforme necessário
        plt.plot(x, y, color='r', linewidth=2)
        plt.hist(data, bins=50, density=True, alpha=0.6, color='b')
        plt.axvline(x=media, color='g', linestyle='--', label=f'Média: {media:.2f}') # Adicionar uma linha vertical representando a média
        #plt.title(f'Distribuição Normal - {coluna}')
        plt.xlabel('Valores')
        plt.ylabel('Densidade')
        # Adicionar valor esperado e variância no título
        plt.title(f'Distribuição Normal - {coluna}\nValor Esperado: {media:.2f}, Variância: {desvio:.2f}²')
        plt.legend(['Distribuição Normal', 'Média', 'Dados'])

        # Salvar a figura em um diretório específico
        nome_do_arquivo = f'distribuicao_{coluna}.png'
        caminho_para_salvar = 'Figuras/' + nome_do_arquivo
        plt.savefig(caminho_para_salvar)

        #plt.show()

# Coleta da amostras
for colunas in coluna_amostral: # coleta da amostragem da colunas
    amostras[coluna] = {}
    for tamanho in tamanho_amostral: # para cada coluna, tamanhos_amostral
        amostras[coluna][tamanho] = []
        for _ in range(n_amostral): # faz n vezes
            amostra = df[coluna].sample(n=tamanho, replace=True).values
            amostras[coluna][tamanho].append(amostra)
pprint(valores_estat)

for coluna in coluna_amostral:
    valores_estat_amostrais[coluna] = {}
    for tamanho in tamanho_amostral:
        valores_estat_amostrais[coluna][tamanho] = {
            "media": [],
            "variancia": [],
            "desvio padrão": []
        }
        for i in range(n_amostral):
            amostra = amostras[coluna][tamanho][i]
            media = np.mean(amostra)
            variancia = np.var(amostra)
            desvio = np.std(amostra)
            valores_estat_amostrais[coluna][tamanho]["media"].append(media)
            valores_estat_amostrais[coluna][tamanho]["variancia"].append(variancia)
            valores_estat_amostrais[coluna][tamanho]["desvio"].append(desvio)

sns.histplot(valores_estat_amostrais['alco'][5]['media'], kde=true)
plt.hist("Média")
plt.title("Histograma da Média (Coluna 3, Tamanho 5)")
plt.show()
