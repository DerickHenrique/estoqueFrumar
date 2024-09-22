import psycopg2
import datetime

class BaseBD:
    hoje = datetime.date.today()
    def __init__(self):
        print('Metodo Construtor')
# Definindo a função que abrirá a cenexão

    def abrirConn(self):
        try:
            self.conn = psycopg2.connect(user="postgres",
                                         password="1234",
                                         host="localhost",
                                         port="5432",
                                         database="postgres")
        except (Exception, psycopg2.Error) as error:
            if (self.conn):
                print('Falha ao conectar', error)

# Definindo a função que selecionara todos os Produtos

    def selDados(self):
        try:
            self.abrirConn()
            cur = self.conn.cursor()
            # Criando uma variavel para selecionar a tabela PRODUTO no SQL
            # e mostrando uma mensagem ao usuario
            print('Selecionando os produtos')
            sql_sel = """select * from public. "PRODUTO" """
            # Usando o cursor para executar a variavel criada acima
            # e retornado os dados ao usuario
            cur.execute(sql_sel)
            reg = cur.fetchall()
            print(reg)

        except (Exception, psycopg2.Error) as error:
            print('Falha na Operação', error)

        finally:
            if (self.conn):
                cur.close()
                self.conn.close()
                print('A conexão oi fechada')
        return reg
    
# Definindo a função para selecionar um produto unico
    
    def selProduto(self, codigo):
        try:
            self.abrirConn()
            cur = self.conn.cursor()
            sql_sel = """select * from public."PRODUTO" 
            where "CODIGO" = %s"""
            cur.execute(sql_sel, (codigo,))
            record = cur.fetchone()
            print(record)
            
        except (Exception, psycopg2.Error) as error:
            print("Erro ao selecionar produto", error)
        finally:
            if(self.conn):
                cur.close()
                self.conn.close()
                print('A conexão oi fechada')
        return record


# Definindo a função para inserir produtos

    def insDados(self, codigo, nome, qtd):
        try:
            self.abrirConn()
            cur = self.conn.cursor()
            ins = """ INSER INTO public."PRODUTO"
             ("CODIGO", "NOME", "QTD") VALUES (%s,%s,%s)"""  # variavel que grava o codigo sql
            grav = (codigo, nome, qtd)  # variavel para gravar os valores
            cur.execute(ins, grav)
            self.conn.commit()
            count = cur.rowcount
            print(count, 'Registro inserido na tabela PRODUTO')
            nome_arquivo = "produto/"+ nome + ".txt"
            arquivo = open(nome_arquivo, "x", encoding="utf-8")
            with arquivo as escrita:
                escrita.write(f"Codigo do produto: {codigo}\nNome do produto: {nome}\nQuantidade inicial: {qtd}\nData do cadastro:{self.hoje}")
        except FileExistsError as error:
            print('Arquivo com este nome ja existe', error)
        except (Exception, psycopg2.Error) as error:
            if (self.conn):
                print('Falha ao inserir registro na tabela PRODUTO', error)
        finally:
            if (self.conn):
                cur.close()
                self.conn.close()
                print('A conexão oi fechada')
# Definindo a função para atualizar os dados

    def atuaDados(self, codigo, qtd):
        try:
            self.abrirConn()
            cur = self.conn.cursor()
            print('Registro antes da atualização')
            slct = """select * from public."PRODUTO" 
            where "CODIGO" =%s"""
            cur.execute(slct, (codigo))
            record = cur.fetchone()
            print(record)
            updt = """Update public. "PRODUTO" set 
            "QTD" = %s where "CODIGO" = %s"""
            cur.execute(updt,( qtd, codigo))
            self.conn.commit()
            count = cur.rowcount
            print(count, "registro atualizado com sucesso")
            print("registro depois da atualização")
            cur.execute(slct, (codigo))
            record = cur.fetchone()
            print(record)

        except(Exception, psycopg2.Error) as error:
            print("Erro na atualização", error)
        finally:
            if(self.conn):
                cur.close()
                self.conn.close()
                print('A conexão foi fechada')
#Definindo a função para excluir dados
    def exclDados(self, codigo):
        try:
            self.abrirConn()
            cur = self.conn.cursor()
            delete = """Delete from public. "PRODUTO"
             where "CODIGO" = %s"""
            cur.execute(delete, (codigo,))

            self.conn.commit()
            count = cur.rowcount
            print(count, "registro excluido")
        except(Exception, psycopg2.Error) as error:
            print("erro ao excluir", error)
        finally:
            if(self.conn):
                cur.close()
                self.conn.close()
                print("a conexão foi fechada")  