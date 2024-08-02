import pandas as pd

def pair(file_spectra, file_univas, file_output_pareado):
    espectros = pd.read_csv(file_spectra)
    exames_univas = pd.read_excel(file_univas)
    resultado = pd.merge(exames_univas, espectros, on='Código', how='inner')
    resultado.to_excel(file_output_pareado, index=False)
    print(f"Planilha pareada com sucesso no diretório {file_output_pareado}")

if __name__ == '__main__':
    espectros = input("Digite o caminho para o arquivo com os espectros: ")
    exames_univas = input("Digite o caminho para o arquivo com os exames da univas mesclados: ")
    pareado = input("Digite o caminho para o arquivo pareado ")
    pair(espectros, exames_univas, pareado)
