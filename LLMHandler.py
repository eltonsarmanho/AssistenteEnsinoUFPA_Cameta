import pandas as pd
import maritalk
import re

class LLMHandler:
    def __init__(self, chave):
        self.model = maritalk.MariTalk(
            key=chave,
            model="sabia-2-small"
        )

    # Função que faz uma pergunta para a LLM
    def pergunta_llm(self, pergunta):
        messages = [
            {"role": "user", "content": f"{pergunta}"},
        ]

        resposta = self.model.generate(
            messages,
            do_sample=True,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95)["answer"]

        # Processar a resposta para remover formatações indesejadas e respostas vazias
        resposta = self.formatar_resposta(resposta)

        return resposta

    # Função para formatar a resposta
    def formatar_resposta(self, resposta):
        # Remover partes vazias como "2. **"
        resposta = re.sub(r"\d+\.\s\*\*", "", resposta)

        # Remover espaços extras
        resposta = resposta.strip()

        # Se a resposta estiver completamente vazia, retornar None
        if not resposta:
            return None

        return resposta

    # Função para gerar N perguntas com base em uma pergunta original
    def gerar_perguntas_llm(self, pergunta, n):
        perguntas_geradas = []

        for i in range(n):
            # Pedir ao modelo para gerar perguntas relacionadas
            messages = [
                {"role": "user", "content": f"Baseado nesta pergunta: '{pergunta}', gere uma nova pergunta relacionada."},
            ]

            nova_pergunta = self.model.generate(
                messages,
                do_sample=True,
                max_tokens=800,
                temperature=0.7,
                top_p=0.95)["answer"]

            perguntas_geradas.append(nova_pergunta)

        return perguntas_geradas

    # Função para atualizar o dataframe localmente (sem sobrescrever ainda)
    def update_dataset(self, df: pd.DataFrame, pergunta, resposta,classe):
        if resposta:  # Só adiciona ao dataset se a resposta não for vazia
            novo_registro = {'Pergunta': pergunta, 'Resposta': resposta, 'Classe': classe}
            df = df._append(novo_registro, ignore_index=True)
        return df

    # Função principal para gerar N perguntas, salvar todas as perguntas e respostas no dataset de uma vez
    def gerar_perguntas_e_atualizar_dataset(self, df: pd.DataFrame, pergunta, n):
        perguntas_geradas = self.gerar_perguntas_llm(pergunta, n)
        perguntas_geradas.append(pergunta)
        for nova_pergunta in perguntas_geradas:
            resposta = self.pergunta_llm(nova_pergunta)  # Obter a resposta para a nova pergunta
            if resposta:
                if(pergunta == nova_pergunta):
                    df = self.update_dataset(df, nova_pergunta, resposta, 1)
                else: df = self.update_dataset(df, nova_pergunta, resposta,0)

        # Após todas as atualizações, salvar o dataframe no arquivo CSV
        df.to_csv('dataset/dataset.csv', index=False)
        return nova_pergunta,resposta,df


