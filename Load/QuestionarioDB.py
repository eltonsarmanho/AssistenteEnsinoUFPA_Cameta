import psycopg2
import time
import csv


class QuestionarioDB:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    # Método para conectar ao banco de dados
    def conectar(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Conexão estabelecida com sucesso!")
        except Exception as error:
            print(f"Erro ao conectar ao banco de dados: {error}")

    # Método para fechar a conexão
    def fechar_conexao(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Conexão encerrada.")

    # Método para criar a tabela Questionario
    def criar_tabela_Questionario(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Questionario (
            id SERIAL PRIMARY KEY,
            qualidade INT NOT NULL,
            tempo INT NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Tabela Questionario criada com sucesso!")


    def criar_tabela_questoes(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Questao (
            id SERIAL PRIMARY KEY,
            Pergunta TEXT NULL,
            Resposta TEXT NULL,
            Classe INT
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Tabela Questoes criada com sucesso!")

        # Método para criar a tabela Requisicoes

    def criar_tabela_requisicoes(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Requisicoes (
                id SERIAL PRIMARY KEY,
                pergunta TEXT NOT NULL,
                tempo_requisicao FLOAT NOT NULL
            );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Tabela Requisicoes criada com sucesso!")

    # Método para inserir dados na tabela Questionario
    def inserir_dados(self, qualidade, tempo):
        insert_query = """
        INSERT INTO Questionario (qualidade, tempo)
        VALUES (%s, %s);
        """
        self.cursor.execute(insert_query, (qualidade, tempo))
        self.connection.commit()
        print("Dados inseridos com sucesso!")

    def inserir_dados_questao(self, pergunta, resposta,classe):
        insert_query = """
        INSERT INTO Questao (pergunta, resposta,classe)
        VALUES (%s, %s,%s);
        """
        self.cursor.execute(insert_query, (pergunta, resposta,classe))
        self.connection.commit()
        print("Dados inseridos com sucesso!")

        # Método para inserir dados na tabela Requisicoes

    def inserir_dados_requisicoes(self, pergunta, tempo_requisicao):
            insert_query = """
            INSERT INTO Requisicoes (pergunta, tempo_requisicao)
            VALUES (%s, %s);
            """
            self.cursor.execute(insert_query, (pergunta, tempo_requisicao))
            self.connection.commit()
            print("Dados inseridos na tabela Requisicoes com sucesso!")

    # Método para listar os dados da tabela Questionario
    def listar_dados(self):
        select_query = "SELECT * FROM Questionario;"
        self.cursor.execute(select_query)
        registros = self.cursor.fetchall()

        print("\nDados da tabela 'Questionario':")
        for row in registros:
            print(f"ID: {row[0]}, Qualidade: {row[1]}, Tempo: {row[2]}")

        # Método genérico para salvar os dados de uma tabela em CSV
    def salvar_tabela_em_csv(self, nome_tabela, nome_arquivo_csv):
            try:
                # Consulta para obter todos os dados da tabela
                select_query = f"SELECT * FROM {nome_tabela};"
                self.cursor.execute(select_query)
                registros = self.cursor.fetchall()

                # Verifica as colunas da tabela para usar como cabeçalhos no CSV
                colunas = [desc[0] for desc in self.cursor.description]

                # Salvar em arquivo CSV
                with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv:
                    escritor_csv = csv.writer(arquivo_csv)
                    escritor_csv.writerow(colunas)  # Escreve os cabeçalhos
                    escritor_csv.writerows(registros)  # Escreve os dados

                print(f"Dados da tabela '{nome_tabela}' salvos com sucesso no arquivo {nome_arquivo_csv}!")

            except Exception as error:
                print(f"Erro ao salvar dados da tabela '{nome_tabela}' no CSV: {error}")



# Uso da classe QuestionarioDB
if __name__ == '__main__':
     # Parâmetros de conexão ao banco de dados
     host = "aws-0-sa-east-1.pooler.supabase.com"
     port = "6543"
     dbname = "postgres"
     user = "postgres.wrlwzbewagseuoisnmqz"
     password = "RR%EPQ^dCen6%fTo"

     # Instancia a classe e conecta ao banco
     db = QuestionarioDB(host, port, dbname, user, password)
     db.conectar()

     try:
         # Cria a tabela Questionario
         #db.criar_tabela_requisicoes()

#         # Insere dados na tabela Questionario
         #db.inserir_dados(4, 3)
         #db.inserir_dados_questao('Como a Lei Geral ','ivacidadebrasileiras?Como a Lei Geral de as brasileiras? ',0)


         # Registrar uma nova requisição com a pergunta e o tempo gasto
         #pergunta = "Qual é a capital da França?"
         #inicio = time.time()
         # Simulação de processamento da pergunta
         #time.sleep(2)  # Simulação de 2 segundos para processamento
         #fim = time.time()
         #tempo_requisicao = fim - inicio
         #db.inserir_dados_requisicoes(pergunta, tempo_requisicao)
         #Lista os dados da tabela Questionario
         #db.listar_dados('')
        db.salvar_tabela_em_csv('Questionario','dataset/dados_questionario.csv')
        db.salvar_tabela_em_csv("Requisicoes", "dataset/dados_requisicoes.csv")

     except Exception as error:
         print(f"Erro: {error}")

     finally:
         # Fecha a conexão com o banco de dados
         db.fechar_conexao()
