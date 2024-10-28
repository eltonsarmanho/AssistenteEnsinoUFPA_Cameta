import pandas as pd
import matplotlib.pyplot as plt

# Dados de exemplo
data = {
    'id': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    'qualidade': [5, 5, 5, 3, 4, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4],
    'tempo': [1, 2, 1, 2, 2, 3, 4, 5, 3, 4, 4, 2, 3, 3, 5]
}

data = pd.read_csv('../dataset/dados_questionario.csv')


df = pd.DataFrame(data)
df.rename(columns={"tempo": "Tempo", "qualidade": "Qualidade"},inplace=True)

metrica = 'Tempo'
# Calcular as porcentagens de cada valor de qualidade
qualidade_percent = df[metrica].value_counts(normalize=True).sort_index() * 100

# Gerar gráfico de barras da distribuição de qualidade em porcentagem
plt.figure(figsize=(8, 6))
qualidade_percent.plot(kind='bar', color='skyblue')
plt.title('Distribuição do {0} da Resposta (%)'.format(metrica),fontsize=14)
plt.xlabel('{0} (1 a 5)'.format(metrica),fontsize=14)
plt.ylabel('Porcentagem de Avaliações (%)',fontsize=14)
plt.xticks(fontsize=14)  # Aumentar o tamanho das marcas no eixo X
plt.yticks(fontsize=14)  # Aumentar o tamanho das marcas no eixo Y
plt.grid(False)

# Exibir o gráfico
plt.show()
