import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

df = pd.read_csv('cardiovascular_data.csv', sep=';', encoding='utf-8') #importando o CSV/dados

df['age_y'] = df['age']/365 #convertendo coluna dia --> ano

limite_superior = 250
df['ap_hi'] = df['ap_hi'].apply(lambda x: x if x <= limite_superior else np.nan)
df['ap_lo'] = df['ap_lo'].apply(lambda x: x if x <= limite_superior else np.nan)

for coluna in df.columns:
    if coluna == 'age':
        continue  # Pular a coluna de idade em dias

    plt.figure(figsize=(6, 4))  # Ajuste o tamanho da figura conforme necessário
    plt.hist(df[coluna], bins=30, density=True, alpha=0.6, color='b')

    if coluna == 'age':
        media = df['age_y'].mean()
        variancia = df['age_y'].var()
        desvio_padrao = df['age_y'].std()
        plt.xticks(np.arange(0, df['age_y'].max(), step=5))  # Ajuste o intervalo dos ticks do eixo x

    else:
        # Calcule a média e o desvio padrão da coluna
        media = df[coluna].mean()
        variancia = df[coluna].var()
        desvio_padrao = df[coluna].std()
    

    # Crie uma curva de distribuição normal usando a média e o desvio padrão
    x = np.linspace(df[coluna].min(), df[coluna].max(), 100)
    y = (1 / (desvio_padrao * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / desvio_padrao) ** 2)
    plt.plot(x, y, color='r', linewidth=2)

    plt.title(f'Distribuição Normal - {coluna}')
    plt.xlabel('Valores')
    plt.ylabel('Densidade')
    plt.legend(['Distribuição Normal', 'Dados'])

    # Salvar a figura em um diretório específico
    nome_do_arquivo = f'distribuicao_{coluna}.png'
    caminho_para_salvar = 'Figuras/' + nome_do_arquivo
    plt.savefig(caminho_para_salvar)

    plt.show()
    

