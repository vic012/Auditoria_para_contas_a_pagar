Attribute VB_Name = "Módulo1"
Option Explicit
Sub Importar_dados()
'
' Importa os dados das planilhas Fechadas
'
' ----------- Planilha 1 (Compras)
'
' Abre a planilha das compras e organiza

    Dim arquivo As String
    
    ' O algorítmo solicita ao cliente o nome do arquivo
    arquivo = Application.GetOpenFilename("Arquivos Excel(*.XLS), *.XLS")
    
               
    Workbooks.Open (arquivo)

End Sub
Sub organiza_tabela_compras()
'
' organiza_tabela_compras Macro
' Organiza a tabela das compras
'
    Dim item As String
    Dim contagem As Integer
                           
    contagem = 1
'Exclui as colunas desnecessárias
    Columns("A:A").Select
    Selection.UnMerge
    Rows("1:6").Select
    Selection.Delete Shift:=xlUp
    Range("D1").Select
    Selection.Copy
    Range("C1").Select
    ActiveSheet.Paste
    Range("D1").Clear
    item = Cells(1, 1).Select
    Do While (contagem <= 6)
        If (contagem > 6) Then
            Exit Do
        End If
        If (Selection = "Data" Or Selection = "Histórico" Or Selection = "Débito" Or Selection = "Crédito" Or Selection = "Número") Then
            ActiveCell.Offset(0, 1).Select
            contagem = contagem + 1
        ElseIf (Selection = "Saldo-Exercício") Then
            ActiveSheet.Range(Cells(1, contagem), Cells(65536, contagem)).Select
            Selection.Delete Shift:=xlUp
            contagem = contagem + 1
        Else
            ActiveSheet.Range(Cells(1, contagem), Cells(65536, contagem)).Select
            Selection.Delete Shift:=xlUp
            ActiveCell.Offset(0, 0).Select
        End If

    Loop
    'Range("F2").Select
    'Selection.End(xlDown).Select
    'ActiveCell.Offset(0, -5).Select
    'Selection.End(xlUp).Select
    'Range(Selection, ActiveCell.Offset(-1, 0)).Select
    'Selection.Delete
    Columns("B:B").EntireColumn.AutoFit
    Range("B2").Select
    Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
    Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
End Sub
Sub filtro_celulas_vazias()
'
' filtro_celulas_vazias Macro
' Exclui céluas vazias e desnecessárias
'

'
    Columns("A:A").Select
    Selection.AutoFilter
    ActiveSheet.Range("$A$1:$D$65536").AutoFilter Field:=1, Criteria1:="=Conta:" _
        , Operator:=xlOr, Criteria2:="="
    Range("$A$2:$E$65536").Select
    Selection.EntireRow.Delete
    ActiveSheet.Range("$A$1:$D$65536").AutoFilter Field:=1
    Columns("B:B").Select
    Selection.NumberFormat = "0"
    Range("B2").Select
End Sub
Sub inicio_da_pagina()
'Volta ao início da página
        
    Range("A1").Select
    
End Sub
Sub preencher()
' Um laço para preencher em cada partida o número do fornecedor nas compras e pagamentos
    Dim item As String
    Dim contagem, tamanho As Integer
    
    
    item = 0
    contagem = 0
    tamanho = Cells(Rows.Count, 1).End(xlUp).Row
    Do While (contagem <= tamanho)
        If (contagem > tamanho) Then
            Exit Do
        End If
        If (Selection = 0) Then
            Selection.Value = item
            ActiveCell.Offset(1, 0).Select
            contagem = contagem + 1
        Else
            item = Selection.Value
            ActiveCell.Offset(1, 0).Select
            contagem = contagem + 1
        End If
    Loop
    Range("A1").Select
    Selection.End(xlDown).Select
    ActiveCell.Offset(1, 0).Select
    ActiveCell.Offset(0, 1).Select
    If (Selection = 0) Then
        Range("B1").Select
    Else
        ActiveSheet.Range(Selection, Selection.End(xlDown)).Delete
        Range("B1").Select
    End If
    Selection.End(xlDown).Select
    Selection.Delete
    ActiveCell.Offset(0, -1).Delete
    ActiveSheet.Buttons.Add(256, 136198.5, 150, 24.75).Select
    Selection.OnAction = "dados.xlsm!inicio_da_pagina"
    Selection.Characters.Text = "Voltar ao inicio da página!"
    Range("A1").Select
    Selection.End(xlDown).Select
End Sub
Sub executa()
    Call Importar_dados
    Call organiza_tabela_compras
    Call filtro_celulas_vazias
    Call preencher
    'Call importar_dados_pagamentos
    'Worksheets("Central de comandos").Select
End Sub
