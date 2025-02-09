import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv
import time
import sys
import os
import json
class QuestionarioFirebase:
    def __init__(self, cred_path, database_url):
        self.cred_path = cred_path
        self.database_url = database_url

    def conectar(self):
        """Inicializa a conexão com o Firebase."""
        if not firebase_admin._apps:
            # O app ainda não foi inicializado
            cred = credentials.Certificate(self.cred_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': self.database_url
            })
            print("Conexão com o Firebase estabelecida com sucesso!")
        else:
            print("Firebase já está conectado.")

    # Método para criar estruturas iniciais (nós) no Firebase
    def criar_estruturas(self):
        try:
            # Referências para as "tabelas" no Firebase
            questionario_ref = db.reference('Questionario')
            questao_ref = db.reference('Questao')
            requisicoes_ref = db.reference('Requisicoes')

            # Verifica se já existem dados nas referências
            if not questionario_ref.get():
                questionario_ref.set({})
                print("Estrutura 'Questionario' criada com sucesso!")
            if not questao_ref.get():
                questao_ref.set({})
                print("Estrutura 'Questao' criada com sucesso!")
            if not requisicoes_ref.get():
                requisicoes_ref.set({})
                print("Estrutura 'Requisicoes' criada com sucesso!")
        except Exception as error:
            print(f"Erro ao criar estruturas: {error}")

    # Método para inserir dados na tabela Questionario
    def inserir_dados_questionario(self, qualidade, tempo):
        try:
            questionario_ref = db.reference('Questionario')
            novo_id = questionario_ref.push({
                'qualidade': qualidade,
                'tempo': tempo
            }).key
            print(f"Dados inseridos no 'Questionario' com ID: {novo_id}")
        except Exception as error:
            print(f"Erro ao inserir dados no 'Questionario': {error}")

    # Método para inserir dados na tabela Questao
    def inserir_dados_questao(self, pergunta, resposta, classe):
        try:
            questao_ref = db.reference('Questao')
            novo_id = questao_ref.push({
                'Pergunta': pergunta,
                'Resposta': resposta,
                'Classe': classe
            }).key
            print(f"Dados inseridos no 'Questao' com ID: {novo_id}")
        except Exception as error:
            print(f"Erro ao inserir dados no 'Questao': {error}")

    # Método para inserir dados na tabela Requisicoes
    def inserir_dados_requisicoes(self, pergunta, tempo_requisicao):
        try:
            requisicoes_ref = db.reference('Requisicoes')
            novo_id = requisicoes_ref.push({
                'pergunta': pergunta,
                'tempo_requisicao': tempo_requisicao
            }).key
            print(f"Dados inseridos no 'Requisicoes' com ID: {novo_id}")
        except Exception as error:
            print(f"Erro ao inserir dados no 'Requisicoes': {error}")

    # Método para listar os dados da tabela Questionario
    def listar_dados_questionario(self):
        try:
            questionario_ref = db.reference('Questionario')
            dados = questionario_ref.get()
            if dados:
                print("\nDados da tabela 'Questionario':")
                for key, value in dados.items():
                    print(f"ID: {key}, Qualidade: {value['qualidade']}, Tempo: {value['tempo']}")
            else:
                print("Nenhum dado encontrado na tabela 'Questionario'.")
        except Exception as error:
            print(f"Erro ao listar dados do 'Questionario': {error}")

    # Método genérico para salvar os dados de uma tabela em CSV
    def salvar_tabela_em_csv(self, nome_tabela, nome_arquivo_csv):
        try:
            tabela_ref = db.reference(nome_tabela)
            dados = tabela_ref.get()
            if not dados:
                print(f"Nenhum dado encontrado na tabela '{nome_tabela}'.")
                return

            # Extrai colunas dos dados
            colunas = list(next(iter(dados.values())).keys())

            # Salva em arquivo CSV
            with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv)
                escritor_csv.writerow(colunas)  # Escreve os cabeçalhos
                for key, value in dados.items():
                    escritor_csv.writerow([value[col] for col in colunas])  # Escreve os dados
            print(f"Dados da tabela '{nome_tabela}' salvos com sucesso no arquivo {nome_arquivo_csv}!")
        except Exception as error:
            print(f"Erro ao salvar dados da tabela '{nome_tabela}' no CSV: {error}")

    def fechar_conexao(self):
        try:
            # Encerra o app Firebase (fecha a conexão)
            firebase_admin.delete_app(firebase_admin.get_app())
            print("Conexão com o Firebase encerrada.")
        except Exception as error:
            print(f"Erro ao encerrar a conexão: {error}")

# Uso da classe QuestionarioFirebase
if __name__ == '__main__':
    # Parâmetros de conexão ao Firebase
    file = "coletadados-f1884-firebase-adminsdk-itqt9-73bd934db1.json"
    project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
    cred_path = os.path.join(project_root, '..', 'Keys', file)
    database_url = "https://coletadados-f1884-default-rtdb.firebaseio.com/"

    # Instancia a classe e conecta ao Firebase
    #firebase_db = QuestionarioFirebase(cred_path, database_url)

    try:
        # Cria as estruturas iniciais no Firebase
        # firebase_db.criar_estruturas()
        #
        # # Insere dados na tabela Questionario
        # firebase_db.inserir_dados_questionario(3, 4)
        #
        # # Insere dados na tabela Questao
        # firebase_db.inserir_dados_questao(
        #     "Como a Lei Geral na EUA?", "Resposta exemplo", 0
        # )
        #
        # # Simula uma requisição
        # pergunta = "Qual é a capital da Arg?"
        # inicio = time.time()
        # time.sleep(2)  # Simulação de processamento
        # fim = time.time()
        # tempo_requisicao = fim - inicio
        # firebase_db.inserir_dados_requisicoes(pergunta, tempo_requisicao)

        # Lista os dados da tabela Questionario
        firebase_db.listar_dados_questionario()

        # Salva os dados da tabela Questionario em CSV
        #firebase_db.salvar_tabela_em_csv("Questionario", "dados_questionario.csv")

    except Exception as error:
        print(f"Erro: {error}")