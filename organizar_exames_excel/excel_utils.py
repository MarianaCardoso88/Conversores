import pandas as pd

def remove_colunas_arquivo(input_file_path, output_file_path):
    # Lista das colunas a serem removidas
    colunas_para_remover = ['Unidade', 'Referência', 'Material', 'Método']

    # Lendo o arquivo Excel
    df = pd.read_excel(input_file_path)

    # Removendo as colunas especificadas
    df_modificado = df.drop(columns=colunas_para_remover)

    # Salvando o DataFrame modificado em um novo arquivo Excel
    df_modificado.to_excel(output_file_path, index=False)

def count_exams(file_path):
    # Lendo o arquivo Excel
    df = pd.read_excel(file_path)

    # Acessando a primeira coluna
    primeira_coluna = df.iloc[:, 0]

    # Verificando quais elementos são inteiros no formato string
    numeros_inteiros = primeira_coluna.apply(lambda x: x.isdigit() if isinstance(x, str) else False)

    # Contando quantos são inteiros
    return numeros_inteiros.sum()

def transpose_exam(input_file_path, output_file_path):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file_path)

    # Transpondo o DataFrame
    df_transposto = df.T

    # Definir o cabeçalho do DataFrame transposto para ser igual à primeira linha do DataFrame original
    df_transposto.columns = df_transposto.iloc[0]

    # Remover a primeira linha do DataFrame transposto
    df_transposto = df_transposto[1:]

    # Salvando o DataFrame modificado em um novo arquivo Excel
    df_transposto.to_excel(output_file_path, index=False)

def organize_exams_code(input_file, output_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)
    number_of_exams = count_exams(input_file)

    if (number_of_exams == 0 or number_of_exams > 1):
        # Adicionando o caminho do arquivo ao arquivo de log
        with open("./logs/arquivos_com_mais_de_um_exame.log", 'a') as arquivo_log:
            arquivo_log.write(input_file + "\n")
        
    if (number_of_exams == 1):
        # Converter a segunda coluna para o tipo 'object'
        df.iloc[:, 1] = df.iloc[:, 1].astype('object')
        
        # Pegar o código
        valor = df.iloc[1, 0]

        # Colocar esse código na quarta linha e segunda coluna
        df.iloc[3, 1] = valor

        # Apagar horários e linha que estava o código
        # Apagar as duas primeiras linhas de uma vez, criando um novo DataFrame modificado
        df_modificado = df.drop(df.index[:2])

        # Salvar o arquivo Excel
        df_modificado.to_excel(output_file, index=False)

if __name__ == '__main__':
    input_file = '/home/vini/Desktop/novosExamesUnivasOrganizados/2024/06_main_excel/03/6028212.xlsx'
    output_file = '/home/vini/Desktop/novosExamesUnivasOrganizados/2024/6028212.xlsx'
    transpose_exam(input_file, output_file)