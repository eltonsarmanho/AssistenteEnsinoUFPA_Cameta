import psycopg2


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
    def criar_tabela(self):
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

    # Método para inserir dados na tabela Questionario
    def inserir_dados(self, qualidade, tempo):
        insert_query = """
        INSERT INTO Questionario (qualidade, tempo)
        VALUES (%s, %s);
        """
        self.cursor.execute(insert_query, (qualidade, tempo))
        self.connection.commit()
        print("Dados inseridos com sucesso!")

    # Método para listar os dados da tabela Questionario
    def listar_dados(self):
        select_query = "SELECT * FROM Questionario;"
        self.cursor.execute(select_query)
        registros = self.cursor.fetchall()

        print("\nDados da tabela 'Questionario':")
        for row in registros:
            print(f"ID: {row[0]}, Qualidade: {row[1]}, Tempo: {row[2]}")


# Uso da classe QuestionarioDB
# if __name__ == '__main__':
#     # Parâmetros de conexão ao banco de dados
#     host = "aws-0-sa-east-1.pooler.supabase.com"
#     port = "6543"
#     dbname = "postgres"
#     user = "postgres.wrlwzbewagseuoisnmqz"
#     password = "RR%EPQ^dCen6%fTo"
#
#     # Instancia a classe e conecta ao banco
#     db = QuestionarioDB(host, port, dbname, user, password)
#     db.conectar()
#
#     try:
#         # Cria a tabela Questionario
#         db.criar_tabela()
#
#         # Insere dados na tabela Questionario
#         db.inserir_dados(4, 3)
#
#         # Lista os dados da tabela Questionario
#         db.listar_dados()
#
#     except Exception as error:
#         print(f"Erro: {error}")
#
#     finally:
#         # Fecha a conexão com o banco de dados
#         db.fechar_conexao()
