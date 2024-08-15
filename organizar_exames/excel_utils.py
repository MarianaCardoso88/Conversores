import os
import pandas as pd
import file_processing

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


# A função transpõe apenas arquivos com uma prescrição e armazena em log os arquivos que possuem mais de uma prescrição
def transpose_exam_one_prescription(input_file_path, output_file_path):
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

def organize_exams_one_prescription(input_file, output_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)
    
    # Salvando o cabeçalho da terceira coluna (Código do exame)
    third_col_header = df.columns[2]

    # Atribuindo o cabeçalhos da terceira coluna como valor na terceira coluna e primeira linha
    df.iat[0, 2] = pd.to_numeric(third_col_header, errors='coerce')

    # Acessa os nomes atuais das colunas
    nomes_atuais = df.columns.tolist()

    # Substitui os nomes das primeiras 3 colunas
    nomes_atuais[:3] = ['Data', 'Atendimento', 'Código']

    # Atribui a lista modificada de volta a df.columns
    df.columns = nomes_atuais

    # Pegando o nome do arquivo sem a extensão
    nome_arquivo = os.path.splitext(os.path.basename(input_file))[0]

    # Adicionando o nome do arquivo na coluna 'Atendimento'
    df['Atendimento'] = nome_arquivo

    # Remover espaços dos cabeçalhos
    df.columns = [col.replace(' ', '') for col in df.columns]

    # Salvando o DataFrame modificado
    df.to_excel(output_file, index=False)

def organize_exams(input_file, output_file):
    # Lendo arquivo excel
    df = pd.read_excel(input_file)
    number_of_exams = count_exams(input_file)

    # Contagem de arquivos com mais de uma prescrição para logs
    if (number_of_exams == 0 or number_of_exams > 1):
        # Adicionando o caminho do arquivo ao arquivo de log
        with open("./logs/arquivos_com_mais_de_um_exame.log", 'a') as arquivo_log:
            arquivo_log.write(input_file + "\n")

    # Armazenando headers em uma lista
    headers = df.columns.values

    # Data que não está alinhada no excel
    data_presc_last = headers[5]

    # Armazena os índices das prescrições em uma lista
    indices_presc = df.loc[df.iloc[:, 0].apply(type) == int].index

    # Armazena as prescrições em uma lista
    prescs = list(df.loc[indices_presc, 'Exame'])

    # Armazena as datas que estão alinhadas em uma lista
    datas =  list(df.loc[indices_presc, 'Unidade'])

    # Armazena as datas em uma lista
    datas.pop(-1)

    datas = [data_presc_last] + datas

    # Armazena na variável o nome do arquivo
    nome_arquivo = os.path.splitext(os.path.basename(input_file))[0]

    # Criando lista para adicionar o atendimento em cada exame
    atends = []
    for i in range(len(prescs)):
        atends.append(int(nome_arquivo))

    # Lista das colunas a serem removidas
    colunas_para_remover = ['Unidade', 'Referência', 'Material', 'Método']
    # Removendo as colunas especificadas
    df_modificado = df.drop(columns=colunas_para_remover, errors='ignore')
    

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

    # Salvando o DataFrame modificado em um novo arquivo Excel
    df_transposto.to_excel(output_file, index=False)

def verify_type(input_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file)

    # Verificando o tipo de cada coluna
    print(df.dtypes)

def merge_excel_files(root_directory, output_file):
    # Lista para armazenar os dataframes
    dataframes = []
    
    # Percorrer todos os arquivos e subpastas na pasta raiz
    for subdir, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(subdir, file)
                # Ler o arquivo Excel e adicionar ao dataframe
                df = pd.read_excel(file_path)
                dataframes.append(df)
    
    # Concatenar todos os dataframes
    merged_df = pd.concat(dataframes, ignore_index=True)
    
    # Salvar o dataframe combinado em um novo arquivo Excel
    merged_df.to_excel(output_file, index=False)
    
    return output_file

def verify_numbers_in_headers(input_file):
    # Lendo o arquivo Excel
    df = pd.read_excel(input_file, engine='openpyxl')

    # Verificando se há números nas colunas
    for col in df.columns:
        if ".1" in col:
            print(f"O arquivo {input_file} possui pelo menos uma coluna {col} com os caracteres '.1' no cabeçalho.")
            continue

if __name__ == '__main__':
    # Mesclando os exames em um único excel
    # input_path_arquivo_excel = "./5795083.xlsx"
    # output_excel_mesclado = "./5795083-MESCLADO.xlsx"
    # merge_excel_files(input_path_arquivo_excel, output_excel_mesclado)
    # print("Arquivos mesclados com sucesso!")

    # Verificando cabeçalhos
    input_path_diretorio_excel = input("Digite o caminho raiz dos arquivos excel organizados: ")
    file_processing.verify_files(input_path_diretorio_excel, verify_numbers_in_headers)
    print("Verificação concluída com sucesso")

    # Organizando exames
    # input_arquivo_excel = "5795083.xlsx"
    # output_excel_organizado = "5795083-organizado.xlsx"
    # organize_exams(input_arquivo_excel, output_excel_organizado)
    # print("Arquivo organizado")