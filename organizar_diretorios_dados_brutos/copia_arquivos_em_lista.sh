#!/bin/bash

# Verifica se o arquivo de lista de caminhos foi fornecido
if [ $# -ne 2 ]; then
  echo "Uso: $0 <arquivo_de_lista.txt> <diretorio_destino>"
  exit 1
fi

# Arquivo contendo os caminhos dos arquivos a serem copiados
arquivo_de_lista=$1

# Diretório de destino para onde os arquivos serão copiados
diretorio_destino=$2

# Verifica se o diretório de destino existe, se não, cria
if [ ! -d "$diretorio_destino" ]; then
  echo "Diretório de destino não existe. Criando..."
  mkdir -p "$diretorio_destino"
fi

# Lê cada linha do arquivo e copia o arquivo para o diretório de destino
while IFS= read -r caminho; do
  if [ -f "$caminho" ]; then
    cp "$caminho" "$diretorio_destino"
    echo "Arquivo $caminho copiado com sucesso."
  else
    echo "Arquivo $caminho não encontrado."
  fi
done < "$arquivo_de_lista"

echo "Cópia concluída."