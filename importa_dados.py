#encoding='utf-8'
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
		self.resultado = list()

	def organiza_cenario(self):
		#Seleciona todas as nf's das compras e as coloca em uma lista
		notas_fiscais = list()
		for item in self.compras['Histórico separado']:
			notas_fiscais.append(item)
		#Cria um dataframe apenas com as NF para serem verificadas a cada
		#loop.
		df = pd.DataFrame(notas_fiscais)
		df['Histórico separado'] = df
		df_atual = pd.DataFrame(df['Histórico separado'])
		#Oragniza as datas das compras e dos pagamentos
		data_compras = list()
		for item in self.compras['Data']:
			data_compras.append(datetime.strptime(item, '%d/%m/%Y').date())
		novo_dataframe_compras = pd.DataFrame(data_compras)
		self.compras['Data'] = novo_dataframe_compras
		#--------------------
		data_pagamentos = list()
		for item in self.pagamentos['Data']:
			data_pagamentos.append(datetime.strptime(item, '%d/%m/%Y').date())
		novo_dataframe_pagamentos = pd.DataFrame(data_pagamentos)
		self.pagamentos['Data'] = novo_dataframe_pagamentos
		self.conferir(df_atual)
		
	def conferir(self, df_atual):
		#Seleciona a nf_atual
		for item in df_atual['Histórico separado']:
			if(item == 'Sem número'):
				self.resultado.append('Lançamento sem número de NF, por favor, corrigir')
				continue
			else:
				nf_atual = item
				#Seleção das compras--------------------
				#Seleciona as compras para serem somadas, com base na nf_atual
				selec_compras = self.compras.loc[(self.compras['Histórico separado'] == nf_atual)]
				#Seleciona o número da nf da compra
				for item in selec_compras['Histórico separado']:
					nf_atual_compra = item
				#Seleciona o número do fornecdor da compra atual
				n_fornecedor_atual = int()
				for item in selec_compras['Número']:
					n_fornecedor_atual = item
				#Pega os históricos para o resultado
				historico_resultado = str()
				for item in selec_compras['Histórico']:
					historico_resultado = item
				#Soma as compras
				selec_compra_com_numero = (selec_compras.loc[(selec_compras['Número'] == n_fornecedor_atual)])
				soma_compras = selec_compra_com_numero['Crédito'].sum().round(2)
				#Pega a data para o resultado
				for item in selec_compra_com_numero['Data']:
					data_resultado = item
				#Seleção dos pagamentos a prazo---------
				selec_pagamentos_prazo = self.pagamentos.loc[(self.pagamentos['Histórico separado'] == nf_atual_compra) & (self.pagamentos['Número'] == n_fornecedor_atual) & (self.pagamentos['Tipo'] == 1)]
				soma_pagamentos_prazo = selec_pagamentos_prazo['Débito'].sum().round(2)
				#Seleção dos pagamentos à vista---------
				selec_pagamentos_a_vista = self.pagamentos.loc[(self.pagamentos['Histórico separado'] == nf_atual_compra) & (self.pagamentos['Número'] == n_fornecedor_atual) & (self.pagamentos['Tipo'] == 2)]
				soma_pagamentos_a_vista = selec_pagamentos_a_vista['Débito'].sum().round(2)
				#Seleciona a data do pagamentoa à vista
				data_pagamento_a_vista = []
				for item in selec_pagamentos_a_vista['Data']:
					data_pagamento_a_vista = item
				#Seleciona as devoluções ---------------
				#Considera as devoluções integrais, sem divisão
				selec_devolucao = self.pagamentos.loc[(self.pagamentos['Número'] == n_fornecedor_atual) & (self.pagamentos['Tipo'] == 0)]
				soma_devolucao = selec_devolucao['Débito'].sum().round(2)
				#Considera as devoluções divididas, mas com o mesmo histórico
				selec_devolucao_dividida = selec_devolucao.loc[(selec_devolucao.duplicated('Histórico separado', keep=False))]
				soma_devolucao_dividida = selec_devolucao_dividida['Débito'].sum().round(2)


				#Começa a conferencia---------------------------

				#Deve verificar se a soma da compra atual é igual a soma de seus pagamentos a prazo
				if(soma_compras == soma_pagamentos_prazo):
					self.resultado.append('A compra está certa')
				#Deve verificar se a soma da compra atual é igual a soma de seu pagamento à vista
				elif(soma_compras == soma_pagamentos_a_vista):
					#Se a data da compra à vista for dieferente da data da compra, há um problema
					if(data_resultado == data_pagamento_a_vista):
						self.resultado.append('A compra está certa')
					elif(data_resultado != data_pagamento_a_vista):
						self.resultado.append('O pagamento da {} em {} Está com data errada'.format (historico_resultado, data_resultado))
				#Deve verificar se as compras estão sem pagamentos, se sim considerar dois fatos
				elif(soma_pagamentos_prazo == 0.0) & (soma_pagamentos_a_vista == 0.0):
					#1º) Se a compra tiver data anterior a data informada pelo usuário: A compra está sem pagamento
					if(data_resultado <= self.arquivo_data):
						self.resultado.append('A {} em {} Está sem pagamento'.format(historico_resultado, data_resultado))
					#2º) Se a compra estiverem sem pagamento: retornar, sem pagamento.
					else:
						self.resultado.append('A {} em {} Provavelmente será paga nos próximos meses'.format(historico_resultado, data_resultado))
				#Se a soma da compra não for igual a soma dos pagamentos à vista e nem dos pagamentos a prazo
				#deve verificar se há devoluções correspondentes ou pagamentos
				else:
					#Se a soma dos pagamentos a prazo + à vista forem igual a compra e verificar
					#a data dos pagamentos à vista
					if(soma_compras == soma_pagamentos_prazo + soma_pagamentos_a_vista) or (soma_pagamentos_prazo + soma_pagamentos_a_vista == soma_compras):
						if(data_resultado != data_pagamento_a_vista):
							self.resultado.append('O pagamento da {} em {} Está com data errada'.format (historico_resultado, data_resultado))
						else:
							self.resultado.append('A compra está certa')
					#Compras que tem a data maior a data informada pelo usuário, verificar se tem devolução,
					#pagamentos à vista ou se a diferença é igual a uma devolução
					elif(soma_compras != 0.0) & (data_resultado >= self.arquivo_data):
						diferenca = ((soma_compras - soma_pagamentos_prazo).round(2) if (soma_compras - soma_pagamentos_prazo).round(2) > 0 else (soma_pagamentos_prazo - soma_compras))
						bool_selec_devol_isolada = (self.pagamentos.loc[(self.pagamentos['Número'] == n_fornecedor_atual) & (self.pagamentos['Débito'] == diferenca) & (self.pagamentos['Tipo'] == 0)])
						selec_devol_isolada = bool_selec_devol_isolada['Débito'].round(2)
						devolucao = []
						for item in selec_devol_isolada:
							devolucao = item
						if(soma_compras == soma_devolucao) or (soma_compras == soma_devolucao_dividida):
							self.resultado.append('A compra está certa')
						elif(soma_compras != soma_pagamentos_prazo):
							if(diferenca == devolucao) or (diferenca == soma_pagamentos_a_vista):
								self.resultado.append('A compra está certa')
							else:
								self.resultado.append('A {} em {} Precisa ser averiguada'.format(historico_resultado, data_resultado))
					##Compras que tem a data inferior a data informada pelo usuário, verificar se tem devolução,
					#pagamentos à vista ou se a diferença é igual a uma devolução
					elif(soma_compras != 0.0) & (data_resultado < self.arquivo_data):
						diferenca = ((soma_compras - soma_pagamentos_prazo).round(2) if (soma_compras - soma_pagamentos_prazo).round(2) > 0 else (soma_pagamentos_prazo - soma_compras))
						bool_selec_devol_isolada = (self.pagamentos.loc[(self.pagamentos['Número'] == n_fornecedor_atual) & (self.pagamentos['Débito'] == diferenca) & (self.pagamentos['Tipo'] == 0)])
						selec_devol_isolada = bool_selec_devol_isolada['Débito'].round(2)
						devolucao = []
						for item in selec_devol_isolada:
							devolucao = item
						if(soma_compras == soma_devolucao) or (soma_compras == soma_devolucao_dividida):
							self.resultado.append('A compra está certa')
						elif(soma_compras != soma_pagamentos_prazo):
							if(diferenca == devolucao) or (diferenca == soma_pagamentos_a_vista):
								print(historico_resultado, 1)
								self.resultado.append('A compra está certa')
							else:
								self.resultado.append('A {} em {} Precisa ser averiguada'.format(historico_resultado, data_resultado))

	def debug(self):
		df_resultado = pd.DataFrame(self.resultado)
		self.compras['Resultado'] = df_resultado
		#df_final = pd.DataFrame(df_resultado['Resultado'])
		self.compras.to_csv('dados/resultado da conferencia.csv', sep=';', index= False, encoding='latin-1')	
		print('O arquivo de resultado foi criado')
#----------------------------
'''
Links úteis:
https://www.vooo.pro/insights/12-tecnicas-pandas-uteis-em-python-para-manipulacao-de-dados/

'''
#----------------------------
