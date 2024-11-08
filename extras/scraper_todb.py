import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from modules.refs import codigo_cidades  # Importe seus códigos de cidade aqui
import pyodbc
import json
import re

# Desabilita os warnings de certificado SSL (apenas para ambiente de teste, não use em produção)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# URL da API
url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/consulta"

# Cabeçalhos HTTP
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

# Função para formatar a data
def formatar_data(data):
    return data.strftime("%d.%m.%Y")

# Regex para capturar data, parcela e valor
pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})\s+(.+?)\s+([\d\.,]+[C|D])")

# Segunda regex para capturar apenas parcela e valor
pattern2 = re.compile(r"([^\d]+)\s+([\d\.,]+[CD])")

# Lista para armazenar códigos de cidades que não foram baixados com sucesso
municipios_nao_baixados = []

ultima_data_transacao = None

for codigo in codigo_cidades:
    for i in range(12):
        data_inicio = datetime(2023, 1 + i, 1)
        data_fim = datetime(2023, 1 + i, 1).replace(day=28) + timedelta(days=4)
        data_fim = data_fim.replace(day=1) - timedelta(days=1)

        payload = {
            "codigoBeneficiario": codigo,
            "codigoFundo": 19,
            "dataInicio": formatar_data(data_inicio),
            "dataFim": formatar_data(data_fim)
        }

        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)

            if response.status_code == 200:
                json_data = response.json()

                mes = data_inicio.strftime("%B")
                ano = data_inicio.strftime("%Y")

                # Iterar sobre os dados e fazer a inserção no banco
                for ocorrencia in json_data.get("quantidadeOcorrencia", []):
                    nomeBeneficio = ocorrencia["nomeBeneficio"].strip()

                    match = pattern.match(nomeBeneficio)
                    if match:
                        data_transacao = match.group(1)
                        parcela = match.group(2)
                        valor_distribuido = match.group(3)

                        print(f"Data Transacao: {data_transacao}, Parcela: {parcela}, Valor Distribuído: {valor_distribuido}")

                        # Atualizar a última data de transação encontrada
                        ultima_data_transacao = data_transacao
                    else:
                        match2 = pattern2.match(nomeBeneficio)
                        if match2:
                            data_transacao = ultima_data_transacao
                            parcela = match2.group(1).strip()
                            valor_distribuido = match2.group(2)

                            print(f"Data Transacao2: {data_transacao}, Parcela2: {parcela}, Valor Distribuído2: {valor_distribuido}")

  

                print(f"Dados para código {codigo}, Mês: {mes} obtidos e salvos com sucesso.")
            else:
                print(f"Falha na consulta para código {codigo}, Mês: {data_inicio.strftime('%B')}. Status Code: {response.status_code}")
                municipios_nao_baixados.append(codigo)
                break  # Pula para o próximo código de cidade

        except Exception as e:
            print(f"Erro ao processar requisição para código {codigo}, Mês: {data_inicio.strftime('%B')}: {str(e)}")
            municipios_nao_baixados.append(codigo)
            break  # Pula para o próximo código de cidade


# Exibe os códigos de cidades que não foram baixados com sucesso
if municipios_nao_baixados:
    print("Os seguintes municípios não foram baixados com sucesso:")
    for codigo in municipios_nao_baixados:
        print(codigo)
else:
    print("Todos os municípios foram baixados com sucesso.")