import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv
import time
import pandas as pd
import os
import json


class ConexaoFirebase:
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
    def inserir_dados_questao(self, pergunta, resposta):
        try:
            questao_ref = db.reference('Questao')
            novo_id = questao_ref.push({
                'Pergunta': pergunta,
                'Resposta': resposta
            }).key
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

    def listar_dados_questoes(self):
        try:
            questionario_ref = db.reference('Questao')
            dados = questionario_ref.get()
            if dados:
                print("\nDados da tabela 'Questao':")
                for key, value in dados.items():
                    print(f"ID: {key}, Pergunta: {value['pergunta']}, Resposta: {value['resposta']}")
            else:
                print("Nenhum dado encontrado na tabela 'Questao'.")
        except Exception as error:
            print(f"Erro ao listar dados do 'Questao': {error}")

    def get_dados_questoes(self):
        """
        Lista os dados da tabela 'Questao' e retorna um DataFrame.
        """
        try:
            questao_ref = db.reference('Questao')
            dados = questao_ref.get()

            if not dados:
                print("Nenhum dado encontrado na tabela 'Questao'.")
                return pd.DataFrame()  # Retorna um DataFrame vazio se não houver dados

            # Converte os dados em uma lista de dicionários
            lista_dados = []
            for key, value in dados.items():
                #value['id'] = key  # Adiciona o ID ao dicionário
                lista_dados.append(value)

            # Cria um DataFrame a partir da lista de dicionários
            df = pd.DataFrame(lista_dados)

            return df  # Retorna o DataFrame

        except Exception as error:
            print(f"Erro ao listar dados do 'Questao': {error}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

    def inserir_dados_resposta_incorreta(self, pergunta, resposta_incorreta):
        """
        Insere uma resposta incorreta na tabela 'RespostasIncorretas'.
        """
        try:
            respostas_incorretas_ref = db.reference('RespostasIncorretas')
            novo_id = respostas_incorretas_ref.push({
                'Pergunta': pergunta,
                'RespostaIncorreta': resposta_incorreta
            }).key
            print(f"Resposta incorreta registrada com ID: {novo_id}")
        except Exception as error:
            print(f"Erro ao registrar resposta incorreta: {error}")

    def substituir_resposta_corrigida(self, pergunta, nova_resposta):
        """
        Substitui uma resposta incorreta pela versão corrigida na tabela 'Questao'.
        """
        try:
            questao_ref = db.reference('Questao')
            dados = questao_ref.get()
            if dados:
                for key, value in dados.items():
                    if value['Pergunta'] == pergunta:
                        questao_ref.child(key).update({'Resposta': nova_resposta})
                        print(f"Resposta corrigida para a pergunta '{pergunta}' atualizada com sucesso!")
                        return
            print("Pergunta não encontrada na tabela 'Questao'.")
        except Exception as error:
            print(f"Erro ao substituir resposta corrigida: {error}")

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
    project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do json atual
    cred_path = os.path.join(project_root,'..', 'Keys', 'coletadados-firebase.json')

    with open(cred_path, 'r') as file:
        config = json.load(file)
    # Acesse os valores no dicionário
    database_url = config['database_url']
    # Instancia a classe e conecta ao Firebase
    firebase_db = ConexaoFirebase(cred_path, database_url)

    try:
        firebase_db.conectar()
        # Cria as estruturas iniciais no Firebase
        firebase_db.criar_estruturas()
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
        firebase_db.listar_dados_questoes()
        print(firebase_db.get_dados_questoes())
        # Salva os dados da tabela Questionario em CSV
        #firebase_db.salvar_tabela_em_csv("Questionario", "dados_questionario.csv")

    except Exception as error:
        print(f"Erro: {error}")