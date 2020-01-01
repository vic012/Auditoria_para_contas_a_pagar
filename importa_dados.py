#encoding='utf-8'
# Importa a biblioteca do pandas
import pandas as pd
from tkinter import *
from datetime import datetime
import re
import matplotlib.pyplot as plt
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
		self.quantidade_de_compras_analizadas = list()
		self.contagem_certa = list()
		self.contagem_certa_com_devolucao = list()
		self.contagem_averiguada = list()
		self.contagem_de_saldo = list()
		self.contagem_com_pagamento_errado = list()
		self.contagem_sem_pagamento = list()
		self.contagem_sem_numero = list()

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
		#__Cria uma lista para armazenar os históricos
		lista_para_historico = list()
		#__Cria uma lista para armazenar os números
		lista_para_numero = list()
		for historico in df_atual['Histórico separado']:
			if(historico == 'Sem número'):
				lista_para_historico.append('*')
			else:
				lista_para_historico.append(str(historico))
		for numero in df_atual['Número']:
			lista_para_numero.append(str(numero))
		#Cria um dataframe para os históricos retirados
		df_lista_para_historico = pd.DataFrame(lista_para_historico)
		#Cria um dataframe para os números retirados
		df_lista_para_numero = pd.DataFrame(lista_para_numero)
		#Cocatena os históricos com os númerosm formando assim um número de nf único
		lista_para_novo_historico = df_lista_para_historico + df_lista_para_numero
		#Cria um novo título
		df_atual['Histórico cocatenado'] = lista_para_novo_historico
		resultado = list()
		for item in df_atual['Histórico cocatenado']:
			filtro = re.findall('([*])',item)
			if(filtro == []):
				resultado.append(item)
			else:
				resultado.append('Sem número')
		df_atual['Histórico cocatenado'] = resultado
		# para teste: df_atual.to_excel('Teste.xlsx', index=False, encoding=False)
		#-------------------------------------------------------------------------------------------------------
		#Históricos das compras-------------------------------------------------------------------------------
		#__Cria uma lista para armazenar os históricos
		lista_para_historico_compras = list()
		#__Cria uma lista para armazenar os números
		lista_para_numero_compras = list()
		for historico_compras in self.compras['Histórico separado']:
			if(historico_compras == 'Sem número'):
				lista_para_historico_compras.append('*')
			else:
				lista_para_historico_compras.append(str(historico_compras))
		for numero_compras in self.compras['Número']:
			lista_para_numero_compras.append(str(numero_compras))
		#Cria um dataframe para os históricos retirados
		df_lista_para_historico_compras = pd.DataFrame(lista_para_historico_compras)
		#Cria um dataframe para os números retirados
		df_lista_para_numero_compras = pd.DataFrame(lista_para_numero_compras)
		#Cocatena os históricos com os númerosm formando assim um número de nf único
		lista_para_novo_historico_compras = df_lista_para_historico_compras + df_lista_para_numero_compras
		#Cria um novo título
		self.compras['Histórico cocatenado'] = lista_para_novo_historico_compras
		resultado_compras = list()
		for compras in self.compras['Histórico cocatenado']:
			filtro_compras = re.findall('([*])',compras)
			if(filtro_compras == []):
				resultado_compras.append(compras)
			else:
				resultado_compras.append('Sem número')
		self.compras['Histórico cocatenado'] = resultado_compras
		#self.compras.to_excel('Teste.xlsx', index=False, encoding=False)
		#-------------------------------------------------------------------------------------------------------
		#Históricos dos pagamentos------------------------------------------------------------------------------
		#__Cria uma lista para armazenar os históricos
		lista_para_historico_pagamentos = list()
		#__Cria uma lista para armazenar os números
		lista_para_numero_pagamentos = list()
		for historico_pagamentos in self.pagamentos['Histórico separado']:
			if(historico_pagamentos == 'Sem número'):
				lista_para_historico_pagamentos.append('*')
			else:
				lista_para_historico_pagamentos.append(str(historico_pagamentos))
		for numero_pagamentos in self.pagamentos['Número']:
			lista_para_numero_pagamentos.append(str(numero_pagamentos))
		#Cria um dataframe para os históricos retirados
		df_lista_para_historico_pagamentos = pd.DataFrame(lista_para_historico_pagamentos)
		#Cria um dataframe para os números retirados
		df_lista_para_numero_pagamentos = pd.DataFrame(lista_para_numero_pagamentos)
		#Cocatena os históricos com os númerosm formando assim um número de nf único
		lista_para_novo_historico_pagamentos = df_lista_para_historico_pagamentos + df_lista_para_numero_pagamentos
		#Cria um novo título
		self.pagamentos['Histórico cocatenado'] = lista_para_novo_historico_pagamentos
		resultado_pagamentos = list()
		for pagamentos in self.pagamentos['Histórico cocatenado']:
			filtro_pagamentos = re.findall('([*])',pagamentos)
			if(filtro_pagamentos == []):
				resultado_pagamentos.append(pagamentos)
			else:
				resultado_pagamentos.append('Sem número')
		self.pagamentos['Histórico cocatenado'] = resultado_pagamentos
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
		
		#tipos de informações para o gráfico
		#contagem dos erros
		quantidade_de_compras_analizadas = len(self.compras['Data'])
		contagem_certa = 0
		contagem_certa_com_devolucao = 0
		contagem_averiguada = 0
		contagem_de_saldo = 0
		contagem_com_pagamento_errado = 0
		contagem_sem_pagamento = 0
		contagem_sem_numero = 0

		#Seleciona a nf_atual
		for item in df_atual['Histórico cocatenado']:
			if(item == 'Sem número'):
				contagem_sem_numero += 1
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
					contagem_certa += 1
					self.resultado.append('A compra está certa')
					continue
				#Deve verificar se a soma da compra atual é igual a soma de seu pagamento à vista
				elif(soma_compras == soma_pagamentos_a_vista):
					#Se a data da compra à vista for dieferente da data da compra, há um problema
					if(data_resultado == data_pagamento_a_vista):
						contagem_certa += 1
						self.resultado.append('A compra está certa')
						continue
					elif(data_resultado != data_pagamento_a_vista):
						contagem_com_pagamento_errado += 1
						self.resultado.append('O pagamento da {} em {} Está com data errada'.format(historico_resultado, data_resultado))
						continue
				#Deve verificar se as compras estão sem pagamentos, se sim considerar dois fatos
				elif(soma_pagamentos_prazo == 0.0) & (soma_pagamentos_a_vista == 0.0):
				# & (soma_devolucao == 0.0) & (soma_devolucao_dividida == 0.0):
					#1º) Se a compra tiver data anterior a data informada pelo usuário: A compra está sem pagamento
					if(data_resultado <= self.arquivo_data):
						contagem_sem_pagamento += 1
						self.resultado.append('A {} em {} Está sem pagamento'.format(historico_resultado, data_resultado))
						continue
					#2º) Se a compra estiverem sem pagamento: retornar, sem pagamento.
					else:
						contagem_de_saldo += 1
						self.resultado.append('A {} em {} Provavelmente será paga nos próximos meses'.format(historico_resultado, data_resultado))
						continue
				#Se a soma da compra não for igual a soma dos pagamentos à vista e nem dos pagamentos a prazo
				#deve verificar se há devoluções correspondentes ou pagamentos
				else:
					#Se a soma dos pagamentos a prazo + à vista forem igual a compra e verificar
					#a data dos pagamentos à vista
					if(soma_compras == soma_pagamentos_prazo + soma_pagamentos_a_vista) or (soma_pagamentos_prazo + soma_pagamentos_a_vista == soma_compras):
						if(data_resultado != data_pagamento_a_vista):
							contagem_com_pagamento_errado += 1
							self.resultado.append('O pagamento da {} em {} Está com data errada'.format(historico_resultado, data_resultado))
							continue
						else:
							contagem_certa += 1
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
							contagem_certa_com_devolucao += 1
							self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
							continue
						elif(soma_compras != soma_pagamentos_prazo):
							if(diferenca == selec_devolucao).any():
								contagem_certa_com_devolucao += 1
								self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
								continue
							elif(diferenca == soma_pagamentos_a_vista):
								contagem_certa += 1
								self.resultado.append('A compra está certa')
								continue
							else:
								contagem_averiguada += 1
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
							contagem_certa_com_devolucao += 1
							self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
							continue
						elif(soma_compras != soma_pagamentos_prazo):
							if(diferenca == selec_devolucao).any():
								contagem_certa_com_devolucao += 1
								self.resultado.append('A compra está certa, o valor da devolução utilizada: {}, e o Nº da NF: {} '.format(string_devolucao, selec_numero_devolucao))
								continue
							elif(diferenca == soma_pagamentos_a_vista):
								contagem_certa += 1
								self.resultado.append('A compra está certa')
								continue
							else:
								contagem_averiguada += 1
								self.resultado.append('A {} em {} Precisa ser averiguada'.format(historico_resultado, data_resultado))
								continue

		#Os Dados do gráfico
		self.quantidade_de_compras_analizadas.append(quantidade_de_compras_analizadas)
		self.contagem_certa.append(contagem_certa)
		self.contagem_certa_com_devolucao.append(contagem_certa_com_devolucao)
		self.contagem_averiguada.append(contagem_averiguada)
		self.contagem_de_saldo.append(contagem_de_saldo)
		self.contagem_com_pagamento_errado.append(contagem_com_pagamento_errado)
		self.contagem_sem_pagamento.append(contagem_sem_pagamento)
		self.contagem_sem_numero.append(contagem_sem_numero)

	def debug(self):
		df_resultado = pd.DataFrame(self.resultado)
		self.compras['Resultado'] = df_resultado
		#df_final = pd.DataFrame(df_resultado['Resultado'])
		new_df = self.compras.drop('Histórico cocatenado', axis=1)
		new_df.to_excel('dados/resultado da conferencia.xlsx', index= False, encoding='latin-1')
		print('O arquivo de resultado foi criado')

		#CRIANDO O GRÁFICO DE BARRAS
		#dados
		eixo_y = [self.contagem_certa[0], self.contagem_certa_com_devolucao[0],
					self.contagem_averiguada[0], self.contagem_de_saldo[0],
					self.contagem_com_pagamento_errado[0], self.contagem_sem_pagamento[0],
					self.contagem_sem_numero[0]]
		eixo_x = [str(self.contagem_certa[0]), str(self.contagem_certa_com_devolucao[0]),
					str(self.contagem_averiguada[0]), str(self.contagem_de_saldo[0]),
					str(self.contagem_com_pagamento_errado[0]), str(self.contagem_sem_pagamento[0]),
					str(self.contagem_sem_numero[0])]

		plt.bar(eixo_x[0], eixo_y[0], color='#8f05f7')
		plt.bar(eixo_x[1], eixo_y[1], color='#f705ad')
		plt.bar(eixo_x[2], eixo_y[2], color='#05f7f7')
		plt.bar(eixo_x[3], eixo_y[3], color='#05f74f')
		plt.bar(eixo_x[4], eixo_y[4], color='#e8f705')
		plt.bar(eixo_x[5], eixo_y[5], color='#f75305')
		plt.bar(eixo_x[6], eixo_y[6], color='#311102')
		plt.ylabel('Quantidade por tipo de erro')
		plt.xlabel('Tipo de erro')
		plt.title('Foram analisadas: {} compras'.format(self.quantidade_de_compras_analizadas[0]))
		plt.legend(('Compra certa', 'Compra certa com utilização de devolução', 'Compra que precisa ser averiguada',
					'Compra (Saldo para próximos meses)', 'Compra com pagamento à vista errado', 'Compra sem pagamento',
					'Lançamento sem Nº de NF'))
		plt.show()
#----------------------------
'''
Links úteis:
https://www.vooo.pro/insights/12-tecnicas-pandas-uteis-em-python-para-manipulacao-de-dados/

'''
#----------------------------