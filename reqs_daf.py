import requests
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from refs import codigo_cidade  # Importe seus códigos de cidade aqui
import json
import time 

# Desabilita os warnings de certificado SSL (apenas para ambiente de teste, não use em produção)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/consulta"

# Dados do cabeçalho da requisição
headers = {
    "cookie": "a8e750f0330a68375b193d281411cbc4=bf1ebe0c3bb06091b0a73a40de712a02",
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

# Para cada código de cidade
for codigo in codigo_cidade:
    # Dicionário para armazenar os dados de todos os meses
    dados_cidade = {}

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
            response = requests.post(url, json=payload, headers=headers, verify=False)

            # Verifica se a requisição foi bem sucedida
            if response.status_code == 200:
                # Processa a resposta conforme necessário
                json_data = response.json()

                # Adiciona os dados ao dicionário para este mês
                mes = data_inicio.strftime("%B")
                dados_cidade[mes] = json_data

                print(f"Dados para código {codigo}, Mês: {mes} obtidos com sucesso.")
            else:
                print(f"Falha na consulta para código {codigo}, Mês: {data_inicio.strftime('%B')}. Status Code: {response.status_code}")

        except Exception as e:
            print(f"Erro ao processar requisição para código {codigo}, Mês: {data_inicio.strftime('%B')}: {str(e)}")

    # Nome do arquivo baseado no código da cidade
    nome_arquivo = f"{codigo}_dados_anuais.json"

    # Salva os dados da cidade em um arquivo JSON único para o ano
    with open(nome_arquivo, "w") as file:
        file.write(json.dumps(dados_cidade, indent=4, ensure_ascii=False))

    print(f"Dados anuais para código {codigo} salvos em {nome_arquivo}\n")
