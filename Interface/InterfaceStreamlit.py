import sys
import os
#Add Raiz ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import streamlit as st
import time
from Database.ConexaoFirebase import ConexaoFirebase
from LLM.QAGenerator import QAGenerator
from Similaridade.VerificadorDePerguntas import VerificadorDePerguntas
from streamlit.web import cli as stcli
from streamlit import runtime
import json

def loadConfig():
    

    project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do json atual
    cred_path = os.path.join(project_root,'..', 'Keys', 'coletadados-firebase.json')
    with open(cred_path, 'r') as file:
        config = json.load(file)
    # Acesse os valores no dicionário
    database_url = config['database_url']
    # Instancia a classe e conecta ao Firebase
    db = ConexaoFirebase(cred_path, database_url)
    # Conecta ao Firebase
    db.conectar()
# Função principal que gera a interface com Streamlit
def main():

    loadConfig()
    st.set_page_config(page_title="Sistema de Perguntas e Respostas", layout="wide")

    # Inicializar o gerador LLM uma única vez
    if 'llm' not in st.session_state:
        st.session_state.llm = QAGenerator(n_perguntas=3,model_name='google')  # Instância única
        #st.session_state['llm'] = QAGenerator(n_perguntas=3)  # Instância única

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

    if escolha == "Sistema de Perguntas":
        st.subheader("Faça sua pergunta")
        pergunta = st.text_input("Digite sua pergunta:")

        if st.button("Enviar"):
            if pergunta:
                # Mostrar barra de progresso
                with st.spinner('Gerando resposta...'):
                    time.sleep(1)  # Simulação de tempo de processamento

                # Verificar se já existe uma pergunta similar
                df = db.get_dados_questoes()
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
                    resultado = st.session_state.llm.generate_qa(pergunta)  # Modificação aqui

                    fim = time.time()
                    st.success("Nova pergunta gerada!")
                    st.write(f"**Pergunta:** {resultado[0]['pergunta']}")
                    st.write(f"**Resposta:** {resultado[0]['resposta']}")
                    # Armazena no session_state
                    st.session_state.pergunta_atual = resultado[0]['pergunta']
                    st.session_state.resposta_atual = resultado[0]['resposta']
                    st.session_state.resultado = resultado


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

        df = db.get_dados_questoes()
        st.dataframe(df[['Pergunta', 'Resposta']], height=400)

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

    # Opção para reportar erro
    st.subheader("Reportar Erro")
    erro_reportado = st.checkbox("A resposta estava incorreta ou insuficiente?")
    if erro_reportado:
        # Recupera a pergunta e resposta do session_state
        pergunta = st.session_state.get('pergunta_atual', None)
        resposta = st.session_state.get('resposta_atual', None)
        st.write("Por favor, forneça mais detalhes sobre o erro:")
        detalhes_erro = st.text_area("Detalhes do erro:")
        if st.button("Enviar Relatório de Erro"):
            try:
                # Salva a resposta incorreta no Firebase
                db.inserir_dados_resposta_incorreta(pergunta, resposta)
                st.success("Erro reportado com sucesso! Uma nova resposta será gerada.")

                # Gera uma nova resposta revisada
                nova_resposta = st.session_state.llm.gerar_resposta_revisada(pergunta, contexto_adicional=detalhes_erro)
                st.write("**Nova Resposta Revisada:**")
                st.write(nova_resposta)

                # Atualiza a resposta no Firebase
                db.substituir_resposta_corrigida(pergunta, nova_resposta)
                st.success("Resposta corrigida atualizada no sistema!")
            except Exception as error:
                st.error(f"Erro ao processar o relatório de erro: {error}")

    # Botão para enviar avaliação normal
    if st.button("Enviar Avaliação"):
        try:
           resultado = st.session_state.resultado
           for i, par in enumerate(resultado, 1):
                db.inserir_dados_questao(par['pergunta'], par['resposta'])
           db.inserir_dados_questionario(qualidade_resposta, tempo_resposta)
           # Iniciar thread
           st.write(f"Você avaliou a **qualidade** da resposta com {qualidade_resposta} estrelas.")
           st.write(f"Você avaliou o **tempo** de resposta com {tempo_resposta} estrelas.")
           st.session_state.page = 'perguntas'
           with st.spinner('Registrando Avaliação...'):
               time.sleep(3)
           st.rerun()
        except Exception as error:
            st.error(f"Erro ao registrar avaliação: {error}")

if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())