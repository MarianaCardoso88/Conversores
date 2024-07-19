import pandas as pd

def pair(data_spectra, data_univas):
    univas_header = list(data_univas.columns)
    spectra_headers = list(data_spectra.columns)
    paired_headers = univas_header + ['Espectros'] + spectra_headers
    print(paired_headers)
    data_paired = pd.DataFrame(columns = paired_headers)

    # for index_univas in range(0, len(data_univas)):
    #     for index_spec in range(0, len(data_spectra)):
    #         if data_univas.iloc[index_univas, 2] == data_spectra.iloc[index_spec, 1]:
    #             print(data_univas.iloc[index_univas, 2])

    return data_paired

if __name__ == '__main__':
    input_arquivo_spectras = input("Digite o caminho do arquivo com os espectros: ")
    input_arquivo_univas = input("Digite o caminho do arquivo com os dados da univas: ")
    output_arquivo_pareado = input("Digite o caminho de saída do arquivo pareado: ")
    data_spectras = pd.read_csv(input_arquivo_spectras)
    data_univas = pd.read_excel(input_arquivo_univas)
    dados_pareados = pair(data_spectras, data_univas)
    dados_pareados.to_csv(output_arquivo_pareado, index=False)
    print (f'Arquivo {output_arquivo_pareado} pareado e salvo com sucesso')