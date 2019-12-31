#encoding='utf-8'
# Importa a biblioteca do pandas
import pandas as pd
import re
from datetime import datetime
import pyautogui as pyg
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
		numero_do_fornecedor = list()
		for item in self.compras['Histórico separado']:
			notas_fiscais.append(item)
		for item in self.compras['Número']:
			numero_do_fornecedor.append(item)

		#Cria um dataframe apenas com as NF para serem verificadas a cada loop.
		df_historico = pd.DataFrame(notas_fiscais)
		df_numero = pd.DataFrame(numero_do_fornecedor)
		df_historico['Histórico separado'] = df_historico
		df_atual = pd.DataFrame(df_historico['Histórico separado'])
		df_atual['Número'] = df_numero
		df_atual['Índice'] = df_atual.index

		#Oragniza as datas das compras e dos pagamentos
		data_compras = list()
		for item in self.compras['Data']:
			data_compras.append(datetime.strptime(item, '%d/%m/%Y').date())
		novo_dataframe_compras = pd.DataFrame(data_compras)
		self.compras['Data'] = novo_dataframe_compras

		data_pagamentos = list()
		for item in self.pagamentos['Data']:
			data_pagamentos.append(datetime.strptime(item, '%d/%m/%Y').date())
		novo_dataframe_pagamentos = pd.DataFrame(data_pagamentos)
		self.pagamentos['Data'] = novo_dataframe_pagamentos
		#--------------------
		self.cocatenar(df_atual)

	def cocatenar(self, df_atual):
		#Essa função deverá cocatenar o número da NF com o número do fornecedor, gerando assim um número único
		
		#Históricos das NF_atual-------------------------------------------------------------------------------
		#__Cria uma lista para armazenar as notas fiscais
		nota_fiscal_sem_numero = list()
		for numero_da_nf in df_atual['Histórico separado']:
			#__Selecionar os números dos fornecedores com a nota fiscal pesquisada
			selecionar_numero = df_atual['Número'].loc[(df_atual['Histórico separado'] == numero_da_nf)]
			lista_para_df = list()
			for item in selecionar_numero:
				lista_para_df.append(item)
			df_df_atual = pd.DataFrame(lista_para_df)
			df_df_atual.drop_duplicates(keep='first', inplace=False)
			lista_para_numeros = list()
			for item in df_df_atual:
				lista_para_numeros.append(str(item))
			novo_numero = list()
			for item in lista_para_numeros:
				novo_numero.append(numero_da_nf + item)
			for item in novo_numero:
				nota_fiscal_sem_numero.append(item)
		df_atual['Histórico cocatenado'] = nota_fiscal_sem_numero
		#-------------------------------------------------------------------------------------------------------
		#Históricos das compras-------------------------------------------------------------------------------
		#__Cria uma lista para armazenar as notas fiscais
		nota_fiscal_sem_numero_compras = list()
		for numero_da_nf_com in self.compras['Histórico separado']:
			#__Selecionar os números dos fornecedores com a nota fiscal pesquisada
			selecionar_numero_com = self.compras['Número'].loc[(self.compras['Histórico separado'] == numero_da_nf_com)]
			lista_para_df = list()
			for item in selecionar_numero_com:
				lista_para_df.append(item)
			df_compras = pd.DataFrame(lista_para_df)
			df_compras.drop_duplicates(keep='first', inplace=False)
			lista_para_numeros_com = list()
			for item in selecionar_numero_com:
				lista_para_numeros_com.append(str(item))
			novo_numero_com = list()
			for item in lista_para_numeros:
				novo_numero_com.append(numero_da_nf_com + item)
			for item in novo_numero_com:
				nota_fiscal_sem_numero_compras.append(item)
		self.compras['Histórico cocatenado'] = nota_fiscal_sem_numero_compras
		#-------------------------------------------------------------------------------------------------------
		#Históricos dos pagamentos------------------------------------------------------------------------------
		#__Cria uma lista para armazenar as notas fiscais
		nota_fiscal_sem_numero_pagamentos = list()
		for numero_da_nf_pag in self.pagamentos['Histórico separado']:
			#__Selecionar os números dos fornecedores com a nota fiscal pesquisada
			selecionar_numero_pag = self.pagamentos['Número'].loc[(self.pagamentos['Histórico separado'] == numero_da_nf_pag)]
			lista_para_df = list()
			for item in selecionar_numero_pag:
				lista_para_df.append(item)
			df_pagamentos = pd.DataFrame(lista_para_df)
			df_pagamentos.drop_duplicates(keep='first', inplace=False)
			lista_para_numeros_pag = list()
			for item in selecionar_numero_pag:
				lista_para_numeros_pag.append(str(item))
			novo_numero_pag = list()
			for item in lista_para_numeros_pag:
				novo_numero_pag.append(numero_da_nf_pag + item)
			for item in novo_numero_pag:
				nota_fiscal_sem_numero_pagamentos.append(item)
		self.pagamentos['Histórico cocatenado'] = nota_fiscal_sem_numero_pagamentos
		#-------------------------------------------------------------------------------------------------------
		self.conferir(df_atual)

	def conferir(self, df_atual):
		#importar arquivos excel
		#pagamentos = pd.read_csv('pagamentos ajustados.csv', sep=';', encoding='latin-1')
		#dataframe = pd.DataFrame(self.pagamentos)

		#Separar somente as devoluções
		alldevolucoes = self.pagamentos.loc[(self.pagamentos['Tipo'] == 0)]
		#PARA TESTES: alldevolucoes.to_csv('devolucao.csv', sep=';', index=False, encoding='latin-1')

		#Selecionar ea agrupar as devoluções únicas, mas divididas
		#devolucao_div = pd.read_csv('devolucao.csv', sep=';', encoding='latin-1')
		agrupar = alldevolucoes.groupby(['Número', 'Histórico separado', 'Tipo']).sum().round(2)

		#Excluir a coluna débito para permitir excluir as duplicações
		alldevolucoes = alldevolucoes.drop('Débito', axis=1)

		#Excluir as duplicações onde somente o débito diferenciava
		alldevolucoes = alldevolucoes.drop_duplicates(keep='first')

		#Criar uma nova coluna débito com os totais das devoluções divididas em um segmento apenas
		valor_débito = list()
		for item in agrupar['Débito']:
			valor_débito.append(float(item))
		alldevolucoes['Débito'] = valor_débito
		
		#Cria um novo arquivo com as novas devoluções
		#PARA TESTES: alldevolucoes.to_csv('Devoluções.csv', sep=';', index=False, encoding='latin-1')
		
		#Seleciona a nf_atual
		for item in df_atual['Histórico cocatenado']:
			if(item == 'Sem número'):
				self.resultado.append('Lançamento sem número de NF, por favor, corrigir')
				continue
			else:
				#selecionar o nº da nf atual
				nf_atual = item
				
				#Seleção das compras--------------------
				#Seleciona as compras para serem somadas, com base na nf_atual
				selec_compras = self.compras.loc[(self.compras['Histórico cocatenado'] == nf_atual)]
				#Seleciona o número do fornecedor da compra atual
				n_fornecedor_atual = int()
				for item in selec_compras['Número']:
					n_fornecedor_atual = item
				#Seleciona o número da nf da compra
				for item in selec_compras['Histórico cocatenado']:
					for pagamento in self.pagamentos['Histórico cocatenado']:
						if (type(pagamento) == type('')):
							nf_atual_compra = str(item)
						else:
							nf_atual_compra = int(item)
				#Pega os históricos para o resultado
				historico_resultado = str()
				selec_historico = selec_compras.loc[(selec_compras['Histórico cocatenado'] == nf_atual_compra)]
				for item in selec_historico['Histórico']:
					historico_resultado = item
				#Soma as compras
				selec_compra_com_numero = (self.compras.loc[(self.compras['Histórico cocatenado'] == nf_atual_compra)])
				soma_compras = selec_compra_com_numero['Crédito'].sum().round(2)
				#Pega a data para o resultado
				for item in selec_compra_com_numero['Data']:
					data_resultado = item
				#Seleção dos pagamentos a prazo---------
				selec_pagamentos_prazo = self.pagamentos.loc[(self.pagamentos['Histórico cocatenado'] == nf_atual_compra) & (self.pagamentos['Tipo'] == 1)]
				soma_pagamentos_prazo = selec_pagamentos_prazo['Débito'].sum().round(2)
				#Seleção dos pagamentos à vista---------
				selec_pagamentos_a_vista = self.pagamentos.loc[(self.pagamentos['Histórico cocatenado'] == nf_atual_compra) & (self.pagamentos['Tipo'] == 2)]
				soma_pagamentos_a_vista = selec_pagamentos_a_vista['Débito'].sum().round(2)
				#Seleciona a data do pagamentoa à vista
				data_pagamento_a_vista = []
				for item in selec_pagamentos_a_vista['Data']:
					data_pagamento_a_vista = item

				#Começa a conferencia---------------------------
				#Deve verificar se a soma da compra atual é igual a soma de seus pagamentos a prazo
				if(soma_compras == soma_pagamentos_prazo):
					self.resultado.append('A compra está certa')
					continue
				#Deve verificar se a soma da compra atual é igual a soma de seu pagamento à vista
				elif(soma_compras == soma_pagamentos_a_vista):
					#Se a data da compra à vista for dieferente da data da compra, há um problema
					if(data_resultado == data_pagamento_a_vista):
						self.resultado.append('A compra está certa')
						continue
					elif(data_resultado != data_pagamento_a_vista):
						self.resultado.append('O pagamento da {} em {} Está com data errada'.format(historico_resultado, data_resultado))
						continue
				#Deve verificar se as compras estão sem pagamentos, se sim considerar dois fatos
				elif(soma_pagamentos_prazo == 0.0) & (soma_pagamentos_a_vista == 0.0):
				# & (soma_devolucao == 0.0) & (soma_devolucao_dividida == 0.0):
					#1º) Se a compra tiver data anterior a data informada pelo usuário: A compra está sem pagamento
					if(data_resultado <= self.arquivo_data):
						self.resultado.append('A {} em {} Está sem pagamento'.format(historico_resultado, data_resultado))
						continue
					#2º) Se a compra estiverem sem pagamento: retornar, sem pagamento.
					else:
						self.resultado.append('A {} em {} Provavelmente será paga nos próximos meses'.format(historico_resultado, data_resultado))
						continue
				#Se a soma da compra não for igual a soma dos pagamentos à vista e nem dos pagamentos a prazo
				#deve verificar se há devoluções correspondentes ou pagamentos
				else:
					#Se a soma dos pagamentos a prazo + à vista forem igual a compra e verificar
					#a data dos pagamentos à vista
					if(soma_compras == soma_pagamentos_prazo + soma_pagamentos_a_vista) or (soma_pagamentos_prazo + soma_pagamentos_a_vista == soma_compras):
						if(data_resultado != data_pagamento_a_vista):
							self.resultado.append('O pagamento da {} em {} Está com data errada'.format(historico_resultado, data_resultado))
							continue
						else:
							self.resultado.append('A compra está certa')
							continue
					#Compras que tem a data maior a data informada pelo usuário, verificar se tem devolução,
					#pagamentos à vista ou se a diferença é igual a uma devolução
					elif(soma_compras != 0.0) & (data_resultado >= self.arquivo_data):
						diferenca = ((soma_compras - soma_pagamentos_prazo).round(2) if (soma_compras - soma_pagamentos_prazo).round(2) > 0 else (soma_pagamentos_prazo - soma_compras))
						selec_devolucao = alldevolucoes['Débito'].loc[(alldevolucoes['Número'] == n_fornecedor_atual) & (alldevolucoes['Débito'] == diferenca)]
						selec_numero_devolucao = alldevolucoes['Histórico separado'].loc[(alldevolucoes['Número'] == n_fornecedor_atual) & (alldevolucoes['Débito'] == diferenca)].to_string(header=False)
						if(diferenca == selec_devolucao).any():
							string_devolucao = selec_devolucao = alldevolucoes['Débito'].loc[(alldevolucoes['Número'] == n_fornecedor_atual) & (alldevolucoes['Débito'] == diferenca)].to_string(header=False)
							self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
							continue
						elif(soma_compras != soma_pagamentos_prazo):
							if(diferenca == selec_devolucao).any():
								self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
								continue
							elif(diferenca == soma_pagamentos_a_vista):
								self.resultado.append('A compra está certa')
								continue
							else:
								self.resultado.append('A {} em {} Precisa ser averiguada'.format(historico_resultado, data_resultado))
								continue
					##Compras que tem a data inferior a data informada pelo usuário, verificar se tem devolução,
					#pagamentos à vista ou se a diferença é igual a uma devolução
					elif(soma_compras != 0.0) & (data_resultado < self.arquivo_data):
						diferenca = ((soma_compras - soma_pagamentos_prazo).round(2) if (soma_compras - soma_pagamentos_prazo).round(2) > 0 else (soma_pagamentos_prazo - soma_compras))
						selec_devolucao = alldevolucoes['Débito'].loc[(alldevolucoes['Número'] == n_fornecedor_atual) & (alldevolucoes['Débito'] == diferenca)]
						selec_numero_devolucao = alldevolucoes['Histórico separado'].loc[(alldevolucoes['Número'] == n_fornecedor_atual) & (alldevolucoes['Débito'] == diferenca)].to_string(header=False)
						if(diferenca == selec_devolucao).any():
							string_devolucao = selec_devolucao = alldevolucoes['Débito'].loc[(alldevolucoes['Número'] == n_fornecedor_atual) & (alldevolucoes['Débito'] == diferenca)].to_string(header=False)
							self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
							continue
						elif(soma_compras != soma_pagamentos_prazo):
							if(diferenca == selec_devolucao).any():
								self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
								continue
							elif(diferenca == soma_pagamentos_a_vista):
								self.resultado.append('A compra está certa')
								continue
							else:
								self.resultado.append('A {} em {} Precisa ser averiguada'.format(historico_resultado, data_resultado))
								continue

	def debug(self):
		df_resultado = pd.DataFrame(self.resultado)
		self.compras['Resultado'] = df_resultado
		#df_final = pd.DataFrame(df_resultado['Resultado'])
		self.compras.to_excel('dados/resultado da conferencia.xlsx', index= False, encoding='latin-1')	
		print('O arquivo de resultado foi criado')
#----------------------------
'''
Links úteis:
https://www.vooo.pro/insights/12-tecnicas-pandas-uteis-em-python-para-manipulacao-de-dados/

'''
#----------------------------