import file_processing

def remove_lines_with_keywords(input_file, output_file):
    keywords = ['Globulinas', 'urina', 'fezes', 'Urina', 'Fezes', 'URINA', 'FEZES', 'BIOQUÍMICA', 'HEMATOLOGIA', 'UROANÁLISE', 'MICROBIOLOGIA', 'Antibiograma', 'Pesquisa de BAAR', 'Bacterioscopia', 'Cultura', 'Hemocultura', 'HERMES PARDINI', 'Tacrolimus', 'Brucelose', 'Citomegalovirus', 'Hepatite', 'HIV', 'HTLV', 'Trypanosoma', 'IMUNOLOGIA', 'VDRL', 'ABO-RhD', 'Fator Rh', 'Pesquisa de D fraco', '%', 'HEMODIÁLISE', 'LAB. APOIO DB', 'Relação TTPA/Controle', 'Glicemia Média Estimada', 'HEMODIÁLISE', 'PARASITOLOGIA']
    with open(input_file, 'r', encoding='ISO-8859-1') as infile:
        lines = infile.readlines()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            if not any(keyword in line for keyword in keywords):
                outfile.write(line)

if __name__ == '__main__':
    input_file_txt = input("Digite o caminho raiz dos arquivos txt organizados por dia: ")
    output_txt_sem_linhas_inuteis = input("Digite o caminho para o txt sem linhas inúteis: ")
    file_processing.process_files(input_file_txt, output_txt_sem_linhas_inuteis, remove_lines_with_keywords)
    print("Linhas removidas com sucesso!")