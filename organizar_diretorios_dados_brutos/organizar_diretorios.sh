#!/bin/bash

# Caminho base onde estão localizadas as pastas originais
BASE_PATH="/home/vini/Desktop/NovosExamesUnivas06-2024"
# Caminho onde queremos criar as novas pastas organizadas por data
OUTPUT_BASE_PATH="/home/vini/Desktop/novosExamesUnivasOrganizados"

# Função para organizar arquivos por data
organizar_arquivos_por_data() {
	local base_path=$1
	local output_base_path=$2

	# Percorrer todas as pastas e arquivos no diretório base
	find "$base_path" -type f | while read -r file_path; do
		# Ignorar arquivos com extensões específicas
		if [[ $file_path == *.db || $file_path == *.jpeg ]]; then
			continue
		fi
		# Extrair todas as datas no formato "DD/MM/YY" do arquivo
		datas_formatadas=$(grep -oE '[0-9]{2}/[0-9]{2}/[0-9]{2}' "$file_path" | sort | uniq)

		# Verificar se alguma data foi encontrada
		if [[ -n $datas_formatadas ]]; then
			# Processar cada data encontrada
			echo "$datas_formatadas" | while read -r data_formatada; do
				# Extrair dia, mês e ano
				dia=$(echo "$data_formatada" | cut -d'/' -f1)
				mes=$(echo "$data_formatada" | cut -d'/' -f2)
				ano="20$(echo "$data_formatada" | cut -d'/' -f3)"
				data="$ano/$mes/$dia"

				# Criar o caminho da nova pasta baseado na data
				nova_pasta="$output_base_path/$data"
				mkdir -p "$nova_pasta"

				# Armazena o nome do arquivo e o caminho em variáveis
				base_name=$(basename "$file_path")
				dest_path="$nova_pasta/$base_name"

				# Verificar se o arquivo já existe na nova pasta
				if [[ -e $dest_path ]]; then
					count=1
					while [[ -e "${dest_path}_$count" ]]; do
						((count++))
					done
					dest_path="${dest_path}_$count"
					cp "$file_path" "$dest_path"
					echo "$file_path já existe, copiado como ${base_name}_$count para $nova_pasta/"
				else
					# Copiar o arquivo para a nova pasta com o novo nome
					cp "$file_path" "$nova_pasta/"
					echo "Copiado $file_path para $nova_pasta/"
				fi
			done
		else
			echo "Nenhuma data encontrada no formato DD/MM/YY no arquivo $file_path"
		fi
	done
}

# Chamar a função para executar a organização dos arquivos
organizar_arquivos_por_data "$BASE_PATH" "$OUTPUT_BASE_PATH"
