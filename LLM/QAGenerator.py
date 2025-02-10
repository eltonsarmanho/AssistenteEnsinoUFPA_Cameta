

import csv
import os
from datetime import datetime
from langchain_community.chat_models import ChatMaritalk
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
import pytz  # Adicione esta linha
import google.generativeai as genai

load_dotenv()
import os

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

class QAGenerator:
    def __init__(self, n_perguntas=3,model_name="maritalk"):
        self.n_perguntas = n_perguntas + 1  # +1 para incluir a original
        self.model_name = model_name.lower()  # Nome do modelo escolhido
        self._inicializar_modelo()

    def _inicializar_modelo(self):
        if self.model_name == "maritalk":
            self.llm = ChatMaritalk(
                model="sabia-3",
                api_key=os.getenv("MARITALK_API_KEY"),
                temperature=0.7,
                max_tokens=600  # Aumentado para comportar mais perguntas
            )
        elif self.model_name == "google":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",transport='rest',
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                top_p=0.30 ,
                max_output_tokens=600# Aumentado para comportar mais perguntas
            )
        elif self.model_name == "openai":
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",  # Ou outro modelo OpenAI desejado
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.7, max_tokens=600
            )
        else:
            raise ValueError(
                f"Modelo '{self.model_name}' não suportado. Escolha entre 'maritalk', 'google' ou 'openai'.")
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             f"""Você é um gerador de perguntas e respostas. Siga estas regras:
             1. Sempre comece respondendo a pergunta original
             2. Em seguida, gere {self.n_perguntas - 1} perguntas relacionadas
             3. Formato obrigatório:
                Pergunta 1: [resposta à pergunta original]
                Resposta 1: [resposta detalhada]
                {self._format_example(start=2)}"""),
            ("human", "{pergunta}")
        ])

        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def _format_example(self, start=2):
        example = []
        for i in range(start, self.n_perguntas + 1):
            example.append(f"Pergunta {i}: [pergunta relacionada]")
            example.append(f"Resposta {i}: [resposta correspondente]")
        return "\n".join(example)



    def generate_qa(self, pergunta_original):
        response = self.chain.invoke({"pergunta": pergunta_original})
        qa_pairs = self._parse_response(response)
        return qa_pairs

    def _parse_response(self, response):
        qa_pairs = []
        blocks = [b.strip() for b in response.split("\n\n") if b.strip()]

        for block in blocks[:self.n_perguntas]:  # Pega todas as perguntas
            lines = block.split("\n")
            if len(lines) >= 2:
                pergunta = lines[0].split(": ", 1)[1].strip()
                resposta = lines[1].split(": ", 1)[1].strip()
                qa_pairs.append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })
        return qa_pairs

# Exemplo de uso
if __name__ == "__main__":
    # Cria o gerador e especifica o arquivo
    gerador = QAGenerator(n_perguntas=3,model_name='google')

    # Gera e salva automaticamente
    #resultado = gerador.generate_qa("o que é machine learning?")

    # Nova requisição adiciona ao mesmo arquivo
    resultado = gerador.generate_qa("o que é linux?")
    for i, par in enumerate(resultado, 1):
        print(par['pergunta'], par['resposta'])