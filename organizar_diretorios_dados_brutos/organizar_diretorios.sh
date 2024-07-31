#!/bin/bash

# - O Seguinte script copia cada arquivo dentro de um diretório raiz de profundidade qualquer e cola ele dentro de uma pasta específica da data retirada de dentro do próprio arquivo
# - Como os arquivos brutos podem estar em pastas diferentes, pode existir arquivos com mesmo nome, o script adiciona (1), (2) ou (3) e assim por diante, no nome do arquivo caso a pasta destino tenha um arquivo com mesmo nome
#     - Isso acaba ocasionando na duplicação de alguns exames
# - Para arquivos com mais de uma data o script adiciona ele em pastas de datas diferentes, ou seja, o dado é duplicado.

# Caminho base onde estão localizadas as pastas originais
BASE_PATH="/home/vini/Desktop/pareamento/brutos-desorganizados"
# Caminho onde queremos criar as novas pastas organizadas por data
OUTPUT_BASE_PATH="/home/vini/Desktop/pareamento/brutos-organizados"

# Função para organizar arquivos por data
organizar_arquivos_por_data() {
	local base_path=$1
	local output_base_path=$2

	# Percorrer todas as pastas e arquivos no diretório base
	find "$base_path" -type f | while read -r file_path; do
		# Ignorar arquivos com extensões específicas
		if [[ $file_path == *.db || $file_path == *.jpeg || $file_path == *.pptx || $file_path == *.mp4 ]]; then
			echo "Arquivo $file_path não pasosu na verificação de extensão"
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

				# Calcular o hash do arquivo atual
				current_hash=$(md5sum "$file_path" | awk '{ print $1 }')

				# Verificar se já existe um arquivo com o mesmo hash na pasta de destino
				if [[ -e $dest_path ]]; then
					existing_hash=$(md5sum "$dest_path" | awk '{ print $1 }')
					if [[ $current_hash == $existing_hash ]]; then
						echo "Arquivo duplicado encontrado: $file_path não foi copiado para $nova_pasta/ pois já existe um arquivo idêntico."
						continue
					else
						count=1
						while [[ -e "${dest_path}_$count" ]]; do
							existing_hash=$(md5sum "${dest_path}_$count" | awk '{ print $1 }')
							if [[ $current_hash == $existing_hash ]]; then
								echo "Arquivo duplicado encontrado: $file_path não foi copiado para $nova_pasta/ pois já existe um arquivo idêntico."
								continue 2
							fi
							((count++))
						done
						dest_path="${dest_path}_$count"
					fi
				fi

				# Copiar o arquivo para a nova pasta com o novo nome
				cp "$file_path" "$dest_path"
				echo "Copiado $file_path para $nova_pasta/"
			done
		else
			echo "Nenhuma data encontrada no formato DD/MM/YY no arquivo $file_path"
		fi
	done
}

# Chamar a função para executar a organização dos arquivos
organizar_arquivos_por_data "$BASE_PATH" "$OUTPUT_BASE_PATH"