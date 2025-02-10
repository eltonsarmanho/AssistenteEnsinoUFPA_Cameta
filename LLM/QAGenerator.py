import os
from langchain_community.chat_models import ChatMaritalk, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Suprime logs indesejados
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


class DictOutputParser(BaseOutputParser):
    """Parser personalizado para converter a saída em um dicionário."""
    def parse(self, text: str):
        qa_pairs = []
        blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
        for block in blocks:
            lines = block.split("\n")
            # Validação: Verifica se há pelo menos duas linhas no bloco
            if len(lines) < 2:
                print(f"Bloco inválido ignorado: {block}")
                continue

            # Extrai pergunta e resposta
            try:
                # Procura por "Pergunta X:" e "Resposta X:"
                pergunta_line = next((line for line in lines if line.startswith("Pergunta")), None)
                resposta_line = next((line for line in lines if line.startswith("Resposta")), None)

                if not pergunta_line or not resposta_line:
                    print(f"Formato inválido no bloco: {block}")
                    continue

                pergunta = pergunta_line.split(": ", 1)[1].strip()
                resposta = resposta_line.split(": ", 1)[1].strip()

                qa_pairs.append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })
            except IndexError:
                print(f"Erro ao processar bloco: {block}")
                continue

        return qa_pairs


class QAGenerator:
    def __init__(self, n_perguntas=3, model_name="maritalk"):
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
                model="gemini-1.5-flash", transport='rest',
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                top_p=0.30,
                max_output_tokens=600  # Aumentado para comportar mais perguntas
            )
        elif self.model_name == "openai":
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",  # Ou outro modelo OpenAI desejado
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.7, max_tokens=600
            )
        else:
            raise ValueError(
                f"Modelo '{self.model_name}' não suportado. Escolha entre 'maritalk', 'google' ou 'openai'."
            )

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             f"""Você é um gerador de perguntas e respostas. Siga estas regras RIGOROSAMENTE:
             1. SEMPRE comece respondendo à pergunta original no formato EXATO:
                Pergunta 1: [resposta à pergunta original]
                Resposta 1: [resposta detalhada]
             2. Em seguida, gere {self.n_perguntas - 1} perguntas relacionadas e suas respostas, seguindo o mesmo formato:
                Pergunta 2: [pergunta relacionada]
                Resposta 2: [resposta correspondente]
                ...
                Pergunta {self.n_perguntas}: [última pergunta relacionada]
                Resposta {self.n_perguntas}: [última resposta correspondente]
             3. NÃO USE MARCADORES (*), LISTAS OU OUTROS FORMATOS. Apenas siga o formato acima.
             """),
            ("human", "{pergunta}")
        ])

        # Usa o parser personalizado
        self.chain = self.prompt_template | self.llm | DictOutputParser()

    def generate_qa(self, pergunta_original):
        # Invoca a cadeia e retorna diretamente o dicionário
        return self.chain.invoke({"pergunta": pergunta_original})

    def gerar_resposta_revisada(self, pergunta, contexto_adicional=None):
        """
        Gera uma resposta revisada para uma pergunta com base no feedback do usuário.
        """
        prompt_template = ChatPromptTemplate.from_messages([
            ("system",
             f"""Você é um assistente de correção de erros. Sua tarefa é gerar uma resposta revisada para a seguinte pergunta:
             Pergunta: {pergunta}
             Contexto adicional (se houver): {contexto_adicional or 'Nenhum'}
             Certifique-se de fornecer uma resposta clara e precisa."""),
            ("human", "{pergunta}")
        ])
        chain = prompt_template | self.llm | StrOutputParser()
        resposta_revisada = chain.invoke({"pergunta": pergunta})
        return resposta_revisada
# Exemplo de uso
if __name__ == "__main__":
    # Cria o gerador e especifica o arquivo
    gerador = QAGenerator(n_perguntas=3, model_name='google')
    # Gera e salva automaticamente
    resultado = gerador.generate_qa("Quais alimentos possuem zinco?")
    for i, par in enumerate(resultado, 1):
        print(f"Pergunta {i}: {par['pergunta']}")
        print(f"Resposta {i}: {par['resposta']}\n")