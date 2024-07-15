import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from modules.refs import codigo_cidades, cidades  # Importe suas listas de códigos de cidade e cidades aqui
import json
import concurrent.futures

# Desabilita os warnings de certificado SSL (apenas para ambiente de teste, não use em produção)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/consulta"

# Dados do cabeçalho da requisição
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://demonstrativos.apps.bb.com.br",
    "Referer": "https://demonstrativos.apps.bb.com.br/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
}

# Função para formatar a data conforme necessário pelo endpoint
def formatar_data(data):
    return data.strftime("%d.%m.%Y")

# Diretório onde os arquivos JSON serão salvos
json_directory = r'C:\Users\Henrique RIbeiro\Documents\projetos em andamentos\daf extração\daf_extractions\json3'

# Criar o diretório 'json3' se ele não existir
if not os.path.exists(json_directory):
    os.makedirs(json_directory)

# Mapeia códigos de cidade para nomes de cidade
codigo_para_cidade = dict(zip(codigo_cidades, cidades))

# Lista para armazenar códigos de cidades que não foram baixados com sucesso
municipios_nao_baixados = []

def fetch_data(codigo):
    nome_cidade = codigo_para_cidade.get(codigo, "Desconhecido")
    # Dicionário para armazenar os dados de todos os meses
    dados_cidade = {}

    with requests.Session() as session:
        session.headers.update(headers)
        
        # Itera sobre os 12 meses
        for i in range(12):
            # Define a data inicial e final para o mês atual
            data_inicio = datetime(2023, 1 + i, 1)
            data_fim = datetime(2023, 1 + i, 1).replace(day=28) + timedelta(days=4)
            data_fim = data_fim.replace(day=1) - timedelta(days=1)

            # Monta os dados da requisição para o mês atual
            payload = {
                "codigoBeneficiario": codigo,
                "codigoFundo": 4,
                "dataInicio": formatar_data(data_inicio),
                "dataFim": formatar_data(data_fim)
            }

            try:
                # Realiza a requisição POST
                response = session.post(url, json=payload, verify=False)

                # Verifica se a requisição foi bem sucedida
                if response.status_code == 200:
                    # Processa a resposta conforme necessário
                    json_data = response.json()

                    # Adiciona os dados ao dicionário para este mês
                    mes = data_inicio.strftime("%B")
                    dados_cidade[mes] = json_data

                    print(f"Dados para código {codigo} ({nome_cidade}), Mês: {mes} obtidos com sucesso.")
                else:
                    print(f"Falha na consulta para código {codigo} ({nome_cidade}), Mês: {data_inicio.strftime('%B')}. Status Code: {response.status_code}")
                    municipios_nao_baixados.append((codigo, nome_cidade))
                    return

            except Exception as e:
                print(f"Erro ao processar requisição para código {codigo} ({nome_cidade}), Mês: {data_inicio.strftime('%B')}: {str(e)}")
                municipios_nao_baixados.append((codigo, nome_cidade))
                return

    # Nome do arquivo baseado no código da cidade
    nome_arquivo = f"{codigo}_dados_anuais.json"

    # Caminho completo do arquivo JSON na pasta 'json3'
    caminho_json = os.path.join(json_directory, nome_arquivo)

    # Salva os dados da cidade em um arquivo JSON único para o ano
    if (codigo, nome_cidade) not in municipios_nao_baixados:
        with open(caminho_json, "w") as file:
            file.write(json.dumps(dados_cidade, indent=4, ensure_ascii=False))

        print(f"Dados anuais para código {codigo} ({nome_cidade}) salvos em {caminho_json}\n")

# Utiliza ThreadPoolExecutor para fazer requisições em paralelo
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(fetch_data, codigo_cidades)

# Exibe os códigos de cidades que não foram baixados com sucesso
if municipios_nao_baixados:
    print("Os seguintes municípios não foram baixados com sucesso:")
    for codigo, nome in municipios_nao_baixados:
        print(f"Código: {codigo}, Nome: {nome}")
else:
    print("Todos os municípios foram baixados com sucesso.")
