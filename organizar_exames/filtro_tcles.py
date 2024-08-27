import pandas as pd

def tcles_filter(dados_pareados, tabela_prescricao_atendimento, mes, data_set):
    pareados = pd.read_excel(dados_pareados)
    prescricao_atendimento = pd.read_excel(tabela_prescricao_atendimento, sheet_name=mes)

    df_filtrado = pareados[pareados['Código'].isin(prescricao_atendimento['Prescrição'])]

    df_filtrado.to_csv(data_set, index=False, decimal=',')


if __name__ == '__main__':
    dados_pareados = "/home/vini/Desktop/pareamento/pareamento-10-2023/pareados.xlsx"
    tabela_prescricao_atendimento = "/home/vini/Desktop/pareamento/pareamento-10-2023/tabela_prescricao_atendimento.xlsx"
    mes = "Outubro"
    data_set = "/home/vini/Desktop/pareamento/pareamento-10-2023/data_set.csv"
    tcles_filter(dados_pareados, tabela_prescricao_atendimento, mes, data_set)
    
