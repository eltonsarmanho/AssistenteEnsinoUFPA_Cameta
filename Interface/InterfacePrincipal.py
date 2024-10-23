import tkinter as tk
from tkinter import scrolledtext
import pandas as pd

# Funções de manipulação do sistema (substituir com chamadas ao sistema real)
from maritalk import MariTalk


# Função que faz a pergunta para a LLM
def pergunta_llm(pergunta):
    minha_chave = "100088405894968274443$48d83f597eed3dac55ca7ab70e8d6d46628784d793046bf36006985b4d18354e"

    model = MariTalk(key=minha_chave, model="sabia-2-small")
    messages = [{"role": "user", "content": f"{pergunta}"}]
    resposta = model.generate(messages, do_sample=True, max_tokens=200, temperature=0.7, top_p=0.95)["answer"]
    return resposta


# Função que atualiza a resposta no campo de texto
def fazer_pergunta():
    pergunta = entrada_pergunta.get()
    resposta = pergunta_llm(pergunta)

    # Atualiza a interface com a resposta
    area_resposta.config(state='normal')
    area_resposta.insert(tk.END, f"Pergunta: {pergunta}\nResposta: {resposta}\n\n")
    area_resposta.config(state='disabled')


# Função principal para criar a interface
def criar_interface():
    janela = tk.Tk()
    janela.title("Sistema de Perguntas")

    # Label para instrução
    label = tk.Label(janela, text="Digite sua pergunta:")
    label.pack(pady=5)

    # Entrada de texto para a pergunta
    global entrada_pergunta
    entrada_pergunta = tk.Entry(janela, width=50)
    entrada_pergunta.pack(pady=5)

    # Botão para enviar a pergunta
    botao_enviar = tk.Button(janela, text="Enviar", command=fazer_pergunta)
    botao_enviar.pack(pady=5)

    # Área de texto para exibir a resposta
    global area_resposta
    area_resposta = scrolledtext.ScrolledText(janela, width=60, height=20, wrap=tk.WORD)
    area_resposta.pack(pady=5)
    area_resposta.config(state='disabled')  # Desativar para evitar edição direta

    janela.mainloop()


# Executar a interface
if __name__ == "__main__":
    criar_interface()
