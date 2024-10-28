import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar o CSV
data = pd.read_csv('../dataset/dados_requisicoes_categoria.csv')

# Converter o tempo de resposta de milissegundos para segundos
class_0_data = data[data['Classe'] == 0]['tempo_requisicao'] / 1000
class_1_data = data[data['Classe'] == 1]['tempo_requisicao'] / 1000

# Plotar o histograma para Classe 0 - MVR
plt.figure(figsize=(10, 6))
plt.hist(class_0_data, bins=20, color='skyblue', edgecolor='black')
plt.title("Histograma do Tempo de Resposta para MVR (Classe 0)", fontsize=14)
plt.xlabel("Tempo de Resposta (s)", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Plotar o histograma para Classe 1 - Sabiá 2.0
plt.figure(figsize=(10, 6))
plt.hist(class_1_data, bins=20, color='salmon', edgecolor='black')
plt.title("Histograma do Tempo de Resposta para Modelo Sabiá 2.0 (Classe 1)", fontsize=14)
plt.xlabel("Tempo de Resposta (s)", fontsize=14)
plt.ylabel("Frequência", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
