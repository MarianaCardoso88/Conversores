import os
import chardet
from openpyxl import Workbook
import zipfile

def txt_to_excel(input_folder_path, output_folder_path):
    # Criando arquivo de log para debug
    caminho_para_o_arquivo_de_log = './logs/txt_to_excel.log'
    with open(caminho_para_o_arquivo_de_log, 'w') as arquivo_log:
        arquivo_log.write("Iniciando conversão de txt para excel\n")

    # Criando a pasta de saída se não existir
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Iterando sobre os arquivos na pasta de entrada
    for root, dirs, files in os.walk(input_folder_path):
        for file_name in files:
            input_file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(root, input_folder_path)
            output_dir_path = os.path.join(output_folder_path, relative_path)
            if not os.path.exists(output_dir_path):
                    os.makedirs(output_dir_path)
            output_file_path = os.path.join(output_dir_path, f"{os.path.splitext(file_name)[0]}.xlsx")

            # Convertendo o arquivo de texto para Excel
            convert_to_txt(input_file_path, output_file_path)

            # Carregando o conteúdo do arquivo TXT
            with open(input_file_path, 'r', encoding='utf-8') as file:
                linhas = file.readlines()

            # Criando um novo arquivo Excel e escrevendo as linhas do arquivo TXT em colunas
            workbook = Workbook()
            sheet = workbook.active

            for linha in linhas:
                # Divide a linha com base na tabulação e adiciona as partes como colunas
                colunas = linha.strip().split('\t')
                colunas = [convert_to_float(coluna) for coluna in colunas]
                sheet.append(colunas)

            # Salvando o arquivo Excel
            workbook.save(output_file_path)

            mensagem_log = "Conversão de txt para excel concluída para " + file_name + " Arquivo de saída salvo em" + output_file_path + "\n"
            # Abrindo o arquivo de log em modo de adição e adicionando a mensagem
            with open(caminho_para_o_arquivo_de_log, 'a') as arquivo_log:
                arquivo_log.write(mensagem_log)

# Dado um diretório de entrada e um diretório de saída, passa a função func em cada arquivo do diretório de entrada e salva o resultado no diretório de saída.
def process_files(input_dir, output_dir, func):
    """
    Processa todos os arquivos em uma pasta de entrada, aplica uma função a cada um
    e salva os arquivos processados na pasta de saída, mantendo a estrutura de diretórios.

    :param input_dir: Caminho para a pasta de entrada.
    :param output_dir: Caminho para a pasta de saída.
    :param func: Função a ser aplicada em cada arquivo - esta função precisa retornar true ou false.
    """

    # Criando arquivo de log para debug
    caminho_para_o_arquivo_de_log = "./logs/" + func.__name__ + '.log'
    with open(caminho_para_o_arquivo_de_log, 'w') as arquivo_log:
        arquivo_log.write(f"Iniciando {func.__name__} \n")

    # Verifica se a pasta de saída existe, senão, cria a pasta
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Percorre todos os arquivos e subdiretórios na pasta de entrada
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            # Caminho completo do arquivo de entrada
            input_file_path = os.path.join(root, file)

            # Caminho relativo do arquivo em relação à pasta de entrada
            relative_path = os.path.relpath(input_file_path, input_dir)

            # Caminho completo do arquivo de saída
            output_file_path = os.path.join(output_dir, relative_path)

            # Cria os diretórios necessários na pasta de saída
            output_file_dir = os.path.dirname(output_file_path)
            if not os.path.exists(output_file_dir):
                os.makedirs(output_file_dir)

            # Aplica a função ao arquivo de entrada
            if (func(input_file_path, output_file_path)):
                # Abrindo o arquivo de log em modo de adição e adicionando a mensagem
                with open(caminho_para_o_arquivo_de_log, 'a') as arquivo_log:
                    arquivo_log.write("Arquivo " + output_file_path + " não processado com sucesso\n")
            else:
                with open(caminho_para_o_arquivo_de_log, 'a') as arquivo_log:
                    arquivo_log.write("Arquivo " + output_file_path + " processado coretamente\n")

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

def is_valid_excel_file(file_path):
    # Verifica se o arquivo tem extensão .xlsx ou .xls
    if not file_path.endswith(('.xlsx', '.xls')):
        return False
    # Verifica se o arquivo pode ser aberto como um zip (apenas para arquivos .xlsx)
    if file_path.endswith('.xlsx'):
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                pass
        except zipfile.BadZipFile:
            return False
    return True

def verify_files(input_folder_path, func):
    """
    Executa a função fornecida em cada arquivo dentro da pasta e subpastas.
    :param input_folder_path: Caminho da pasta principal.
    :param func: Função a ser executada em cada arquivo.
    """
    # Percorre a estrutura de diretórios recursivamente
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            caminho_completo = os.path.join(root, file)
            if is_valid_excel_file(caminho_completo):
                func(caminho_completo)
            else:
                print(f"Arquivo inválido ou corrompido: {caminho_completo}")

def convert_to_float(value):
    value = value.replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return value

def convert_to_txt(input_file, output_file):
    # Detectando a codificação do arquivo
    encoding = detect_encoding(input_file)
    if encoding is None:
        encoding = 'utf-8'  # Caso a detecção de codificação não seja bem-sucedida, use UTF-8 como padrão

    # Lendo o arquivo em bytes
    with open(input_file, 'rb') as file:
        content_bytes = file.read()

    # Decodificando manualmente, ignorando erros
    content = content_bytes.decode(encoding, errors='ignore')

    # Escrevendo o conteúdo no arquivo de texto
    with open(output_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write(content)

if __name__ == "__main__":
    print(detect_encoding('/home/vini/Desktop/ExamesUnivas03_06_2024_a_14_06_2024/06/06_2_txts_tratados/03/6028212'))