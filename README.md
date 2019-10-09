# Esse repositório tem o objeivo de mostrar o uso de técnicas de data science para a conferência de relatórios contábeis.

# O Objetivo do projeto
### O objetivo desse projeto é realizar uma tarefa trivial, mas que demanda muito tempo dos profissionais contábeis, essa tarefa consiste em averiguar longas páginas de relatórios contábeis, analisando se cada compra recebeu o seu devido pagamento, só que esses relatórios chegam a ter centenas de páginas com centenas de fornecedores diferentes e milhares de transações entre eles, sendo assim, esse script será capaz de realizar uma grande função afim de otimizar o tempo gasto, o script fará esta análise e retornará apenas as compras que apresentarem problemas afim de que os responsáveis possam analisar e realizar os devidos ajustes.

# Como funciona?
1) o script abrirá uma janela solicitando três informações ao usuário:
 1.1 - O nome do arquivo (csv) das compras na pasta dados;
 1.2 - O nome do arquivo (csv) dos pagamentos também na pasta dados;
 1.3 - O primeiro dia do último mês do relatório, pois o último mês influencia nos saldos finais, por isso as compras acima desta data devem ser averiguadas de forma diferente das demais.

2) Os arquivos serão tratados para serem conferidos, assim dois novos (csv's) serão criados: Compras ajustada e Pagamentos ajustados.

3) Logo após a conferência chega ao seu climax, onde será criado um outro (csv) contendo os erros encontrados e também as compras certas, assim o usuário pode abrir esse arquivo e com um simples filtro desconsiderar as compras certas e então poderá averiguar os erros.

### Uma tarefa que grande parte dela demandaria dias, agora pode ser realizada em questão de minutos.

# Instruções:
1) Clone o repositório com todos os arquivos inclusive a pasta dados;
2) Execute o arquivo janela.py, este será responsável de criar a interação entre o usuário e o script;

* Linguagem do projeto: Python
* os arquivos csv na pasta dados, não são reais na verdade eles estão incompletos, eles servem apenas como exemplo, para uma melhor experiência, utilize arquivos reais com a mesma estrutura e tipo de arquivo que os apresentados nos exemplos na pasta dados.
* Microserviço: Pode ser que esse projeto não se aplique a sua necessidade, pois ele se aplica a uma demanda de um escritório que fornece os relatórios que são auditados por este script, se você não tiver esses relatórios (nos mesmos padrões dos que estão, como exemplo, na pasta dados) talvez não consiga usar o script, pois ele foi configurado para um formato específico de CSV, se esse for o seu caso, você pode criar uma estrutura que lhe posibilite usar o sistema (Uma boa ferramenta para esta função é o VBA).
* Ou se preferir, você pode estudar o código e usar da forma que melhor lhe atender, apenas peço que cite em seu projeto este repositório como fonte, pois este código é aberto, mas foi preciso longos períodos de estudos para realizá-lo
