import pandas as pd
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as infile:
        raw_data = infile.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    return encoding
        

def pair(file_spectra, file_univas, file_output_pareado):
    espectros = pd.read_csv(file_spectra)
    exames_univas = pd.read_excel(file_univas)

    espectros["Código"] = espectros["Código"].astype(str)
    exames_univas["Código"] = exames_univas["Código"].astype(str)

    resultado = pd.merge(exames_univas, espectros, on='Código', how='inner')

    resultado["Código"] = resultado["Código"].astype(int)
    resultado.to_excel(file_output_pareado, index=False)
    print(f"Exames pareados com sucesso no diretório {file_output_pareado}")

if __name__ == '__main__':
    espectros = "/home/vini/Desktop/pareamento/pareamento-09-2023/espectros_2023_setembro.csv"
    exames_univas = "/home/vini/Desktop/pareamento/pareamento-09-2023/exames_univas.xlsx"
    pareado = "/home/vini/Desktop/pareamento/pareamento-09-2023/pareados_setembro.xlsx"
    pair(espectros, exames_univas, pareado)

    # print(detect_encoding(espectros))
