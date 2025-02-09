

import csv
import os
from datetime import datetime
from langchain_community.chat_models import ChatMaritalk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
import pytz  # Adicione esta linha

load_dotenv()


class QAGenerator:
    def __init__(self, n_perguntas=3, arquivo_csv='dataset.csv'):
        self.n_perguntas = n_perguntas
        self.arquivo_csv = arquivo_csv
        self._inicializar_modelo()
        self._criar_arquivo_se_nao_existir()

    def _inicializar_modelo(self):
        self.llm = ChatMaritalk(
            model="sabia-3",
            api_key=os.getenv("MARITALK_API_KEY"),
            temperature=0.7,
            max_tokens=400
        )

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             f"""Você é um gerador de perguntas e respostas relacionadas.
             Para cada pergunta recebida, gere {self.n_perguntas} perguntas similares 
             com respostas correspondentes.

             Formato obrigatório:
             {self._format_example()}"""),
            ("human", "Pergunta original: {pergunta}")
        ])

        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def _format_example(self):
        example = []
        for i in range(1, self.n_perguntas + 1):
            example.append(f"Pergunta {i}: [texto]")
            example.append(f"Resposta {i}: [texto]")
        return "\n".join(example)

    def _criar_arquivo_se_nao_existir(self):
        if not os.path.exists(self.arquivo_csv):
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self._cabecalhos())
                writer.writeheader()

    def _cabecalhos(self):
        return ['original_pergunta', 'pergunta', 'resposta', 'data_criacao']

    def generate_qa(self, pergunta):
        response = self.chain.invoke({"pergunta": pergunta})
        qa_pairs = self._parse_response(response)
        self._salvar_no_csv(pergunta, qa_pairs)
        return qa_pairs

    def _parse_response(self, response):
        qa_pairs = []
        blocks = [b.strip() for b in response.split("\n\n") if b.strip()]

        for block in blocks[:self.n_perguntas]:
            lines = block.split("\n")
            if len(lines) >= 2:
                pergunta = lines[0].split(": ", 1)[1].strip()
                resposta = lines[1].split(": ", 1)[1].strip()
                qa_pairs.append({"pergunta": pergunta, "resposta": resposta})

        return qa_pairs

    def _salvar_no_csv(self, pergunta_original, qa_pairs):
        with open(self.arquivo_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self._cabecalhos())

            for par in qa_pairs:
                writer.writerow({
                    'original_pergunta': pergunta_original,
                    'pergunta': par['pergunta'],
                    'resposta': par['resposta'],
                    'data_criacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })


# Exemplo de uso
if __name__ == "__main__":
    # Cria o gerador e especifica o arquivo
    project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
    file_path_dataset = os.path.join(project_root, '..', 'dataset', 'dataset.csv')
    gerador = QAGenerator(n_perguntas=3, arquivo_csv=file_path_dataset)

    # Gera e salva automaticamente
    resultado = gerador.generate_qa("o que é machine learning?")

    # Nova requisição adiciona ao mesmo arquivo
    gerador.generate_qa("o que é deep learning?")