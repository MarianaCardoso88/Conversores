import os
import file_processing
import excel_utils
import txt_utils
import pair

def clean_logs():
    directory_path = "./logs"
    # Listando todos os arquivos no diretório
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Verificando se é um arquivo (e não um diretório)
        if os.path.isfile(file_path):
            os.remove(file_path)  # Apaga o arquivo
    print(f"Arquivo de logs de operações antigas apagados")


if __name__ == "__main__":
    clean_logs()

    # Criar script para logar arquivos com mais de um exame antes de passar pro excel
    # Criar script para identificar arquivos com biomarcadores com mesmos nomes, mas obtidos de formas diferentes

    # Solicita o caminho raiz das pastas de entrada
    input_path_raiz_dados = input("Digite o caminho raiz que possue a pasta dos TXTs organizados por dia: ")
    
    # Converte os arquivos TXT da ISO-8859-1 para UTF-8
    print("Convertendo TXTs ISO-8859-1 para UTF-8...")
    input_path_dados_brutos = input_path_raiz_dados + "/0.brutos"
    output_txt_utf8 = input_path_raiz_dados + "/1.TXTs_utf-8"
    file_processing.process_files(input_path_dados_brutos, output_txt_utf8, txt_utils.convert_to_utf8)
    print("TXTs convertidos para UTF-8")

    # Tratar Gasometrias e tipo de sangue venoso e arterial
    print("Tratando Gasometrias...")
    output_gasometrias_tratadas = input_path_raiz_dados + "/2.TXTs_gasometrias_tratadas"
    file_processing.process_files(output_txt_utf8, output_gasometrias_tratadas, txt_utils.changing_gasometrias_exams_strings)
    print("Gasometrias tratadas")

    # Remove linhas baseadas em keywords dos arquivos em txt
    print("Removendo linhas baseadas em keywords")
    output_txt_sem_linhas_inuteis = input_path_raiz_dados + "/3.TXTs_sem_linhas_inuteis"
    file_processing.process_files(output_gasometrias_tratadas, output_txt_sem_linhas_inuteis, txt_utils.remove_lines_with_keywords)
    print("Linhas removidas")

    # Converte arquivos de TXT para Excel
    print("Convertendo TXTs para xlsx...")
    output_path_arquivos_excel = input_path_raiz_dados + "/4.excel"
    file_processing.txt_to_excel(output_txt_sem_linhas_inuteis, output_path_arquivos_excel)
    print("Conversão de TXT para Excel concluída.")

    # Organizando os códigos dos exames
    print("Organizando arquivos xlsx...")
    output_path_arquivos_organizados = input_path_raiz_dados + "/5.excel_organizados"
    file_processing.process_files(output_path_arquivos_excel, output_path_arquivos_organizados, excel_utils.organize_exams)
    print("Organização dos códigos dos exames concluída.")

    # Mesclar arquivos xlsx
    while True:
        mesclar = input("deseja mesclar todos os arquivos excel em um só arquivo? sim/não: ").strip().lower()
        if mesclar == "sim":
            excel_utils.merge_excel_files(output_path_arquivos_organizados,input_path_raiz_dados + "/exames_univas.xlsx")
            print("Arquivos mesclados")
            break
        elif mesclar == "não":
            print("arquivos não mesclados")
            break
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")

    # Parear arquivos univas progenos
    while True:
        parear = input("deseja parear os arquivos da univas mesclados com os espectros? sim/não: ").strip().lower()
        if parear == "sim":
            input_espectros = input("Insira o caminho para o arquivo csv contendo os espectros do Progenos: ")
            pair.pair(input_path_raiz_dados + "/exames_univas.xlsx", input_espectros)
            print("Exames pareados")
            break
        elif parear == "não":
            print("exames não pareados")
            break
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")
        
