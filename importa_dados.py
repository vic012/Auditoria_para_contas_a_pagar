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
		self.resultado = list()
		
	def confronta(self):
		#Seleciona a compra atual a cada loop
		for nf_atual in self.compras['Histórico separado']:
		#Verifica se há alguma compra sem número e classifica a conferencia
			if (nf_atual == ['Sem número'] or nf_atual == 'Sem número'):
				pass
			else:
				#Seleciona as compras com a nf_atual
				seleciona_compra = (self.compras['Histórico separado'] == nf_atual)
				#seleciona a nf para ser conferida
				selecao_compra = (self.compras[seleciona_compra]['Histórico'])
				#Pega apenas o histórico
				for item in selecao_compra:
					historico_compras = item
				#Seleção data da compra para ser usada no resultado
				data_compras_resultado = (self.compras[seleciona_compra]['Data'].to_string(index=False))
				#Transforma a data em Strptime
				data_compras = (self.compras[seleciona_compra]['Data'])
				str_date = str()
				if(data_compras == '(Series[],)').any():
					pass
				else:
					str_date = data_compras.to_string(index=False).strip(' ')
				tamanho_limite_da_string = 9
				if(len(str_date) <= tamanho_limite_da_string):
					pass
				contagem = 0
				data_final = str()
				while (contagem <= tamanho_limite_da_string):
					if(len(str_date)==0):
						contagem += 1
						pass
					else:
						data_final = data_final + str_date[contagem]
						contagem += 1
				if(len(str_date)==0):
					pass
				else:
					data_das_compras = datetime.strptime(data_final, '%d/%m/%Y').date()
				#Soma as compras a cada loop em um total
				soma_selecao_compras = (self.compras[seleciona_compra]['Crédito'].sum().round(2))
				#------------------------------------
				
				#Seleciona o pagamento com a nf_atual
				selecao_pagamento = (self.pagamentos['Histórico separado'] == nf_atual)
				#Novo dataframe com os pagamentos que tem o mesmo número de nf que as sua compras
				todos_os_pagamentos = (self.pagamentos[selecao_pagamento])
				#Seleciona os pagamentos somente com o tipo (1)
				selecao_a_prazo = (todos_os_pagamentos['Tipo'] == 1)
				#Seleciona os pagamentos somente com o tipo (2)
				selecao_a_vista = (todos_os_pagamentos['Tipo'] == 2)
				#--------------------------------------------
				#Soma a seleção dos pagamentos a prazo com o nº da nf_atual
				soma_pagamentos_a_prazo = (todos_os_pagamentos[selecao_a_prazo]['Débito'].sum().round(2))
				#Soma a seleção dos pagamentos a vista com o nº da nf_atual
				soma_pagamentos_a_vista = (todos_os_pagamentos[selecao_a_vista]['Débito'].sum().round(2))
				#--------------------------------------------
				#----Realiza as conferências
				#Confere as compras que tenham pagamentos à vista ou que tenham devolução
				if(selecao_a_prazo).any():
					#Trata as datas A PRAZO para serem comparadas
					data_compra_a_prazo = (todos_os_pagamentos[selecao_a_prazo]['Data'])
					str_date_pagamento = str()
					if(data_compra_a_prazo == '(Series[],)').any():
						pass
					else:
						str_date_pagamento = data_compra_a_prazo.to_string(index=False).strip(' ')
					tamanho_limite_da_string_pagamento = 9
					if(len(str_date_pagamento) <= tamanho_limite_da_string_pagamento):
						pass
					contagem_pagamento = 0
					data_final_pagamento = str()
					while (contagem_pagamento <= tamanho_limite_da_string_pagamento):
						if(len(str_date_pagamento)==0):
							contagem_pagamento += 1
							pass
						else:
							data_final_pagamento = data_final_pagamento + str_date_pagamento[contagem_pagamento]
							contagem_pagamento += 1
					if(len(str_date_pagamento)==0):
						pass
					else:
						date_time_final_pagamento = datetime.strptime(data_final_pagamento, '%d/%m/%Y').date()
					#--------------------------------------------
					#----Realiza as conferências
					if(soma_selecao_compras == soma_pagamentos_a_prazo):
						pass
					else:
						if((soma_selecao_compras - soma_pagamentos_a_prazo).round(2) > 0):
							diferenca = (soma_selecao_compras - soma_pagamentos_a_prazo).round(2)
						else:
							diferenca = (soma_pagamentos_a_prazo - soma_selecao_compras).round(2)
						#Seleciona os pagamentos somente com o tipo (0)
						seleciona = (self.pagamentos['Débito'] == diferenca)
						seleciona_devolucao = (self.pagamentos[seleciona])
						devolucao = (seleciona_devolucao['Tipo'] == 0)
						#Soma a seleção das devoluções
						soma_devolucao = (seleciona_devolucao[devolucao]['Débito'].sum().round(2))
						#--------------------------------------------
						if(diferenca == soma_pagamentos_a_vista):
							#Trata as datas A VISTA para serem comparadas
							data_compra_a_vista = (todos_os_pagamentos[selecao_a_vista]['Data'])
							str_date_pagamento_a_vista = str()
							if(data_compra_a_vista == '(Series[],)').any():
								pass
							else:
								str_date_pagamento_a_vista = data_compra_a_vista.to_string(index=False).strip(' ')
							tamanho_limite_da_string_pagamento_a_vista = 9
							if(len(str_date_pagamento_a_vista) <= tamanho_limite_da_string_pagamento_a_vista):
								pass
							contagem_pagamento_a_vista = 0
							data_final_pagamento_a_vista = str()
							while (contagem_pagamento_a_vista <= tamanho_limite_da_string_pagamento_a_vista):
								if(len(str_date_pagamento_a_vista)==0):
									contagem_pagamento_a_vista += 1
									pass
								else:
									data_final_pagamento_a_vista = data_final_pagamento_a_vista + str_date_pagamento_a_vista[contagem_pagamento_a_vista]
									contagem_pagamento_a_vista += 1
							if(len(str_date_pagamento_a_vista)==0):
								pass
							else:
								date_time_final_pagamento_a_vista = datetime.strptime(data_final_pagamento_a_vista, '%d/%m/%Y').date()
							#--------------------------------------------
							if(data_das_compras != date_time_final_pagamento_a_vista):
								self.resultado.append('O pagamento da {} em {} está errado'.format(historico_compras, data_compras_resultado))
							else:
								pass
						elif(diferenca == soma_devolucao):
							pass
						else:
							self.resultado.append('A {} em {} precisa ser corrigida'.format(historico_compras, data_compras_resultado))
				elif(selecao_a_vista).any():
					#Trata as datas A VISTA para serem comparadas
					data_compra_a_vista = (todos_os_pagamentos[selecao_a_vista]['Data'])
					str_date_pagamento_a_vista = str()
					if(data_compra_a_vista == '(Series[],)').any():
						pass
					else:
						str_date_pagamento_a_vista = data_compra_a_vista.to_string(index=False).strip(' ')
					tamanho_limite_da_string_pagamento_a_vista = 9
					if(len(str_date_pagamento_a_vista) <= tamanho_limite_da_string_pagamento_a_vista):
						pass
					contagem_pagamento_a_vista = 0
					data_final_pagamento_a_vista = str()
					while (contagem_pagamento_a_vista <= tamanho_limite_da_string_pagamento_a_vista):
						if(len(str_date_pagamento_a_vista)==0):
							contagem_pagamento_a_vista += 1
							pass
						else:
							data_final_pagamento_a_vista = data_final_pagamento_a_vista + str_date_pagamento_a_vista[contagem_pagamento_a_vista]
							contagem_pagamento_a_vista += 1
					if(len(str_date_pagamento_a_vista)==0):
						pass
					else:
						date_time_final_pagamento_a_vista = datetime.strptime(data_final_pagamento_a_vista, '%d/%m/%Y').date()
					#--------------------------------------------
					#----Realiza as conferências
					if(soma_selecao_compras == soma_pagamentos_a_vista):
						if(data_das_compras != date_time_final_pagamento_a_vista):
							self.resultado.append('O pagamentos da {} em {} está errado'.format(historico_compras, data_compras_resultado))
						else:
							pass
					else:
						if((soma_selecao_compras - soma_pagamentos_a_vista).round(2) > 0):
							diferenca = ((soma_selecao_compras - soma_pagamentos_a_vista).round(2))
						else:
							diferenca = ((soma_pagamentos_a_vista - soma_selecao_compras).round(2))
						#Seleciona os pagamentos somente com o tipo (0)
						seleciona = (self.pagamentos['Débito'] == diferenca)
						seleciona_devolucao = (self.pagamentos[seleciona])
						devolucao = (seleciona_devolucao['Tipo'] == 0)
						#Soma a seleção das devoluções
						soma_devolucao = (seleciona_devolucao[devolucao]['Débito'].sum().round(2))
						if(diferenca == soma_devolucao):
							pass
						else:
							self.resultado.append('A {} em {} precisa ser corrigida'.format(historico_compras, data_compras_resultado))
				elif(data_das_compras >= self.arquivo_data):
					self.resultado.append('A {} em {} provavelmente será paga no próximo mês'.format(historico_compras, data_compras_resultado))
				else:
					self.resultado.append('A {} em {} está sem pagamento'.format(historico_compras, data_compras_resultado))
	
	def debug(self):
		df_resultado = pd.DataFrame(self.resultado)
		df_resultado['Resultado'] = df_resultado
		df_final = pd.DataFrame(df_resultado['Resultado'])
		df_final.to_csv('dados/resultado da conferencia.csv', sep=';', index= False, encoding='latin-1')	
		print('O arquivo de resultado foi criado')
#-----------------------------
