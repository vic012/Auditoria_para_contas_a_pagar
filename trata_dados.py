#Importação das bibliotecas
# Importa o pandas para conectar o csv com o banco de dados
import pandas as pd
# Importa as expressões regulares para lidar com os dados
# dos csv's
import re
from datetime import datetime
class RetiraNumero:
	def __init__(self, arquivo_compra = "", arquivo_pagamento=""):
		#-----------------------------
		# Lê os dados do csv e trata de acordo com a forma precisa para conferir

		# Ativando a leitura do banco de dados pelo pandas (pd)
		self.arquivo_compra = "dados\{}".format(arquivo_compra)
		self.arquivo_pagamento = "dados\{}".format(arquivo_pagamento)
		self.compras = pd.read_csv(self.arquivo_compra, sep = ';', encoding = 'latin-1')
		self.pagamentos = pd.read_csv(self.arquivo_pagamento, sep = ';', encoding = 'latin-1')
        # Receberá os números das notas fiscais de compra e pagamento
        # Essas varíavies são uma do tipo lista e receberão números inteiros
		self.data = list()
		self.historico_das_compras = list()
		self.historico_dos_pagamentos = list()
		self.valores_compras_formatados = list()
		self.valores_pagamentos_formatados = list()

		'''Campo das funcionalidades do Objeto, aqui estarão as funções e métodos'''
		# A função historico_compras(self) e historico_pagamentos(self) cria um loop e retira os números dos históricos e os passa para
		# as variáveis self.historico_das_compras e historico_dos_pagamentos na forma de número inteiros.

	def historico_compras(self):
		# Um laço é feito para percorrer cada linha dos históricos e retirar os números individualmente
		for i in self.compras['Histórico']:
			resultado = list()
			resultado_composto = list()
			# Para retirar os números, é preciso utilizar Expressões Regulares para encontrar números(str) no meio dos históricos,
			# pois eles estão juntos no mesmo campo.
			filtro = re.findall('([0-9]+)',i)
			# Outro laço é criado para garantir que cada nota fiscal seja adicionada na lista self.historico_das_compras de um por um.
			# E também os números serão retornados como inteiros
			for item in filtro:
				if(item == []):
					pass
				else:
					resultado.append(item)
			if (len(resultado) > 1):
				resultado.pop(-1)
			else:
				pass
			for item in resultado:
				if(item == []):
					pass
				else:
					self.historico_das_compras.append([resultado[0]])
			
	# As funcionalidades dessa função muito se assemelha com a anterior, o que muda é que aqui o foco está nos pagamentos e não nas compras,
	# Por isso caso necessário consulte os comentários da função anterior.
	def historico_pagamentos(self):
		for i in self.pagamentos['Histórico']:
			resultado = list()
			# Para retirar os números, é preciso utilizar Expressões Regulares para encontrar números(str) no meio dos históricos,
			# pois eles estão juntos no mesmo campo.
			filtro = re.findall('([0-9]+)',i)
			# Outro laço é criado para garantir que cada nota fiscal seja adicionada na lista self.historico_das_compras de um por um.
			# E também os números serão retornados como inteiros
			for item in filtro:
				if(item == []):
					pass
				else:
					resultado.append(item)
			if (len(resultado) > 1):
				resultado.pop(-1)
			else:
				pass
			for item in resultado:
				if(item == []):
					pass
				else:
					self.historico_dos_pagamentos.append([resultado[0]])

	def retira_sep_de_milhar(self):
		for i in self.compras['Crédito']:
			retira_ponto = i.replace('.' , '')
			retira_virgula = retira_ponto.replace(',', '.')
			self.valores_compras_formatados.append(float(retira_virgula))
		for i in self.pagamentos['Débito']:
			retira_ponto = i.replace('.' , '')
			retira_virgula = retira_ponto.replace(',', '.')
			self.valores_pagamentos_formatados.append(float(retira_virgula))

	def melhora_data_compra(self):
		for item in self.compras['Data']:
			data = str(item)
			self.data.append(data)

	def cria_coluna_historico(self):
		# Tendo separado os históricos das compras e dos pagamentos, agora criamos uma nova coluna
		# ['Histórico separado'] contendo as NF's sem nenhuma influencia do histórico passado.
		df_compras = pd.DataFrame(self.historico_das_compras)
		self.compras['Data'] = self.data
		self.compras['Histórico separado'] = df_compras
		self.compras['Crédito'] = self.valores_compras_formatados
		df_pagamentos = pd.DataFrame(self.historico_dos_pagamentos)
		self.pagamentos['Histórico separado'] = df_pagamentos
		self.pagamentos['Débito'] = self.valores_pagamentos_formatados

	def novo_arquivo(self):
		# Agora, tendo organizado os dados, como boa prática, é criado um arquivo novo que recebe os dados
		# dos arquivos originais e a nova coluna com os histórios já formatados afim de não alterar os arquivos originais
		self.compras.to_csv('dados\compras ajustadas.csv', sep=';', index= False, encoding='latin-1')
		self.pagamentos.to_csv('dados\pagamentos ajustados.csv', sep=';', index= False, encoding='latin-1')
		# Transmite a mensagem de que o script funcionou ao usuário
		print("Os Históricos das compras e dos pagamentos foram ajustados!")

#-----------------------------