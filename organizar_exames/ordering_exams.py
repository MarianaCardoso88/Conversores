import pandas as pd

def ordering_exams(data):
    data['registryDate'] = pd.to_datetime(data['registryDate'], format='%d/%m/%Y - %H:%M:%S')
    data.sort_values('registryDate', inplace=True)
    return data

def verify_extension(file_name):
    if file_name.endswith('.csv'):
        return pd.read_csv(file_name)
    elif file_name.endswith('.xlsx'):
        return pd.read_excel(file_name)
    else:
        raise ValueError('Arquivo não suportado')


if __name__ == '__main__':
    input_arquivo_desordenado = input("Digite o caminho do arquivo a ser ordenado por data: ")
    output_arquivo_ordenado = input("Digite o caminho de saída do arquivo ordenado: ")
    data = verify_extension(input_arquivo_desordenado)
    dados_organizados = ordering_exams(data)
    dados_organizados.to_csv(output_arquivo_ordenado, index=False)
    print (f'Arquivo {output_arquivo_ordenado} ordenado e salvo com sucesso')