import tkinter as tk
from tkinter import ttk
import datetime as datetime
import crud as crud


class PrincipalBD:
    def __init__(self, win):
        hoje = datetime.datetime.now()
        self.hDia = int(hoje.day) - 1
        self.hMes = int(hoje.month) - 1
        self.hAno = int(hoje.year) - 2023

        self.objBD = crud.AppBD()
        self.vDias = list(range(1, 32))
        self.vMes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.vAno = list(range(2023, 2051))
        # componentes
        self.lblCodigo = tk.Label(win, text='Código do Produto:')
        self.lblNome = tk.Label(win, text='Nome do Produto:')
        self.lblQtd = tk.Label(win, text='Quantidade:')
        self.lblDia = tk.Label(win, text='Dia:')
        self.lblMes = tk.Label(win, text='Mês:')
        self.lblAno = tk.Label(win, text='Ano:')

        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry(bd=3)
        self.txtQtd = tk.Entry(bd=3)

        self.diasCombo = ttk.Combobox(janela, values=self.vDias)
        self.mesCombo = ttk.Combobox(janela, values=self.vMes)
        self.anoCombo = ttk.Combobox(janela, values=self.vAno)

        self.btnCadastrar = tk.Button(
            win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnEntrada = tk.Button(
            win, text='Entrada', command=self.fEntradaProduto)
        self.btnSaida = tk.Button(
            win, text='Saida', command=self.fSaidaProduto)
        self.btnExcluir = tk.Button(
            win, text='Excluir', command=self.fExcluirProduto)
        self.btnLimpar = tk.Button(
            win, text='Limpar', command=self.fLimparTela)
        self.btnPesquisar = tk.Button(
            win, text='pesquiasar', command= self.fPesquisarProduto)
        # ----- Componente TreeView --------------------------------------------
        self.dadosColunas = ("Código", "Nome", "Quantidade")

        self.treeProdutos = ttk.Treeview(win,
                                         columns=self.dadosColunas,

                                         selectmode='browse')

        self.verscrlbar = ttk.Scrollbar(win,
                                        orient="vertical",
                                        command=self.treeProdutos.yview)
        self.verscrlbar.pack(side='right', fill='x')

        self.treeProdutos.configure(yscrollcommand=self.verscrlbar.set)

        self.treeProdutos.heading("#0", text="")
        self.treeProdutos.heading("Código", text="Código")
        self.treeProdutos.heading("Nome", text="Nome")
        self.treeProdutos.heading("Quantidade", text="Quatidade")

        self.treeProdutos.column("#0", width=0, stretch=0)
        self.treeProdutos.column("Código", minwidth=0, width=100)
        self.treeProdutos.column("Nome", minwidth=0, width=100)
        self.treeProdutos.column("Quantidade", minwidth=0, width=100)

        self.treeProdutos.pack(padx=3, pady=3)

        self.treeProdutos.bind("<<TreeviewSelect>>",
                               self.apresentarRegistrosSelecionados)
        # ---------------------------------------------------------------------
        # posicionamento dos componentes na janela
        # ---------------------------------------------------------------------
        self.lblCodigo.place(relx=0.24, rely=0.08)
        self.txtCodigo.place(relx=0.445, rely=0.08, relwidth=0.34)

        self.lblNome.place(relx=0.24, rely=0.14)
        self.txtNome.place(relx=0.445, rely=0.14, relwidth=0.34)

        self.lblQtd.place(relx=0.68, rely=0.36)
        self.txtQtd.place(relx=0.68, rely=0.4, relwidth=0.195)

        self.lblDia.place(relx=0.678, rely=0.44)
        self.diasCombo.place(relx=0.68, rely=0.465, relwidth=0.04)
        self.diasCombo.current(self.hDia)

        self.lblMes.place(relx=0.724, rely=0.44)
        self.mesCombo.place(relx=0.726, rely=0.465, relwidth=0.085)
        self.mesCombo.current(self.hMes)

        self.lblAno.place(relx=0.812, rely=0.44)
        self.anoCombo.place(relx=0.814, rely=0.465, relwidth=0.06)
        self.anoCombo.current(self.hAno)

        self.btnEntrada.place(relx=0.68, rely=0.5, relwidth=0.098)
        self.btnSaida.place(relx=0.78, rely=0.5, relwidth=0.098)
        self.btnCadastrar.place(relx=0.24, rely=0.8, relwidth=0.125)
        self.btnExcluir.place(relx=0.37, rely=0.8, relwidth=0.125)
        self.btnLimpar.place(relx=0.50, rely=0.8, relwidth=0.125)
        self.btnPesquisar.place(relx=0.60, rely=0.14)

        self.treeProdutos.place(relx=0.24, rely=0.36,
                                relheight=0.40, relwidth=0.4)
        self.verscrlbar.place(relx=0.630, rely=0.36, relheight=0.40)
        self.carregarDadosIniciais()
# -----------------------------------------------------------------------------

    def apresentarRegistrosSelecionados(self, event):
        self.fLimparTela()
        for selection in self.treeProdutos.selection():
            item = self.treeProdutos.item(selection)
            codigo, nome, preco = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
# -----------------------------------------------------------------------------

    def carregarDadosIniciais(self):
        try:
            self.id = 0
            self.iid = 0
            registros = self.objBD.selecionarDados()
            print("************ dados dsponíveis no BD ***********")
            for item in registros:
                codigo = item[0]
                nome = item[1]
                qtd = item[2]
                print("Código: ", codigo,
                      "\nNome:", nome,
                      "\nQuantidade Atual: ", qtd, "\n")

                self.treeProdutos.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo,
                                                 nome,
                                                 qtd))
                self.iid = self.iid + 1
                self.id = self.id + 1
            print('Dados da Base')
        except:
            print('Ainda não existem dados para carregar')


# -----------------------------------------------------------------------------
# Ler os dados da Tela
# -----------------------------------------------------------------------------


    def fLerCampos(self):
        try:
            print("************ dados disponíveis ***********")
            if (self.txtCodigo.get()):
                codigo = int(self.txtCodigo.get())
            else:
                codigo = 0
            print('codigo', codigo)
            nome = self.txtNome.get()
            print('nome', nome)
            nomePesquisa = (f"%{nome}%")
            print('nome pesquisa', nomePesquisa)
            if (self.txtQtd.get()):
                qtd = int(self.txtQtd.get())
            else:
                qtd = 0
            
            print('qtd', qtd)
            print('Leitura dos Dados com Sucesso!')
        except:
            print('Não foi possível ler os dados.')
        return codigo, nome, qtd, nomePesquisa
# -----------------------------------------------------------------------------
# Ler a data do menu dropdown
# -----------------------------------------------------------------------------

    def fLerDatas(self):
        try:
            dia = int(self.diasCombo.get())
            print('dia', dia)
            mes = self.mesCombo.get()
            print('mes', mes)
            ano = int(self.anoCombo.get())
            print('ano', ano)
            print('leitura da data com sucesso')
        except:
            print('Não foi possível ler a data')
        return dia, mes, ano
# -----------------------------------------------------------------------------
# Cadastrar Produto
# -----------------------------------------------------------------------------

    def fCadastrarProduto(self):
        try:
            print("************ dados disponíveis ***********")
            codigo, nome, qtd, nomeP = self.fLerCampos()
            dia, mes, ano = self.fLerDatas()
            self.objBD.inserirDados(codigo, nome, qtd)
            self.treeProdutos.insert('', 'end',
                                     iid=self.iid,
                                     values=(codigo,
                                             nome,
                                             qtd))
            self.iid = self.iid + 1
            self.id = self.id + 1
            self.fLimparTela()
            nome_arquivo = "produto/" + nome + ".txt"
            arquivo = open(nome_arquivo, "a", encoding="utf-8")
            with arquivo as escrita:
                escrita.write(f"\nData de cadastro: {dia} de {mes} de {ano}\n")

            print('Produto Cadastrado com Sucesso!')
        except:
            print('Não foi possível fazer o cadastro.')
# -----------------------------------------------------------------------------
# Atualizar Saida do Produto
# -----------------------------------------------------------------------------

    def fSaidaProduto(self):
        try:
            print("************ dados disponíveis ***********")

            codigo, nome, sqtd, nomeP = self.fLerCampos()
            dcodigo, dnome, dqtd = self.objBD.selecionarDadosUnicos(codigo)
            aqtd = dqtd - sqtd
            self.objBD.atualizarDados(codigo, aqtd)

            dia, mes, ano = self.fLerDatas()

            nome_arquivo = "produto/" + nome + ".txt"
            arquivo = open(nome_arquivo, "a", encoding="utf-8")
            with arquivo as escrita:
                escrita.write(f"\nSaida:\n{dia} de {mes} de {ano}\nQuantidade anterior: {dqtd}\nQuantidade de saida: {sqtd}\nQuantidade atual: {aqtd}\n")

            # recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Produto Atualizado com Sucesso!')
        except:
            print('Não foi possível fazer a atualização.')
# -------------------------------------------------------------------------------
# Atualizar Entrada do Produto
# -------------------------------------------------------------------------------

    def fEntradaProduto(self):
        try:
            print("************ dados disponíveis ***********")

            codigo, nome, entraadQtd, nomeP = self.fLerCampos()
            dcodigo, dnome, selecionarQtd = self.objBD.selecionarDadosUnicos(
                codigo)
            atualQtd = selecionarQtd + entraadQtd
            self.objBD.atualizarDados(codigo, atualQtd)

            dia, mes, ano = self.fLerDatas()

            nome_arquivo = "produto/" + nome + ".txt"
            arquivo = open(nome_arquivo, "a", encoding="utf-8")
            with arquivo as escrita:
                escrita.write(f"\nEntrada:\n{dia} de {mes} de {ano}\nQuantidade anterior: {selecionarQtd}\nQuantidade de entrada: {entraadQtd}\nQuantidade atual: {atualQtd}\n")
            # recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Produto Atualizado com Sucesso!')
        except:
            print('Não foi possível fazer a atualização.')
# -----------------------------------------------------------------------------
# Excluir Produto
# -----------------------------------------------------------------------------

    def fExcluirProduto(self):
        try:
            print("************ dados disponíveis ***********")
            codigo, nome, qtd, nomeP = self.fLerCampos()
            self.objBD.excluirDados(codigo)
            # recarregar dados na tela
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            self.carregarDadosIniciais()
            self.fLimparTela()
            print('Produto Excluído com Sucesso!')
        except:
            print('Não foi possível fazer a exclusão do produto.')
# -----------------------------------------------------------------------------
# Limpar Tela
# -----------------------------------------------------------------------------

    def fLimparTela(self):
        try:
            print("************ dados disponíveis ***********")
            self.txtCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtQtd.delete(0, tk.END)
            print('Campos Limpos!')
        except:
            print('Não foi possível limpar os campos.')
# ------------------------------------------------------------------------------
# Pesquisar Dados
# ------------------------------------------------------------------------------
    def fPesquisarProduto(self):
        try:
            
            rcodigo, rnome, rqtd, rnomePesquisa = self.fLerCampos()
            
            print(rnomePesquisa)
            registros = self.objBD.pesquisarDados(rnomePesquisa)
            self.iid = 0
            self.id = 0
            self.treeProdutos.delete(*self.treeProdutos.get_children())
            for item in registros:
                codigo = item[0]
                nome = item[1]
                qtd = item[2]
                print("Código: ", codigo,
                      "\nNome:", nome,
                      "\nQuantidade Atual: ", qtd, "\n")

                self.treeProdutos.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo,
                                                 nome,
                                                 qtd))
                self.iid = self.iid + 1
                self.id = self.id + 1
        except:
            print("Não foi possível pesquisar produto.")

# -----------------------------------------------------------------------------
# Programa Principal
# -----------------------------------------------------------------------------
janela = tk.Tk()
principal = PrincipalBD(janela)
janela.title('Bem Vindo a Aplicação de Banco de Dados')
janela.geometry("1080x720+10+10")
janela.mainloop()
# -----------------------------------------------------------------------------
