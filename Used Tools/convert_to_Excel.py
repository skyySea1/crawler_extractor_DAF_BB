import os
import pandas as pd
import openpyxl

# Diretório onde os arquivos CSV estão localizados
directory = r'C:\Users\Henrique RIbeiro\Documents\projetos em andamentos\daf extração\daf_extractions\csv'  # Substitua pelo caminho correto

# Diretório onde os arquivos Excel serão salvos
excel_directory = os.path.join(directory, 'excel')

# Criar o diretório 'excel' se ele não existir
if not os.path.exists(excel_directory):
    os.makedirs(excel_directory)

# Listar todos os arquivos no diretório
arquivos = os.listdir(directory)

# Filtrar apenas os arquivos CSV
arquivos_csv = [arquivo for arquivo in arquivos if arquivo.endswith('.csv')]

for arquivo_csv in arquivos_csv:
    # Caminho completo do arquivo CSV
    caminho_csv = os.path.join(directory, arquivo_csv)
    
    # Carregar o arquivo CSV em um DataFrame
    df = pd.read_csv(caminho_csv)
    
    # Substituir a extensão .csv por .xlsx
    arquivo_excel = arquivo_csv.replace('.csv', '.xlsx')
    
    # Caminho completo do arquivo Excel na pasta 'excel'
    caminho_excel = os.path.join(excel_directory, arquivo_excel)
    
    # Salvar o DataFrame como um arquivo Excel
    df.to_excel(caminho_excel, index=False)
    
    print(f"Convertido: {arquivo_csv} para {arquivo_excel}")

print("Todos os arquivos CSV foram convertidos para Excel e salvos na pasta 'excel'.")
