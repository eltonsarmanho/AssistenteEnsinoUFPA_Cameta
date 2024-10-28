import pandas as pd
import matplotlib.pyplot as plt

# Dados de exemplo
data = pd.read_csv('../dataset/dados_questionario.csv')
df = pd.DataFrame(data)
df.rename(columns={"tempo": "Tempo", "qualidade": "Qualidade"},inplace=True)

# Agrupar dados por 'tempo' e calcular a média de 'qualidade' para cada grupo
satisfacao_por_tempo = df.groupby('Tempo')['Qualidade'].mean()

# Plotar os resultados
plt.figure(figsize=(8, 6))
satisfacao_por_tempo.plot(kind='bar', color='skyblue')
plt.title('Satisfação por Tempo de Resposta',fontsize=14)
plt.xlabel('Tempo de Resposta (1 a 5)',fontsize=14)
plt.ylabel('Satisfação',fontsize=14)
plt.xticks(rotation=0, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)

# Mostrar o gráfico
plt.show()
