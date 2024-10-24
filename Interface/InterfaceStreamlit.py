import streamlit as st
import pandas as pd
import numpy as np

# Título do aplicativo
st.title("Meu Primeiro App no Streamlit")

# Subtítulo
st.subheader("Exemplo de um app básico")

# Texto de introdução
st.write("Este é um aplicativo de exemplo usando Streamlit.")

# Slider para entrada do usuário
valor = st.slider("Selecione um valor", 0, 100, 50)

# Mostrar o valor selecionado
st.write(f"Você selecionou: {valor}")

# Exemplo de tabela de dados
dados = pd.DataFrame({
    'coluna 1': np.random.randn(10),
    'coluna 2': np.random.randn(10)
})

# Mostrar tabela
st.write("Aqui está uma tabela de dados aleatórios:")
st.dataframe(dados)

# Gráfico de linha
st.line_chart(dados)

# Exibir um gráfico interativo
st.write("Gráfico interativo de barras:")
st.bar_chart(dados)

# Checkbox para exibir mensagem
if st.checkbox("Mostrar mensagem"):
    st.write("Checkbox marcado! Aqui está sua mensagem.")

# Entrada de texto
nome = st.text_input("Digite seu nome", "Digite aqui...")
st.write(f"Olá, {nome}!")

# Botão
if st.button("Clique aqui"):
    st.write("Botão clicado!")

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write("Aqui estão os dados do arquivo CSV que você fez o upload:")
    st.write(dataframe)
