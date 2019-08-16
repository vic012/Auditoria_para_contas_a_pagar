#-----------------------------
# Importa a biblioteca de interfaces Tkinter
from tkinter import *
from trata_dados import RetiraNumero
from importa_dados import Conferencia
#-----------------------------

#-----------------------------
# Cria a janela de diálogo com o usuário
# Variáveis globais que solicita ao usuário os nomes dos CSV's de comrpa e pagamentclass

class Janela:
	def __init__(self, master=None):
		self.fonte_padrao = ("Arial", "10")

		self.mensagem = Frame(master)
		self.mensagem["pady"] = 5
		self.mensagem.pack()

		self.titulo = Label(self.mensagem, text="Insira o nome dos arquivos")
		self.titulo["font"] = self.fonte_padrao
		self.titulo.pack()

		self.arquivo_compra = Frame(master)
		self.arquivo_compra["padx"] = 6
		self.arquivo_compra.pack()
		self.compra_label = Label(self.arquivo_compra, text="Compra:      ")
		self.compra_label.pack(side=LEFT)

		self.dados_compras = Entry(self.arquivo_compra)
		self.dados_compras["width"] = 30
		self.dados_compras["font"] = self.fonte_padrao
		self.dados_compras.pack(side=LEFT)

		self.arquivo_pagamento = Frame(master)
		self.arquivo_pagamento["padx"] = 7
		self.arquivo_pagamento.pack()
		self.pagamento_label = Label(self.arquivo_pagamento, text="Pagamento:")
		self.pagamento_label.pack(side=LEFT)

		self.dados_pagamentos = Entry(self.arquivo_pagamento)
		self.dados_pagamentos["width"] = 30
		self.dados_pagamentos["font"] = self.fonte_padrao
		self.dados_pagamentos.pack(side=LEFT)

		self.butões = Frame(master)
		self.butões["pady"] = 10
		self.butões.pack()

		self.feedback = Frame(master)
		self.feedback.pack()
		self.msgfeedback = Label(self.feedback, text="", font=self.fonte_padrao)
		self.msgfeedback.pack(side=LEFT)

		self.autentica = Button(self.butões)
		self.autentica["text"] = "ENTER"
		self.autentica["font"] = ("Calibri", "8")
		self.autentica["width"] = 8
		self.autentica["command"] = self.dados
		self.autentica.pack(side=LEFT)

		self.butões = Frame(master)
		self.butões["pady"] = 8
		self.butões.pack()

		self.feedback_conferencia = Frame(master)
		self.feedback_conferencia.pack()
		self.msgfeedback_conferencia = Label(self.feedback_conferencia, text="", font=self.fonte_padrao)
		self.msgfeedback_conferencia.pack(side=LEFT)

		self.butões_sair = Frame(master)
		self.butões_sair["pady"] = 10
		self.butões_sair.pack()

		self.autentica = Button(self.butões)
		self.autentica["text"] = "Realizar conferência"
		self.autentica["font"] = ("Calibri", "10", "bold")
		self.autentica["width"] = 20
		self.autentica["command"] = self.confere
		self.autentica.pack()

		self.autentica = Button(self.butões_sair)
		self.autentica["text"] = "SAIR"
		self.autentica["font"] = ("Calibri", "8")
		self.autentica["width"] = 8
		self.autentica["command"] = self.butões.quit
		self.autentica.pack()

	def dados(self):
		arquivo_compra = self.dados_compras.get()
		arquivo_pagamento = self.dados_pagamentos.get()
		organiza = RetiraNumero(arquivo_compra, arquivo_pagamento)
		organiza.historico_compras()
		organiza.historico_pagamentos()
		organiza.retira_sep_de_milhar()
		organiza.cria_coluna_historico()
		organiza.novo_arquivo()
		self.msgfeedback["text"] = "Os arquivos foram inseridos com sucesso!"
	
	def confere(self):
		confere = Conferencia()
		confere.loop_compras()
		confere.debug()
		self.msgfeedback_conferencia["text"] = "Conferencia realizada com sucesso!"

root = Tk()
Janela(root)
root.mainloop()