import file_processing

def remove_lines_with_keywords(input_file, output_file):
    keywords = ['Globulinas', 'urina', 'fezes', 'Urina', 'Fezes', 'URINA', 'FEZES', 'BIOQUÍMICA', 'HEMATOLOGIA', 'UROANÁLISE', 'MICROBIOLOGIA', 'Antibiograma', 'Pesquisa de BAAR', 'Bacterioscopia', 'Cultura', 'Hemocultura', 'HERMES PARDINI', 'Tacrolimus', 'Brucelose', 'Citomegalovirus', 'Hepatite', 'HIV', 'HTLV', 'Trypanosoma', 'IMUNOLOGIA', 'VDRL', 'ABO-RhD', 'Fator Rh', 'Pesquisa de D fraco', '%', 'LAB. APOIO DB', 'Relação TTPA/Controle', 'Glicemia Média Estimada', 'HEMODIÁLISE', 'PARASITOLOGIA']
    with open(input_file, 'r', encoding='ISO-8859-1') as infile:
        lines = infile.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if not any(keyword in line for keyword in keywords):
                outfile.write(line)
                
def convert_to_utf8(input_file, output_file):
    with open(input_file, 'r', encoding='ISO-8859-1') as infile:
        content = infile.read()

    with open(output_file, 'w', encoding='UTF-8') as outfile:
        outfile.write(content)

def changing_gasometrias_exams_strings(input_file, output_file):
    keyword = 'GASOMETRIAS'

    dicts_keys = ['BE', 'cHCO3', 'ctCO2', 'FIO2', 'GLICEMIA:', 'Hematócrito', 'Lactato (ácido lático)', 'pCO2', 'pH', 'pO2', 'sO2(c)']
    dict_exams_venoso = {"BE": "GasometriaVenosaBE", "cHCO3": "GasometriaVenosacHCO3", "ctCO2": "GasometriaVenosactCO2", "FIO2": "GasometriaVenosaFIO2", "GLICEMIA:": "GasometriaVenosaGLICEMIA", "Hematócrito": "GasometriaVenosaHematócrito", "Lactato (ácido lático)": "GasometriaVenosaLactato", "pCO2": "GasometriaVenosapCO2", "pH": "GasometriaVenosapH", "pO2": "GasometriaVenosapO2", "sO2(c)": "GasometriaVenosasO2"}
    dict_exams_arterial = {"BE": "GasometriaArterialBE", "cHCO3": "GasometriaArterialcHCO3", "ctCO2": "GasometriaArterialctCO2", "FIO2": "GasometriaArterialFIO2", "GLICEMIA:": "GasometriaArterialGLICEMIA", "Hematócrito": "GasometriaArterialHematócrito", "Lactato (ácido lático)": "GasometriaArterialLactato", "pCO2": "GasometriaArterialpCO2", "pH": "GasometriaArterialpH", "pO2": "GasometriaArterialpO2", "sO2(c)": "GasometriaArterialsO2"}

    with open(input_file, 'r', encoding='ISO-8859-1') as infile:
        lines = infile.readlines()

    # Itera sobre cada linha do arquivo
    for i in range(len(lines)):
        # Verifica se existe a linha escrito "GASOMETRIAS"
        if keyword in lines[i]:
            # pula a linha que contém a keyword
            i += 1
            # Itera sobre o restante das linhas do arquivo
            for k in range(i, len(lines)):
                # Condição para não alterar linhas depois das GASOMETRIAS
                if (lines[k][0] == ' ') and (lines[k][1] == ' ') and (lines[k][2] == ' ') and (lines[k][3] == ' '):
                    # Itera sobre as chaves dos dois dicionários que são iguais
                    for j in range(len(dicts_keys)):
                        if (dicts_keys[j] in lines[k]) and ('Venoso' in lines[k]):
                            # Substituindo pela string correta
                            lines[k].replace(dicts_keys[j], dict_exams_venoso[j])
                            print('---- Venoso: ' + lines[k])
                        elif (dicts_keys[j] in lines[k]) and ('Arterial' in lines[k]):
                            # Substituir pela string correta
                            lines[k].replace(dicts_keys[j], dict_exams_arterial[j])
                            print('---- Arterial: ' + lines[k])
                        # Faltou escrever no arquivo
                else:
                    break
                i = k
        # else:
            # Faltou escrever no arquivo as linhas que não fazem parte das GASOMETRIAS
            

    # with open(output_file, 'w', encoding='UTF-8') as outfile:
    #     for line in lines:
    #         if keyword in line:
    #             print("teste")


if __name__ == '__main__':
    # input_file_txt = input("Digite o caminho raiz dos arquivos txt organizados por dia: ")
    # output_txt_sem_linhas_inuteis = input("Digite o caminho para o txt sem linhas inúteis: ")
    # file_processing.process_files(input_file_txt, output_txt_sem_linhas_inuteis, remove_lines_with_keywords)
    # print("Linhas removidas com sucesso!")]
    input_file_txt = "./7516347"
    output_file_txt = "./7516347_tratado"
    changing_gasometrias_exams_strings(input_file_txt, output_file_txt)
    print('finalizado')