import os
import re
from modules.refs import cidades, codigo_cidades

# Diretório onde os arquivos estão localizados
directory = r'C:\Users\Henrique RIbeiro\Documents\projetos em andamentos\daf extração\daf_extractions\json'  # Substitua pelo caminho correto

# Verificar se as listas de cidades e códigos têm o mesmo tamanho
assert len(cidades) == len(codigo_cidades), f"As listas de cidades e códigos têm tamanhos diferentes! {len(cidades)} cidades e {len(codigo_cidades)} códigos."

# Criar um dicionário para mapeamento de código para nome da cidade
codigo_para_cidade = dict(zip(codigo_cidades, cidades))
        
# Listar todos os arquivos no diretório
arquivos = os.listdir(directory)

for arquivo in arquivos:
    match = re.match(r'(\d+)_dados_anuais.json', arquivo)
    if match:
        codigo = int(match.group(1))
        if codigo in codigo_para_cidade:
            novo_nome = f"{codigo_para_cidade[codigo]}_dados_anuais.json"
            os.rename(os.path.join(directory, arquivo), os.path.join(directory, novo_nome))
            print(f"Renomeado: {arquivo} para {novo_nome}")
