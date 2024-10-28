import pandas as pd
import time

from LLMHandler import LLMHandler
from Similaridade.VerificadorDePerguntas import VerificadorDePerguntas
import json



if __name__ == '__main__':
    # Carregar dataset (ou criar novo)
    # Abra e leia o arquivo JSON
    with open('Keys/config.json', 'r') as file:
        config = json.load(file)

    minha_chave = config['minha_chave']
    modelo = LLMHandler(minha_chave)
    dados_requisicoes_categoria = pd.DataFrame(columns=['Pergunta', 'tempo_requisicao','Classe'])
    try:

        dados_requisicoes = pd.read_csv('../dataset/dados_requisicoes.csv')
    except FileNotFoundError:
        dados_requisicoes = pd.DataFrame(columns=['Pergunta', 'Resposta'])

    df = pd.read_csv('../dataset.csv')
    perguntas = dados_requisicoes['pergunta']
    for pergunta in perguntas:
        check = VerificadorDePerguntas(df, threshold=0.75)
        inicio = time.time()
        pergunta_similar, resposta_similar = check.verificar_similaridade(pergunta)

        if pergunta_similar:
            classe = 0
            fim = time.time()
            print("Pergunta similar encontrada!")
        else:
            classe = 1
            # Gerar nova resposta e atualizar dataset
            resposta= modelo.pergunta_llm(pergunta)
            novo_registro_data = {'Pergunta': pergunta, 'Resposta': resposta, 'Classe': classe}
            df = df._append(novo_registro_data, ignore_index=True)
            fim = time.time()
            print("Nova pergunta gerada!")


        tempo_requisicao = (fim - inicio) * 1000
        novo_registro = {'Pergunta': pergunta, 'tempo_requisicao': tempo_requisicao, 'Classe': classe}
        dados_requisicoes_categoria = dados_requisicoes_categoria._append(novo_registro, ignore_index=True)
    dados_requisicoes_categoria.to_csv('../dados_requisicoes_categoria.csv', index=False)
    df.to_csv('../dataset.csv', index=False)