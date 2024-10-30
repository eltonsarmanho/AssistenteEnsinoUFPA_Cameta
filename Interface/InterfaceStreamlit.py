import streamlit as st
import pandas as pd
import time

from LLM.LLMHandler import LLMHandler
from Load.QuestionarioDB import QuestionarioDB
from Similaridade.VerificadorDePerguntas import VerificadorDePerguntas

from streamlit.web import cli as stcli
from streamlit import runtime
import sys
import os
import json

# Abra e leia o arquivo JSON
# Caminho absoluto para o arquivo JSON
project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
file_path = os.path.join(project_root,'..' ,'Keys', 'config.json')

# Abra e leia o arquivo JSON
with open(file_path, 'r') as file:
    config = json.load(file)
# Acesse os valores no dicionário
host = config['host']
port = config['port']
dbname = config['dbname']
user = config['user']
password = config['password']
minha_chave = config['minha_chave']

project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
file_path_dataset = os.path.join(project_root, '..', 'dataset', 'dataset.csv')

db = QuestionarioDB(host, port, dbname, user, password)
# Função principal que gera a interface com Streamlit
def main():
    st.set_page_config(page_title="Sistema de Perguntas e Respostas", layout="wide")

    # Inicializar página
    if 'page' not in st.session_state:
        st.session_state.page = 'perguntas'  # Página inicial é o sistema de perguntas

    # Barra lateral para navegação
    escolha = st.sidebar.radio("Navegar", ["Sistema de Perguntas", "Histórico"])

    # Definir qual página mostrar
    if st.session_state.page == 'perguntas':
        sistema_perguntas(escolha)
    elif st.session_state.page == 'avaliacao':
        pagina_avaliacao()

# Função para a página do sistema de perguntas
def sistema_perguntas(escolha):
    st.title("🧠 Sistema de Perguntas e Respostas")


    llm = LLMHandler(minha_chave)

    # Carregar dataset (ou criar novo)
    try:
        df = pd.read_csv(file_path_dataset)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Pergunta', 'Resposta'])

    if escolha == "Sistema de Perguntas":
        st.subheader("Faça sua pergunta")
        pergunta = st.text_input("Digite sua pergunta:")

        if st.button("Enviar"):
            if pergunta:
                # Mostrar barra de progresso
                with st.spinner('Gerando resposta...'):
                    time.sleep(1)  # Simulação de tempo de processamento

                # Verificar se já existe uma pergunta similar
                inicio = time.time()
                check = VerificadorDePerguntas(df, threshold=0.75)
                pergunta_similar, resposta_similar = check.verificar_similaridade(pergunta)

                if pergunta_similar:
                    fim = time.time()
                    st.success("Pergunta similar encontrada!")
                    st.write(f"**Pergunta:** {pergunta_similar}")
                    st.write(f"**Resposta:** {resposta_similar}")
                else:
                    # Gerar nova resposta e atualizar dataset
                    pergunta, resposta, df = llm.gerar_perguntas_e_atualizar_dataset(df, pergunta, 3)
                    fim = time.time()
                    st.success("Nova pergunta gerada!")
                    st.write(f"**Pergunta:** {pergunta}")
                    st.write(f"**Resposta:** {resposta}")
                    df.to_csv('dataset.csv', index=False)
                tempo_requisicao = (fim - inicio)*1000
                db.conectar()
                db.inserir_dados_requisicoes(pergunta, tempo_requisicao)
                db.fechar_conexao()

        if pergunta:
            if st.button("Avaliar Resposta"):
                # Atualiza estado da sessão para mudar a página
                st.session_state.page = 'avaliacao'  # Ir para a página de avaliação
                st.rerun()  # Recarrega a página para refletir a mudança de estado
        #else: #st.warning( #   "Por favor, insira uma pergunta antes de tentar avaliar a resposta.")  # Exibe um alerta se a pergunta estiver vazia


    elif escolha == "Histórico":
        st.subheader("Histórico de Perguntas e Respostas")

        df = pd.read_csv(file_path_dataset)
        df_historico = df[df['Classe'] == 1]
        df_historico = df_historico.drop('Classe', axis=1)
        st.dataframe(df_historico, height=400)

# Função para a página de avaliação
def pagina_avaliacao():
    st.title("Avaliação da Resposta")

    db.conectar()
    st.subheader("Avalie a resposta que você recebeu")
    col1, col2 = st.columns(2)

    with col1:
        # Avaliação de qualidade da resposta
        st.write("Qualidade da resposta:")
        qualidade_resposta = st.radio("Avalie de 1 a 5 estrelas", [1, 2, 3, 4, 5], index=2, key="qualidade")

    with col2:
        # Avaliação do tempo de resposta
        st.write("Tempo de resposta:")
        tempo_resposta = st.radio("Avalie de 1 a 5 estrelas", [1, 2, 3, 4, 5], index=2, key="tempo")

    # Botão para enviar avaliação e voltar para o sistema de perguntas
    if st.button("Enviar Avaliação"):
        try:
        # Insere dados na tabela Questionario
            db.inserir_dados(qualidade_resposta, tempo_resposta)
        except Exception as error:
            print(f"Erro: {error}")
        finally: db.fechar_conexao()
        st.write(f"Você avaliou a **qualidade** da resposta com {qualidade_resposta} estrelas.")
        st.write(f"Você avaliou o **tempo** de resposta com {tempo_resposta} estrelas.")
        st.session_state.page = 'perguntas'  # Retorna à página de perguntas após avaliar
        with st.spinner('Registrando Avaliação...'):
            time.sleep(3)  # Simulação de tempo de processamento
        st.rerun()  # Recarrega a página para refletir a mudança de estado

if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())