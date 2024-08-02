import pandas as pd
import os
import openpyxl
import file_processing

# A função transpõe apenas arquivos com um exame e armazena em log os arquivos que possuem mais de um exame
def transpose_exam(input_file_path, output_file_path):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file_path)

    # Transpondo o DataFrame
    df_transposto = df.T

    # Resetando o índice para transformar o índice em uma coluna regular
    df_transposto.reset_index(inplace=True)

    # Definir o cabeçalho do DataFrame transposto para ser igual à primeira linha do DataFrame original
    df_transposto.columns = df_transposto.iloc[0]

    # Remover a primeira linha do DataFrame transposto
    df_transposto = df_transposto[1:]

    # Salvando o DataFrame modificado em um novo arquivo Excel
    df_transposto.to_excel(output_file_path, index=False)

def remove_header_spaces(input_file, output_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)

    # Remover espaços dos cabeçalhos
    df.columns = [col.replace(' ', '') for col in df.columns]

    # Exclui a primeira coluna
    df = df.iloc[:, 1:]

    # Salvando o DataFrame modificado
    df.to_excel(output_file, index=False)

def organize_exams(input_file, output_file):
    # Lendo arquivo excel
    df = pd.read_excel(input_file)

    # Armazenando headers em uma lista
    headers = df.columns.values

    # Data que não está alinhada no excel
    data_presc_1 = headers[5]

    # Armazena os índices das prescrições em uma lista
    indices_presc = df.loc[df.iloc[:, 0].apply(type) == int].index

    # Armazena as prescrições em uma lista
    prescs = list(df.loc[indices_presc, 'Exame'])

    # Armazena as datas que estão alinhadas em uma lista
    datas =  list(df.loc[indices_presc, 'Unidade'])

    # Armazena as datas em uma lista
    datas.pop(-1)
    datas.append(data_presc_1)

    # Armazena na variável o nome do arquivo
    nome_arquivo = os.path.splitext(os.path.basename(input_file))[0]

    # Criando lista para adicionar o atendimento em cada exame
    atends = []
    for i in range(len(prescs)):
        atends.append(int(nome_arquivo))

    # Lista das colunas a serem removidas
    colunas_para_remover = ['Unidade', 'Referência', 'Material', 'Método']
    # Removendo as colunas especificadas
    df_modificado = df.drop(columns=colunas_para_remover)
    

    # Criando linhas com prescrições, atendimentos e datas organizados
    novas_linhas = pd.DataFrame({
        'Exame': [0]
    })
    novas_linhas = pd.concat([novas_linhas, pd.DataFrame([datas])], ignore_index=True)
    novas_linhas = pd.concat([novas_linhas, pd.DataFrame([atends])], ignore_index=True)
    novas_linhas = pd.concat([novas_linhas, pd.DataFrame([prescs])], ignore_index=True)


    # Dividindo o DataFrame original
    parte2 = df_modificado.iloc[indices_presc[-1] + 1:, :]
    parte2.columns = range(parte2.shape[1])

    # Alterando o cabeçalho para não ter problema de paridade
    novas_linhas.columns = range(novas_linhas.shape[1])
    df_organizado = pd.concat([novas_linhas, parte2], ignore_index=True)
    df_transposto = df_organizado.T

    # Organizando cabeçalho
    df_transposto.columns = df_transposto.iloc[0]
    df_transposto = df_transposto[1:]
    df_transposto = df_transposto.drop(df_transposto.columns[0], axis=1)
    df_transposto.columns = ['Data', 'Atendimento', 'Prescrição'] + list(df_transposto.columns[3:])
    df_transposto.columns = [col.replace(' ', '') for col in df_transposto.columns]
    print(df_transposto)

    # Salvando o DataFrame modificado em um novo arquivo Excel
    df_transposto.to_excel(output_file, index=False)


if __name__ == "__main__":
    # # Transpondo exames
    # input_caminho_excel_tratados = input("Digite o caminho do da pasta contendo o excel: ")
    # output_caminho_excel_transpostos = input("Digite o caminho da pasta de saída para os arquivos Excel transpostos: ")
    # file_processing.process_files(input_caminho_excel_tratados, output_caminho_excel_transpostos, transpose_exam)
    # print("Transposição dos exames concluída.")

    # # Organizando exames (removendo linhas do cabeçalho)
    # input_camino_excel_transpostos = output_caminho_excel_transpostos
    # output_caminho_excel_organizados = input("igite o caminho da pasta de saída para os arquivos Excel organizados: ")
    # file_processing.process_files(input_camino_excel_transpostos, output_caminho_excel_organizados, remove_header_spaces)
    # print("Organização dos exames concluída.")
    input_caminho_excel = "/home/vini/Desktop/578188.xlsx"
    output_excel = "/home/vini/Desktop/578188-tratado.xlsx"
    organize_exams(input_caminho_excel, output_excel)