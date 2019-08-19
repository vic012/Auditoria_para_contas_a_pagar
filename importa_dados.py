#-----------------------------
# Importa a biblioteca do pandas
import pandas as pd
import re
#-----------------------------

#-----------------------------
class Conferencia:

	def __init__(self):
		# Ler e importa os novos arquivos
		self.compras = pd.read_csv('dados\compras ajustadas.csv', sep=';', encoding='latin-1')
		self.pagamentos = pd.read_csv('dados\pagamentos ajustados.csv', sep=';', encoding='latin-1')
		# Variavel para o loop que contará a contagem necessária para percorrer as compras
		self.tamanho_da_lista = len(self.compras['Histórico separado'])
		self.contagem = 1
		self.resultado = list()
								
	# Definir um laço para percorrer todos o históricos das compras
	def loop_compras(self):
		while (self.contagem <= self.tamanho_da_lista):
			if(self.contagem > self.tamanho_da_lista):
				break
			else:
				#---Define a Nf que será verificada a cada loop designada nf_atual---#
				nf_atual = self.compras['Histórico separado'][self.contagem - 1]
				#---Seleção das compras---#
				selecao_compras = (self.compras['Histórico separado'] == nf_atual)
				soma_selecao_compras = (self.compras[selecao_compras]['Crédito'].sum().round(2))
				# debugger print(self.compras[selecao_compras])
				# debugger	print(soma_selecao_compras)

				#---Seleção dos pagamentos---#
				selecao_pagamentos = (self.pagamentos['Histórico separado'] == nf_atual)
				soma_selecao_pagamentos = (self.pagamentos[selecao_pagamentos]['Débito'].sum().round(2))
				# print(self.pagamentos[selecao_pagamentos])
				# debugger print(soma_selecao_pagamentos)

				#---Verifica se os valores dos pagamentos são iguais aos das compras---#
				if(soma_selecao_compras == soma_selecao_pagamentos):
					self.contagem += 1
					pass
				else:
					resultado = 'A nf {} precisa ser averiguada'.format(nf_atual)
					self.resultado.append(resultado)
					self.contagem += 1
					
	def debug(self):
		df = pd.DataFrame(self.resultado)
		df['Resultado'] = df
		df1 = df['Resultado']
		df_final = pd.DataFrame(df1)
		df_final.to_csv('dado\resultado da conferencia.csv', sep=';', index= False, encoding='latin-1')	
#-----------------------------
