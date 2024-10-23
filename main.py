
#conteudo = "quais os problemas com o não cumprimento da LGPD?" #PERGUNTA QUE NÃO TEM NA BASE DE DADOS - SEMELHANTE
#conteudo = 'O que é a LGPD?' #PERGUNTA QUE NÃO TEM NA BASE DE DADOS - IDENTICA
#conteudo = 'Qual a Diferença entre controlador e operador de dados na LGPD?' # PERGUNTA QUE NÃO TEM NA BASE DE DADOS
#conteudo = 'Como utilizar algoritmos de IA?' # PERGUNTA NADA HAVER
#conteudo = 'Cite três tipos de Banco de Dados.' # PERGUNTA NADA HAVER

import pandas as pd

from LLM.llm import gerar_perguntas_e_atualizar_dataset
from Similaridade.VerificadorDePerguntas import VerificadorDePerguntas

df = pd.read_csv('dataset/dataset.csv')
pergunta = 'Como utilizar algoritmos de IA?'#input("Faça sua pergunta: ")

check = VerificadorDePerguntas(df, threshold=0.75);
pergunta_similar, resposta_similar = check.verificar_similaridade(pergunta);

if(pergunta_similar):
        print(f"Pergunta similar encontrada no dataset: {pergunta_similar}")
        print(f"Resposta associada: {resposta_similar}\n")
else:   gerar_perguntas_e_atualizar_dataset(df, pergunta, 3)  # Gerar 5 novas perguntas



