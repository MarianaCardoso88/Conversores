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

def organize_exams(input_file, output_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)

    # Remover espaços dos cabeçalhos
    df.columns = [col.replace(' ', '') for col in df.columns]

    # Exclui a primeira coluna
    df = df.iloc[:, 1:]

    # Salvando o DataFrame modificado
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    # Transpondo exames
    input_caminho_excel_tratados = input("Digite o caminho do da pasta contendo o excel: ")
    output_caminho_excel_transpostos = input("Digite o caminho da pasta de saída para os arquivos Excel transpostos: ")
    file_processing.process_files(input_caminho_excel_tratados, output_caminho_excel_transpostos, transpose_exam)
    print("Transposição dos exames concluída.")

    # Organizando exames (removendo linhas do cabeçalho)
    input_camino_excel_transpostos = output_caminho_excel_transpostos
    output_caminho_excel_organizados = input("igite o caminho da pasta de saída para os arquivos Excel organizados: ")
    file_processing.process_files(input_camino_excel_transpostos, output_caminho_excel_organizados, organize_exams)
    print("Organização dos exames concluída.")