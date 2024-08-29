import pandas as pd

def tcles_filter(dados_pareados, tabela_prescricao_atendimento, data_set):
    pareados = pd.read_excel(dados_pareados)
    prescricao_atendimento = pd.read_excel(tabela_prescricao_atendimento)

    df_filtrado = pareados[pareados['Código'].isin(prescricao_atendimento['Prescrição'])]

    df_filtrado.to_excel(data_set, index=False)

def tcles_reexportar(dados_pareados, tabela_prescricao_atendimento):
    pareados = pd.read_excel(dados_pareados)
    prescricao_atendimento = pd.read_excel(tabela_prescricao_atendimento)

    diferenca = prescricao_atendimento[~prescricao_atendimento['Prescrição'].isin(pareados['Código'])]
    diferenca.to_excel("tcles_sem_exames.xlsx", index=False)


if __name__ == '__main__':
    dados_pareados = "/home/vini/Desktop/pareamento/pareamento-11-2023/pareados.xlsx"
    tabela_prescricao_atendimento = "/home/vini/Desktop/pareamento/pareamento-11-2023/tcles_novembro.xlsx"
    data_set = "/home/vini/Desktop/pareamento/pareamento-11-2023/data_set.xlsx"
    tcles_filter(dados_pareados, tabela_prescricao_atendimento, data_set)
    print("Exames filtrados")

    tcles_reexportar(dados_pareados, tabela_prescricao_atendimento)
    print("Exames para reexportar")


    
