# Esse repositório tem o objetivo de mostrar o uso de técnicas de data science para conferência de relatórios contábeis.

# O Objetivo do projeto
### O objetivo desse projeto é realizar uma tarefa trivial, mas que demanda muito tempo dos profissionais contábeis, essa tarefa consiste em averiguar longas páginas de relatórios contábeis, analisando se cada compra recebeu o seu devido pagamento, só que esses relatórios chegam a ter centenas de páginas com centenas de fornecedores diferentes e milhares de transações entre eles, sendo assim, esse script será capaz de realizar uma grande função afim de otimizar o tempo gasto, o script fará esta análise e retornará apenas as compras que apresentarem problemas afim de que os responsáveis possam analisar e realizar os devidos ajustes.

# Como funciona?
1) O script abrirá uma janela solicitando três informações ao usuário:
 1.1 - O nome do arquivo (csv) das compras na pasta dados;
 1.2 - O nome do arquivo (csv) dos pagamentos também na pasta dados;
 1.3 - O primeiro dia do último mês do relatório, pois o último mês influencia nos saldos finais, por isso as compras acima desta data devem ser averiguadas de forma diferente das demais.
 

2) Os arquivos serão tratados para serem conferidos, assim dois novos (csv's) serão criados: Compras ajustadas e Pagamentos ajustados.

3) Logo após a conferência chega ao seu clímax, onde serão criados dois novos relatórios (csv) contendo os erros encontrados e também as compras certas chamado de RESULTADO DA CONFERÊNCIA e outro relatório também em excel contendo as devoluções que não foram utilizadas com o nome DEVOLUÇÕES NÃO UTILIZADAS, assim o usuário pode abrir esses dois arquivos e com um simples filtro desconsiderar as compras certas e então poderá averiguar os erros.

### Uma tarefa que grande parte dela demandaria dias, agora pode ser realizada em questão de minutos.

# Instruções:
1) Clone a pasta Dados e o arquivo "Download do drive" para o seu PC;
2) Abra o txt "Download do drive", nele há um link (repositório do google drive) que contém um executável com todas as pastas do projeto e seus arquivos, depois de baixar o Auditor.exe execute-o, ele fará a pré-instalação do software;
3) Copie a pasta dados que você clonou do repositório para o caminho dist/janela e se houver uma pasta chamada dados substitua pela "dados" que você baixou, *Não mude o nome da pasta dados, o software vai procurar por ela*;
4) Agora crie um atalho da pasta |dados| para a área de trabalho (mude seu ícone se quiser, existem opções na pasta imagem), essa pasta será onde você vai inserir os arquivos de excel do seu sistema, *nesse caso, os arquivos para teste: Compras e pagamentos ambos em .CSV já estão na pasta dados que você copiou do desse repositório Github;
5) Volte a pasta janela e crie um atalho do executável janela.exe para a pasta |dados|, ele será o responsável por analisar os dados.

* Linguagem do projeto: Python 3.
* os arquivos csv na pasta dados, não são reais na verdade eles estão incompletos, eles servem apenas como exemplo, para uma melhor experiência, utilize arquivos reais com a mesma estrutura e tipo de arquivo que os apresentados nos exemplos na pasta dados.
* Microserviço: Pode ser que esse projeto não se aplique a sua necessidade, pois ele se aplica a uma demanda de um escritório que fornece os relatórios que são auditados por este script, se você não tiver esses relatórios (nos mesmos padrões dos que estão, como exemplo, na pasta dados) talvez não consiga usar o script, pois ele foi configurado para um formato específico de CSV, se esse for o seu caso, você pode criar uma estrutura que lhe posibilite usar o sistema (Uma boa ferramenta para esta função é o VBA para formatar os CSV ao seu gosto).
* Há no repositório um módulo em VBA que você pode utilizar para organizar os seus dados em CSV.
