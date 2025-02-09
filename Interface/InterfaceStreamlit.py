
import pandas as pd
import streamlit as st
import time

from LLM.AgenteLLM import QAGenerator
from Load.QuestionarioFirebase import QuestionarioFirebase
from Similaridade.VerificadorDePerguntas import VerificadorDePerguntas

from streamlit.web import cli as stcli
from streamlit import runtime
import sys
import os


# Abra e leia o arquivo csv
project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
file_path_dataset = os.path.join(project_root, '..', 'dataset', 'dataset.csv')

# Parâmetros de conexão ao Firebase
file = "coletadados-f1884-firebase-adminsdk-itqt9-73bd934db1.json"
project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
cred_path = os.path.join(project_root, '..', 'Keys', file)
database_url = "https://coletadados-f1884-default-rtdb.firebaseio.com/"
# Instancia a classe e conecta ao Firebase
db = QuestionarioFirebase(cred_path, database_url)
    # Conecta ao Firebase
db.conectar()
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

    llm = QAGenerator(n_perguntas=3,arquivo_csv=file_path_dataset)

    # Carregar dataset (ou criar novo)
    try:

        df = pd.read_csv(file_path_dataset)
    except FileNotFoundError as e:
        print(e)
        df = pd.DataFrame(columns=['original_pergunta','Pergunta', 'Resposta'])

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
                    resultado = llm.generate_qa(pergunta)
                    fim = time.time()
                    st.success("Nova pergunta gerada!")
                    st.write(f"**Pergunta:** {resultado[0]['pergunta']}")
                    st.write(f"**Resposta:** {resultado[0]['resposta']}")

                tempo_requisicao = (fim - inicio)*1000
                db.inserir_dados_requisicoes(pergunta, tempo_requisicao)

        if pergunta:
            if st.button("Avaliar Resposta"):
                # Atualiza estado da sessão para mudar a página
                st.session_state.page = 'avaliacao'  # Ir para a página de avaliação
                st.rerun()  # Recarrega a página para refletir a mudança de estado
        #else: #st.warning( #   "Por favor, insira uma pergunta antes de tentar avaliar a resposta.")  # Exibe um alerta se a pergunta estiver vazia


    elif escolha == "Histórico":
        st.subheader("Histórico de Perguntas e Respostas")

        df = pd.read_csv(file_path_dataset)
        st.dataframe(df[['pergunta', 'resposta']], height=400)

# Função para a página de avaliação
def pagina_avaliacao():
    st.title("Avaliação da Resposta")

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
            db.inserir_dados_questionario(qualidade_resposta, tempo_resposta)
        except Exception as error:
            print(f"Erro: {error}")

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