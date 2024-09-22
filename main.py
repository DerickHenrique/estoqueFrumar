import tkinter as tk
from tkinter import ttk
import crud as crud

class MainBD:
    def __init__(self, win):
        self.objBD = crud.BaseBD()
        self.lblCodigo = tk.Label(win, text='Código do produto')
        self.lblNome = tk.Label(win, text='Nome do produto')
        self.lblQtd = tk.Label(win, text='Quantiade do produto')

        self.txtCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry(bd=3)
        self.txtQtd = tk.Entry(bd=3)

        self.btnCadastrar =tk.Button(win, text='Cadastrar', command=self.cadProduto)
        self.btnEntrada =tk.Button(win, text='Entrada', command=self.entProduto)
        self.btnSaida =tk.Button(win, text='Saida', command=self.saiProduto)
        self.btnExcluir =tk.Button(win, text='Excluir', command=self.exclProduto)
        self.btnLimpar =tk.Button(win, text='Limpar', command=self.clear)

        self.dadosColuna = ("Código", "Nome", "Quantidade")

        self.viewProdutos = ttk.Treeview(win,
                                         columns=self.dadosColuna,
                                         selectmode='browse')
        
        self.scrl = ttk.Scrollbar(win,
                                  orient='vertical',
                                  command=self.viewProdutos.yview)
        self.scrl.pack(side='right', fill='x')

        self.viewProdutos.configure(yscrollcommand=self.scrl.set)

        self.viewProdutos.heading("#0", text='')
        self.viewProdutos.heading("Código", text='Código')
        self.viewProdutos.heading("Nome", text='Nome')
        self.viewProdutos.heading("Quantidade", text='Quantidade')

        self.viewProdutos.column("#0", width=0, stretch=0)
        self.viewProdutos.column("Código", minwidth=0, width=100)
        self.viewProdutos.column("Nome", minwidth=0, width=100)
        self.viewProdutos.column("Quantidade", minwidth=0, width=100)

        self.viewProdutos.pack(padx=3, pady=3)
        
        self.viewProdutos.bind("<<TreeviewSelect>>",
                               self.showSel)
        
        self.lblCodigo.place(relx=0.24, rely=0.08)
        self.txtCodigo.place(relx=0.445, rely=0.08, relwidth=0.34)
        self.lblNome.place(relx=0.24, rely=0.14)
        self.txtNome.place(relx=0.445, rely=0.14, relwidth=0.34)
        self.lblQtd.place(relx=0.24, rely=0.20)
        self.txtQtd.place(relx=0.445, rely=0.20, relwidth=0.34)

        self.btnCadastrar.place(relx=0.24, rely=0.8, width=100)
        self.btnEntrada.place(relx=0.40, rely=0.25, width=100)
        self.btnSaida.place(relx=0.50, rely=0.25, width=100)
        self.btnExcluir.place(relx=0.529, rely=0.8, width=100)
        self.btnLimpar.place(relx=0.674, rely=0.8, width=100)

        self.viewProdutos.place(relx=0.24, rely=0.36, relheight=0.40, relwidth=0.55)
        self.scrl.place(relx=0.785, rely=0.36, relheight=0.40)
        self.carregarDados()

    def showSel(self, event):
        self.clear()
        for selection in self.viewProdutos.selection():
            item = self.viewProdutos.item(selection)
            codigo, nome, qtd = item["values"][0:3]
            self.txtCodigo.insert(0, codigo)
            self.txtNome.insert(0, nome)
            self.txtQtd.insert(0, qtd)

    def carregarDados(self):
        try:
            self.id = 0
            self.iid = 0
            registros = self.objBD.selDados()
            print("Dados disponives no Banco de Dados")
            for item in registros:
                codigo = item[0]
                nome = item [1]
                qtd = item [2]
                print("Código: ", codigo,
                      "\n Nome:", nome,
                      "\n Quantidade Atual: ", qtd)
                    
                self.viewProdutos.insert('', 'end',
                                         iid=self.iid,
                                         values=(codigo,
                                                 nome,
                                                 qtd))
                self.id = self.id + 1
                self.iid = self.iid + 1
            print('Dados da Base')
        except:
            print('Ainda não existem dados para carregar')

    def read(self):
        try:
          print("dados dsponíveis") 
          codigo = int(self.txtCodigo.get())
          print('codigo', codigo)
          nome= self.txtNome.get()
          print('nome', nome) 
          qtd= float(self.txtQtd.get())          
          print('qtd', qtd)
          print('Leitura dos Dados com Sucesso!')        
        except:
          print('Não foi possível ler os dados.')
        return codigo, nome, qtd

    def cadProduto(self):
        try:
           print("dados dsponíveis")
           codigo, nome, qtd = self.read()
           self.objBD.insDados(codigo, nome, qtd)
           self.viewProdutos.insert('','end',
                                    iid=self.iid,
                                    values=(codigo,
                                            nome,
                                            qtd))
           self.id = self.id + 1
           self.iid = self.iid + 1
           self.clear()
           print('produto cadastrado')
        except:
            print('Não foi possivel efetuar o cadastro')
        
    def entProduto(self):
        try:
            print("dados dsponíveis")
            codigo, nome, qtd = self.read()
            dcodigo, dnome, dqtd = self.objBD.selProduto(codigo)
            dqtd = dqtd + qtd
            self.objBD.atuaDados(codigo, dqtd)
            self.viewProdutos.delete(*self.viewProdutos.get_children())
            self.carregarDados()
            self.clear()
            print("Produto atualizado com sucesso")
        except:
            print("Não foi possivel dar entrada no produto")

    def saiProduto(self):
        try:
            print("dados dsponíveis")
            codigo, nome, qtd = self.read()
            dcodigo, dnome, dqtd = self.objBD.selProduto(codigo)
            dqtd = dqtd - qtd
            self.objBD.atuaDados(codigo, dqtd)
            self.viewProdutos.delete(*self.viewProdutos.get_children())
            self.carregarDados()
            self.clear()
            print("Produto atualizado com sucesso")
        except:
            print("Não foi possivel dar entrada no produto")

    def exclProduto(self):
        try:
            print("dados dsponíveis")
            codigo, nome, qtd = self.read()
            self.objBD.exclDados(codigo)
            self.viewProdutos.delete(*self.viewProdutos.get_children())
            self.carregarDados()
            self.clear()
            print("Produto excluido com sucesso")
        except:
            print("Não foi possivel excluir o produto")
    
    def clear(self):
        try:
            print("dados dsponíveis")
            self.txtCodigo.delete(0,tk.END)
            self.txtNome.delete(0,tk.END)
            self.txtQtd.delete(0,tk.END)
        except:
            print("Não foi possivel limpar os campos")



janela=tk.Tk()
principal=MainBD(janela)
janela.title('FRUMAR - estoque')
janela.geometry("1080x720+10+10")
janela.mainloop()