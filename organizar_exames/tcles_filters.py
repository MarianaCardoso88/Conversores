"""
Este módulo contém funções utilitárias que filtram dados 
pareados de duas formas.


Funções

- filter: recebe uma planilha com dados pareados e filtra
baseado na planilha de tcles recebidos e retorna uma data_set.
    :param dados_pareados: caminho arquivo de entrada com os
    dados pareados;
    :param tabela_prescricao_atendimento: caminho arquivo de 
    entrada para filtro com as prescrições dos TCLEs;
    :param data_set: arquivo de output com as linhas filtradas

- reexport: recebe uma planilha com dados pareados e faz a diferença
baseado na planilha de tcles recebidos, ou seja, cria um arquivo com
os TCLEs que não possuem exames.
    :param dados_pareados: caminho arquivo de entrada com os
    dados pareados;
    :param tabela_prescricao_atendimento: caminho arquivo de 
    entrada para filtro com as prescrições dos TCLEs;
"""

import pandas as pd

def filter(dados_pareados, tabela_prescricao_atendimento, data_set):
    pareados = pd.read_excel(dados_pareados)
    prescricao_atendimento = pd.read_excel(tabela_prescricao_atendimento)

    df_filtrado = pareados[pareados['Código'].isin(prescricao_atendimento['Prescrição'])]

    df_filtrado.to_excel(data_set, index=False)

def reexport(dados_pareados, tabela_prescricao_atendimento):
    pareados = pd.read_excel(dados_pareados)
    prescricao_atendimento = pd.read_excel(tabela_prescricao_atendimento)

    diferenca = prescricao_atendimento[~prescricao_atendimento['Prescrição'].isin(pareados['Código'])]
    diferenca.to_excel("tcles_sem_exames.xlsx", index=False)


if __name__ == '__main__':
    dados_pareados = "/home/vini/Desktop/pareamento/pareamento-11-2023/pareados.xlsx"
    tabela_prescricao_atendimento = "/home/vini/Desktop/pareamento/pareamento-11-2023/tcles_novembro.xlsx"
    data_set = "/home/vini/Desktop/pareamento/pareamento-11-2023/data_set.xlsx"
    filter(dados_pareados, tabela_prescricao_atendimento, data_set)
    print("Exames filtrados")

    reexport(dados_pareados, tabela_prescricao_atendimento)
    print("Exames para reexportar")


    
