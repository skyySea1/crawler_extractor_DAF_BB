import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from modules.refs import codigo_cidades  # Importe seus códigos de cidade aqui
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Desabilita os warnings de certificado SSL (apenas para ambiente de teste, não use em produção)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/consulta"

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

def formatar_data(data):
    return data.strftime("%d.%m.%Y")

icms_dir = r'C:\Users\Henrique RIbeiro\Documents\projetos em andamentos\daf extração\icms_final\FASTER'

if not os.path.exists(icms_dir):
    os.makedirs(icms_dir)

municipios_nao_baixados = []

def processar_cidade(codigo):
    dados_cidade = {}
    for i in range(12):
        data_inicio = datetime(2023, 1 + i, 1)
        data_fim = (data_inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        payload = {
            "codigoBeneficiario": codigo,
            "codigoFundo": 19,
            "dataInicio": formatar_data(data_inicio),
            "dataFim": formatar_data(data_fim)
        }

        mes = data_inicio.strftime("%B")

        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)

            if response.status_code == 200:
                dados_cidade[mes] = response.json()
            else:
                return codigo, f"Falha na consulta para código {codigo}, Mês: {mes}. Status Code: {response.status_code}"

        except Exception as e:
            return codigo, f"Erro ao processar requisição para código {codigo}, Mês: {mes}: {str(e)}"
    
    caminho_json = os.path.join(icms_dir, f"{codigo}_dados_anuais.json")
    with open(caminho_json, "w") as file:
        file.write(json.dumps(dados_cidade, indent=4, ensure_ascii=False))

    return None, f"Dados anuais para código {codigo} salvos em {caminho_json}\n"

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(processar_cidade, codigo) for codigo in codigo_cidades]

    for future in as_completed(futures):
        codigo, mensagem = future.result()
        if codigo:
            municipios_nao_baixados.append(codigo)
        print(mensagem)

if municipios_nao_baixados:
    print("Os seguintes municípios não foram baixados com sucesso:")
    for codigo in municipios_nao_baixados:
        print(codigo)
else:
    print("Todos os municípios foram baixados com sucesso.")
