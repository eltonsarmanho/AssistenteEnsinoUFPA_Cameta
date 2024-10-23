import pandas as pd
import maritalk
import re

minha_chave = "100088405894968274443$48d83f597eed3dac55ca7ab70e8d6d46628784d793046bf36006985b4d18354e"


# Função que faz uma pergunta para a LLM
def pergunta_llm(pergunta):
    model = maritalk.MariTalk(
        key=minha_chave,
        model="sabia-2-small"
    )

    messages = [
        {"role": "user", "content": f"{pergunta}"},
    ]

    resposta = model.generate(
        messages,
        do_sample=True,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95)["answer"]

    # Processar a resposta para remover formatações indesejadas e respostas vazias
    resposta = formatar_resposta(resposta)

    return resposta


# Função para formatar a resposta
def formatar_resposta(resposta):
    # Remover partes vazias como "2. **"
    resposta = re.sub(r"\d+\.\s\*\*", "", resposta)

    # Remover espaços extras
    resposta = resposta.strip()

    # Se a resposta estiver completamente vazia, retornar None
    if not resposta:
        return None

    return resposta


# Função para gerar N perguntas com base em uma pergunta original
def gerar_perguntas_llm(pergunta, n):
    model = maritalk.MariTalk(
        key=minha_chave,
        model="sabia-2-small"
    )

    perguntas_geradas = []

    for i in range(n):
        # Pedir ao modelo para gerar perguntas relacionadas
        messages = [
            {"role": "user", "content": f"Baseado nesta pergunta: '{pergunta}', gere uma nova pergunta relacionada."},
        ]

        nova_pergunta = model.generate(
            messages,
            do_sample=True,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95)["answer"]

        perguntas_geradas.append(nova_pergunta)

    return perguntas_geradas


# Função para atualizar o dataframe localmente (sem sobrescrever ainda)
def update_dataset(df: pd.DataFrame, pergunta, resposta):
    if resposta:  # Só adiciona ao dataset se a resposta não for vazia
        novo_registro = {'Pergunta': pergunta, 'Resposta': resposta}
        df = df._append(novo_registro, ignore_index=True)
    return df


# Função principal para gerar N perguntas, salvar todas as perguntas e respostas no dataset de uma vez
def gerar_perguntas_e_atualizar_dataset(df: pd.DataFrame, pergunta, n):
    perguntas_geradas = gerar_perguntas_llm(pergunta, n)
    perguntas_geradas.append(pergunta)
    for nova_pergunta in perguntas_geradas:
        resposta = pergunta_llm(nova_pergunta)  # Obter a resposta para a nova pergunta
        if resposta:
            # Printar a pergunta e resposta
            #print(f"Pergunta: {nova_pergunta}")
            #print(f"Resposta: {resposta}\n")
            # Atualizar o dataframe localmente
            df = update_dataset(df, nova_pergunta, resposta)

    # Após todas as atualizações, salvar o dataframe no arquivo CSV
    df.to_csv('../dataset/dataset.csv', index=False)
    return nova_pergunta,resposta



