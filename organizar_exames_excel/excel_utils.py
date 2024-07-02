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
    numeros_inteiros = primeira_coluna.apply(lambda x: isinstance(x, int) or (isinstance(x, str) and x.isdigit()))

    # Contando quantos são inteiros
    return numeros_inteiros.sum()

# A função transpõe apenas arquivos com um exame e armazena em log os arquivos que possuem mais de um exame
def transpose_exam(input_file_path, output_file_path):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file_path)
    number_of_exams = count_exams(input_file_path)

    # Condição para caso o exame não possua código ou possua mais que um código
    if (number_of_exams == 0 or number_of_exams > 1):
        # Adicionando o caminho do arquivo ao arquivo de log
        with open("./logs/arquivos_com_mais_de_um_exame.log", 'a') as arquivo_log:
            arquivo_log.write(input_file_path + "\n")
        
    if (number_of_exams == 1):
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

def organize_exams_code(input_file, output_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)
    
    # Salvando o cabeçalho da terceira coluna (Código do exame)
    third_col_header = df.columns[2]

    # Atribuindo o cabeçalhos da terceira coluna como valor na terceira coluna, primeira linha
    df.iat[0, 2] = pd.to_numeric(third_col_header, errors='coerce')

    # Acessa os nomes atuais das colunas
    nomes_atuais = df.columns.tolist()

    # Substitui os nomes das primeiras 3 colunas
    nomes_atuais[:3] = ['Data', 'Atendimento', 'Código']

    # Atribui a lista modificada de volta a df.columns
    df.columns = nomes_atuais

    # Salvando o DataFrame modificado
    df.to_excel(output_file, index=False)

def verify_type(input_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)

    # Verificando o tipo de cada coluna
    print(df.dtypes)
    

if __name__ == '__main__':
    input_file = '/home/vini/Desktop/novosExamesUnivasOrganizados/2024/06_teste_main_transpostas/03/6028212.xlsx'
    output_file = '/home/vini/Desktop/novosExamesUnivasOrganizados/2024/6073087_arrumado.xlsx'
    organize_exams_code(input_file, output_file)
    # print(verify_type(input_file))