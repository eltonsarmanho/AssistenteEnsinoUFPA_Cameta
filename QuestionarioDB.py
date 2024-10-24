import psycopg2
import time


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
         db.criar_tabela_requisicoes()
#
#         # Insere dados na tabela Questionario
         #db.inserir_dados(4, 3)
         #db.inserir_dados_questao('Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?',
         #                          'Como a Lei Geral deComo a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras?Como a Lei Geral de Proteção de Dados (LGPD) afeta as práticas de privacidade de dados nas empresas brasileiras? ',0)
#
#
         # Registrar uma nova requisição com a pergunta e o tempo gasto
         pergunta = "Qual é a capital da França?"
         inicio = time.time()
         # Simulação de processamento da pergunta
         time.sleep(2)  # Simulação de 2 segundos para processamento
         fim = time.time()
         tempo_requisicao = fim - inicio
         db.inserir_dados_requisicoes(pergunta, tempo_requisicao)
     # Lista os dados da tabela Questionario
         #db.listar_dados()
#
     except Exception as error:
         print(f"Erro: {error}")

     finally:
         # Fecha a conexão com o banco de dados
         db.fechar_conexao()
