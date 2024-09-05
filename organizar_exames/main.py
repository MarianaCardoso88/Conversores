import os
import file_processing
import excel_utils
import txt_utils
import pair
import tcles_filters

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

    # Solicita o caminho raiz das pastas de entrada
    input_path_raiz_dados = input("Digite o caminho raiz que possue a pasta dos TXTs organizados por dia: ")
    
    # Converte os arquivos TXT da ISO-8859-1 para UTF-8
    print("Convertendo TXTs ISO-8859-1 para UTF-8...")
    input_path_dados_brutos = input_path_raiz_dados + "/0.brutos"
    output_txt_utf8 = input_path_raiz_dados + "/1.TXTs_utf-8"
    file_processing.process_files(input_path_dados_brutos, output_txt_utf8, txt_utils.convert_to_utf8_if_needed)
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
    
    # Encontrar arquivos com marcadores duplicados e pausar processamento para a edição manual
    print("Encontrando arquivos com marcadores duplicados")
    file_processing.verify_files(output_path_arquivos_excel, excel_utils.verify_duplicated_markers)

    # Organizando os códigos dos exames
    print("Organizando arquivos xlsx...")
    output_path_arquivos_organizados = input_path_raiz_dados + "/5.excel_organizados"
    file_processing.process_files(output_path_arquivos_excel, output_path_arquivos_organizados, excel_utils.organize_exams)
    print("Organização dos códigos dos exames concluída.")

    # Mesclar arquivos xlsx
    while True:
        mesclar = input("Deseja mesclar todos os arquivos excel em um só arquivo? sim/não: ").strip().lower()
        if mesclar == "sim":
            exames_mesclados = input_path_raiz_dados + "/exames_univas.xlsx"
            excel_utils.merge_excel_files(output_path_arquivos_organizados, exames_mesclados)
            
            # Substituir HGM, CHGM, VGM por HCM, CHCM, VCM
            excel_utils.rename_columns(exames_mesclados)

            # Removendo cabeçalhos não validados
            # OBS.: a função NÃO filtra corretamente os marcadores que vêm duplicados nos arquivos
            excel_utils.remove_unvalidated_headers(exames_mesclados)

            print("Arquivos mesclados")
            break
        elif mesclar == "não":
            print("Arquivos não mesclados")
            break
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")

    # Parear arquivos univas progenos
    while True:
        parear = input("Deseja parear os exames da univas com os espectros? sim/não: ").strip().lower()
        if parear == "sim":
            input_espectros = input("Insira o caminho para o arquivo csv contendo os espectros do Progenos: ")
            pareados = input_path_raiz_dados + "/pareados.xlsx"
            pair.pair(input_espectros, input_path_raiz_dados + "/exames_univas.xlsx", pareados)
            print("Exames pareados")
            break
        elif parear == "não":
            print("Exames não pareados")
            break
        else:
            print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")
        
    # Filtrar pareados com TCLEs
    if (parear == "sim"):
        while True:
            filtrar = input("Deseja filtrar os exames pareados baseado nos TCLEs? sim/não: ").strip().lower()
            if filtrar == "sim":
                input_tecles = input("Insira o caminho para o arquivo xlsx contendo os TCLEs ")
                tcles_filters.filter(input_path_raiz_dados + "/pareados.xlsx", input_tecles, input_path_raiz_dados + "/data_set.xlsx")
                print("Exames filtrados com base nos TCLEs salvo em " + input_path_raiz_dados + "/data_set.xlsx")
                tcles_filters.reexport(input_path_raiz_dados + "/pareados.xlsx", input_tecles, input_path_raiz_dados + "/tcles_sem_exames.xlsx")
                print("Diferença dos TCLEs com data_set salvo em " + input_path_raiz_dados + "/tcles_sem_exames.xlsx")
                break
            elif filtrar == "não":
                print("Dados não filtrados")
                break
            else:
                print("Resposta inválida. Por favor, digite 'sim' ou 'não'.")