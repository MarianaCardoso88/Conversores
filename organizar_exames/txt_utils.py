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

    dict_exams_venoso = {"BE": "GasometriaVenosaBE", "cHCO3": "GasometriaVenosacHCO3", "ctCO2": "GasometriaVenosactCO2", "FIO2": "GasometriaVenosaFIO2", "GLICEMIA:": "GasometriaVenosaGLICEMIA", "Hematócrito": "GasometriaVenosaHematócrito", "Lactato (ácido lático)": "GasometriaVenosaLactato", "pCO2": "GasometriaVenosapCO2", "pH": "GasometriaVenosapH", "pO2": "GasometriaVenosapO2", "sO2(c)": "GasometriaVenosasO2"}
    dict_exams_arterial = {"BE": "GasometriaArterialBE", "cHCO3": "GasometriaArterialcHCO3", "ctCO2": "GasometriaArterialctCO2", "FIO2": "GasometriaArterialFIO2", "GLICEMIA:": "GasometriaArterialGLICEMIA", "Hematócrito": "GasometriaArterialHematócrito", "Lactato (ácido lático)": "GasometriaArterialLactato", "pCO2": "GasometriaArterialpCO2", "pH": "GasometriaArterialpH", "pO2": "GasometriaArterialpO2", "sO2(c)": "GasometriaArterialsO2"}

    with open(input_file, 'r', encoding='ISO-8859-1') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', encoding='UTF-8') as outfile:
        for line in lines:
            if keyword in line:
                print("teste")


if __name__ == '__main__':
    input_file_txt = input("Digite o caminho raiz dos arquivos txt organizados por dia: ")
    output_txt_sem_linhas_inuteis = input("Digite o caminho para o txt sem linhas inúteis: ")
    file_processing.process_files(input_file_txt, output_txt_sem_linhas_inuteis, remove_lines_with_keywords)
    print("Linhas removidas com sucesso!")