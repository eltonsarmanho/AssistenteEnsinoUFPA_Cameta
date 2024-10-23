import streamlit as st
import pandas as pd
import time

from LLM.LLMHandler import LLMHandler
from Similaridade.VerificadorDePerguntas import VerificadorDePerguntas

from streamlit.web import cli as stcli
from streamlit import runtime
import sys


# Função principal que gera a interface com Streamlit
def main():
    st.set_page_config(page_title="Sistema de Perguntas e Respostas", layout="wide")

    st.title("🧠 Sistema de Perguntas e Respostas")

    minha_chave = "100088405894968274443$48d83f597eed3dac55ca7ab70e8d6d46628784d793046bf36006985b4d18354e"
    llm = LLMHandler(minha_chave)

    # Carregar dataset (ou criar novo)
    try:
        df = pd.read_csv('../dataset/dataset.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Pergunta', 'Resposta'])

    # Barra lateral para navegação
    escolha = st.sidebar.radio("Navegar", ["Sistema de Perguntas", "Histórico"])

    if escolha == "Sistema de Perguntas":
        st.subheader("Faça sua pergunta")
        pergunta = st.text_input("Digite sua pergunta:")

        if st.button("Enviar"):
            if pergunta:
                # Mostrar barra de progresso
                with st.spinner('Gerando resposta...'):
                    time.sleep(1)  # Simulação de tempo de processamento

                # Verificar se já existe uma pergunta similar
                check = VerificadorDePerguntas(df, threshold=0.75)
                pergunta_similar, resposta_similar = check.verificar_similaridade(pergunta)

                if pergunta_similar:
                    st.success("Pergunta similar encontrada!")
                    st.write(f"**Pergunta:** {pergunta_similar}")
                    st.write(f"**Resposta:** {resposta_similar}")
                else:
                    # Gerar nova resposta e atualizar dataset
                    pergunta, resposta, df = llm.gerar_perguntas_e_atualizar_dataset(df, pergunta, 3)
                    st.success("Nova pergunta gerada!")
                    st.write(f"**Pergunta:** {pergunta}")
                    st.write(f"**Resposta:** {resposta}")
                    df.to_csv('../dataset/dataset.csv', index=False)
            else:
                st.warning("Por favor, insira uma pergunta antes de enviar.")

    elif escolha == "Histórico":
        st.subheader("Histórico de Perguntas e Respostas")
        df = pd.read_csv('../dataset/dataset.csv')
        df_historico = df[df['Classe']==1]
        df_historico = df_historico.drop('Classe',axis=1)
        st.dataframe(df_historico, height=400)


if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())