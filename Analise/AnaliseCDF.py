import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Dados de exemplo

data = pd.read_csv('../dataset/dados_requisicoes_categoria.csv')
print(data)
# Converter o tempo de resposta de milissegundos para segundos
class_0_data = data[data['Classe'] == 0]['tempo_requisicao']
class_1_data = data[data['Classe'] == 1]['tempo_requisicao']

# Função para calcular a CDF
def calculate_cdf(data):
    sorted_data = np.sort(data)
    y_vals = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    return sorted_data, y_vals

# Calcular a CDF para cada classe
class_0_sorted, class_0_cdf = calculate_cdf(class_0_data / 1000)  # Conversão para segundos
class_1_sorted, class_1_cdf = calculate_cdf(class_1_data / 1000)  # Conversão para segundos

# Plotar o gráfico da CDF para Classe 0
plt.figure(figsize=(10, 6))
plt.plot(class_0_sorted, class_0_cdf, label="MVR", linewidth=2)
plt.title("Função de Distribuição Acumulada (CDF) para MVR",fontsize=14)
plt.xlabel("Tempo de Resposta (s)",fontsize=14)
plt.ylabel("Probabilidade Acumulada (%)",fontsize=14)
plt.legend()
plt.grid(True)
plt.show()

# Plotar o gráfico da CDF para Classe 1
plt.figure(figsize=(10, 6))
plt.plot(class_1_sorted, class_1_cdf, label="Sabiá 2.0", linewidth=2)
plt.title("Função de Distribuição Acumulada (CDF) para Modelo Sabiá 2.0",fontsize=14)
plt.xlabel("Tempo de Resposta (s)",fontsize=14)
plt.ylabel("Probabilidade Acumulada (%)",fontsize=14)
plt.legend()
plt.grid(True)
plt.show()
