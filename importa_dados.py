#-----------------------------
# Importa a biblioteca do pandas
import pandas as pd
import re
from datetime import datetime
#-----------------------------

#-----------------------------
class Conferencia:

	def __init__(self, arquivo_data):
		# Ler e importa os novos arquivos
		self.compras = pd.read_csv('dados\compras ajustadas.csv', sep=';', encoding='latin-1')
		self.pagamentos = pd.read_csv('dados\pagamentos ajustados.csv', sep=';', encoding='latin-1')
		# Variavel para o loop que contará a contagem necessária para percorrer as compras
		self.arquivo_data = arquivo_data
		self.tamanho_da_lista = len(self.compras['Histórico separado'])
		self.data_das_compras = list()
		self.data_dos_pagamentos = list()
		self.contagem = 1
		self.resultado = list()
		self.resultado_saldo = list()
	
	def altera_datas(self):
		for item in self.compras['Data']:
			nova_data_compras = datetime.strptime(item, '%d/%m/%Y').date()
			self.data_das_compras.append(nova_data_compras)
		for item in self.pagamentos['Data']:
			nova_data_pagamentos = datetime.strptime(item, '%d/%m/%Y').date()
			self.data_dos_pagamentos.append(nova_data_pagamentos)

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
				
				#---Seleção da data atual---#
				data = self.compras[selecao_compras]['Data']
				str_date = data.to_string(index=False).strip(' ')
				tamanho_limite_da_string = 9
				if(len(str_date) <= tamanho_limite_da_string):
					pass
				contagem = 0
				data_final = str()
				while (contagem <= tamanho_limite_da_string):
					data_final = data_final + str_date[contagem]
					contagem += 1
					
				date_time_final = datetime.strptime(data_final, '%d/%m/%Y').date()
				
				# verifica a diferença entre o valor de uma compra e o seu pagamento
				diferenca = (soma_selecao_compras - soma_selecao_pagamentos).round(2)
				selecao = (self.pagamentos['Débito'] == diferenca)
				valor_devolucao = self.pagamentos[selecao]['Débito']

				#---Verifica se os valores dos pagamentos são iguais aos das compras---#
				if(soma_selecao_compras == soma_selecao_pagamentos):
					self.contagem += 1
					pass
				elif(soma_selecao_compras != soma_selecao_pagamentos and date_time_final >= self.arquivo_data):
					resultado = 'A {} em {} provavelmente será paga nos próximos meses'.format(self.compras['Histórico'][self.contagem-1], self.compras['Data'][self.contagem - 1])										
					self.resultado_saldo.append(resultado)
					self.contagem += 1
					pass
				else:
					for item in valor_devolucao:
						if(item == diferenca):	
							self.contagem += 1
							pass
					resultado = 'A {} em {} precisa ser averiguada'.format(self.compras['Histórico'][self.contagem-1], self.compras['Data'][self.contagem - 1])
					self.resultado.append(resultado)
					self.contagem += 1
										
	def debug(self):
		df_resultado = pd.DataFrame(self.resultado)
		df_resultado_saldo = pd.DataFrame(self.resultado_saldo)
		df_final = pd.concat([df_resultado,df_resultado_saldo])
		df_final['Resultado'] = df_final
		df_final_1 = pd.DataFrame(df_final['Resultado'])
		df_final_1.to_csv('dados/resultado da conferencia.csv', sep=';', index= False, encoding='latin-1')	
#-----------------------------
