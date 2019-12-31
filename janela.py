#encoding='utf-8'
# Importa a biblioteca de interfaces Tkinter
from tkinter import *
from datetime import datetime
from trata_dados import RetiraNumero
from importa_dados import Conferencia


# -----------------------------

# -----------------------------
# Cria a janela de diálogo com o usuário
# Variáveis globais que solicita ao usuário os nomes dos CSV's de comrpa e pagamentclass

class Janela:
    def __init__(self, master=None):
        self.fonte_padrao = ('Arial', '10')

        self.mensagem = Frame(master)
        self.mensagem['pady'] = 10
        self.mensagem['background'] = '#7988b5'
        self.mensagem.pack()

        self.titulo = Label(self.mensagem, text='Insira o nome dos arquivos')
        self.titulo['font'] = ('Calibri', '12')
        self.titulo['foreground'] = '#ffffff'
        self.titulo['background'] = '#7988b5'
        self.titulo.pack()

        self.arquivo_compra = Frame(master)
        self.arquivo_compra['padx'] = 6
        self.arquivo_compra['background'] = '#7988b5'
        self.arquivo_compra.pack()
        self.compra_label = Label(self.arquivo_compra, text='Arquivo de Compra:      ')
        self.compra_label['foreground'] = '#ffffff'
        self.compra_label['background'] = '#7988b5'
        self.compra_label.pack(side=LEFT)

        self.dados_compras = Entry(self.arquivo_compra)
        self.dados_compras['width'] = 30
        self.dados_compras['font'] = self.fonte_padrao
        self.dados_compras.pack(side=LEFT)

        self.arquivo_pagamento = Frame(master)
        self.arquivo_pagamento['padx'] = 6
        self.arquivo_pagamento['background'] = '#7988b5'
        self.arquivo_pagamento.pack()
        self.pagamento_label = Label(self.arquivo_pagamento, text='Arquivo de Pagamento:')
        self.pagamento_label['foreground'] = '#ffffff'
        self.pagamento_label['background'] = '#7988b5'
        self.pagamento_label.pack(side=LEFT)

        self.dados_pagamentos = Entry(self.arquivo_pagamento)
        self.dados_pagamentos['width'] = 30
        self.dados_pagamentos['font'] = self.fonte_padrao
        self.dados_pagamentos.pack(side=LEFT)

        self.arquivo_data = Frame(master)
        self.arquivo_data['padx'] = 6
        self.arquivo_data['background'] = '#7988b5'
        self.arquivo_data.pack()
        self.data_label = Label(self.arquivo_data, text='1º dia do último mês:    ')
        self.data_label['foreground'] = '#ffffff'
        self.data_label['background'] = '#7988b5'
        self.data_label.pack(side=LEFT)

        self.dados_data = Entry(self.arquivo_data)
        self.dados_data['width'] = 30
        self.dados_data['font'] = self.fonte_padrao
        self.dados_data.pack(side=LEFT)

        self.butões = Frame(master)
        self.butões['pady'] = 10
        self.butões['background'] = '#7988b5'
        self.butões.pack()

        self.feedback = Frame(master)
        self.feedback.pack()
        self.msgfeedback = Label(self.feedback, text='', font=self.fonte_padrao)
        self.msgfeedback['background'] = '#7988b5'
        self.msgfeedback.pack(side=LEFT)

        self.autentica = Button(self.butões)
        self.autentica['text'] = 'ENTER'
        self.autentica['font'] = ('Calibri', '8', 'bold')
        self.autentica['foreground'] = '#f68327'
        self.autentica['background'] = '#03125a'
        self.autentica['width'] = 8
        self.autentica['command'] = self.dados
        self.autentica.pack(side=LEFT)

        self.butões = Frame(master)
        self.butões['pady'] = 8
        self.butões['background'] = '#7988b5'
        self.butões.pack()

        self.feedback_conferencia = Frame(master)
        self.feedback_conferencia.pack()
        self.msgfeedback_conferencia = Label(self.feedback_conferencia, text='', font=self.fonte_padrao)
        self.msgfeedback_conferencia['foreground'] = '#ffffff'
        self.msgfeedback_conferencia['background'] = '#7988b5'
        self.msgfeedback_conferencia.pack(side=LEFT)

        self.butões_sair = Frame(master)
        self.butões_sair['pady'] = 12
        self.butões_sair['background'] = '#7988b5'
        self.butões_sair.pack()

        self.autentica = Button(self.butões)
        self.autentica['text'] = 'REALIZAR CONFERÊNCIA'
        self.autentica['font'] = ('Calibri', '8', 'bold')
        self.autentica['foreground'] = '#f68327'
        self.autentica['background'] = '#03125a'
        self.autentica['width'] = 20
        self.autentica['command'] = self.confere
        self.autentica.pack()

        self.autentica = Button(self.butões_sair)
        self.autentica['text'] = 'SAIR'
        self.autentica['font'] = ('Calibri', '8', 'bold')
        self.autentica['foreground'] = '#f68327'
        self.autentica['background'] = '#03125a'
        self.autentica['width'] = 8
        self.autentica['command'] = self.butões.quit
        self.autentica.pack()

    def dados(self):
        arquivo_compra = self.dados_compras.get()
        arquivo_pagamento = self.dados_pagamentos.get()
        organiza = RetiraNumero(arquivo_compra, arquivo_pagamento)
        organiza.historico_compras()
        organiza.historico_pagamentos()
        organiza.retira_sep_de_milhar()
        organiza.melhora_data_compra()
        organiza.cria_coluna_historico()
        organiza.novo_arquivo()
        self.msgfeedback['text'] = 'Os arquivos foram ajustados com sucesso!'
        self.msgfeedback['foreground'] = '#ffffff'
        self.msgfeedback['background'] = '#7988b5'
        
    def confere(self):
        arquivo_data = self.dados_data.get()
        data_formatada = datetime.strptime(arquivo_data, '%d/%m/%Y').date()
        confere = Conferencia(data_formatada)
        confere.organiza_cenario()
        confere.debug()
        self.msgfeedback_conferencia['text'] = 'Conferência realizada com sucesso!'
        self.msgfeedback_conferencia['foreground'] = '#ffffff'

root = Tk()
imagem = PhotoImage(file='.\\imagens\\icon.png')
root.configure(background='#7988b5')
root.title('Auditor')
root.iconphoto(False, imagem)
Janela(root)
root.mainloop()