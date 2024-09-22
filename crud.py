import psycopg2
import os


class AppBD:
    def __init__(self):
        print('Método Construtor')

    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                               password="1234",
                                               host="localhost",
                                               port="5432",
                                               database="postgres")
        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print("Falha ao se conectar ao Banco de Dados", error)
# -----------------------------------------------------------------------------
# Selecionar Um Unico Produto
# -----------------------------------------------------------------------------

    def selecionarDadosUnicos(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            print("Selecionando produto unico")
            sql_select_query = """select * from public."PRODUTO" where "CODIGO" =%s"""

            cursor.execute(sql_select_query, (codigo,))
            registros = cursor.fetchone()
            print(registros)

        except (Exception, psycopg2.Error) as error:
            print("Error in select operation", error)

        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
        return registros
# -----------------------------------------------------------------------------
# Selecionar todos os Produtos
# -----------------------------------------------------------------------------

    def selecionarDados(self):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            print("Selecionando todos os produtos")
            sql_select_query = """select * from public."PRODUTO" ORDER BY "NOME" ASC"""

            cursor.execute(sql_select_query)
            registros = cursor.fetchall()
            print(registros)

        except (Exception, psycopg2.Error) as error:
            print("Error in select operation", error)

        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
        return registros
# -----------------------------------------------------------------------------
# Pesquisar por Produtos
# -----------------------------------------------------------------------------

    def pesquisarDados(self, nome):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            print("Pesquisando por Produtos")
            sql_select = """select * from public. "PRODUTO" where "NOME" ILIKE %s ORDER BY "NOME" ASC"""

            
            cursor.execute(sql_select, (nome, ))
            registro = cursor.fetchall()
            print(registro)
        except (Exception, psycopg2.Error) as error:
            print("Error in select operation", error)
        finally:
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")
        return registro

# -----------------------------------------------------------------------------
# Inserir Produto
# -----------------------------------------------------------------------------

    def inserirDados(self, codigo, nome, qtd):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO public."PRODUTO" 
          ("CODIGO", "NOME", "QTD") VALUES (%s,%s,%s)"""
            record_to_insert = (codigo, nome, qtd)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro inserido com successo na tabela PRODUTO")
            nome_arquivo = "produto/" + nome + ".txt"
            arquivo = open(nome_arquivo, "w", encoding="utf-8")
            with arquivo as escrita:
                escrita.write(f"Codigo do produto: {codigo}\nNome do produto: {nome}\nQuantidade inicial: {qtd}")

        except (Exception, psycopg2.Error) as error:
            if (self.connection):
                print("Falha ao inserir registro na tabela PRODUTO", error)

        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

# -----------------------------------------------------------------------------
# Atualizar Produto
# -----------------------------------------------------------------------------
    def atualizarDados(self, codigo, qtd):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()

            print("Registro Antes da Atualização ")
            sql_select_query = """select * from public."PRODUTO" 
            where "CODIGO" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)
            # Atualizar registro

            sql_update_query = """Update public."PRODUTO" set  
            "QTD" = %s where "CODIGO" = %s"""
            cursor.execute(sql_update_query, (qtd, codigo))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro atualizado com sucesso! ")

            print("Registro Depois da Atualização ")
            sql_select_query = """select * from public."PRODUTO" 
            where "CODIGO" = %s"""
            cursor.execute(sql_select_query, (codigo,))
            record = cursor.fetchone()
            print(record)
        except (Exception, psycopg2.Error) as error:
            print("Erro na Atualização", error)
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

# -----------------------------------------------------------------------------
# Excluir Produto
# -----------------------------------------------------------------------------
    def excluirDados(self, codigo):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            # Atualizar registro
            sql_delete_query = """Delete from public."PRODUTO" 
            where "CODIGO" = %s"""
            cursor.execute(sql_delete_query, (codigo, ))

            self.connection.commit()
            count = cursor.rowcount
            print(count, "Registro excluído com sucesso! ")
        except (Exception, psycopg2.Error) as error:
            print("Erro na Exclusão", error)
        finally:
            # closing database connection.
            if (self.connection):
                cursor.close()
                self.connection.close()
                print("A conexão com o PostgreSQL foi fechada.")

# -----------------------------------------------------------------------------
