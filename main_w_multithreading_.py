import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime, timedelta
from modules.refs import codigo_cidades, headers  # Importe seus códigos de cidade aqui
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Desabilita os warnings de certificado SSL (apenas para ambiente de teste, não use em produção)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/consulta"



def formatar_data(data):
    return data.strftime("%d.%m.%Y")

fundo_dir = r'C:\Users\Henrique RIbeiro\Documents\projetos em andamentos\daf extração\SUPER\FEB'

if not os.path.exists(fundo_dir):
    os.makedirs(fundo_dir)

municipios_nao_baixados = []

def processar_cidade(session, codigo):
    """
    Processa os dados de uma cidade para cada mês do ano e salva em um arquivo JSON.
    Args:
        session (object): Objeto de sessão para realizar requisições HTTP.
        codigo (int): Código da cidade.
    Returns:
        tuple: Uma tupla contendo o código da cidade e uma mensagem de sucesso ou falha.
    Raises:
        Exception: Se ocorrer algum erro durante o processamento da requisição.
    """
    dados_cidade = {}
    for i in range(12):
        data_inicio = datetime(2023, 1 + i, 1)
        data_fim = (data_inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        payload = {
            "codigoBeneficiario": codigo,
            "codigoFundo": 50,
            "dataInicio": formatar_data(data_inicio),
            "dataFim": formatar_data(data_fim)
        }

        mes = data_inicio.strftime("%B")

        try:
            response = session.post(url, json=payload, headers=headers, verify=False)

            if response.status_code == 200:
                dados_cidade[mes] = response.json()
            else:
                return codigo, f"Falha na consulta para código {codigo}, Mês: {mes}. Status Code: {response.status_code}"

        except Exception as e:
            return codigo, f"Erro ao processar requisição para código {codigo}, Mês: {mes}: {str(e)}"
    
    caminho_json = os.path.join(fundo_dir, f"{codigo}_dados_anuais.json")
    with open(caminho_json, "w") as file:
        file.write(json.dumps(dados_cidade, indent=4, ensure_ascii=False))

    return None, f"Dados anuais para código {codigo} salvos em {caminho_json}\n"

with ThreadPoolExecutor(max_workers=20) as executor:
    with requests.Session() as session:
        futures = [executor.submit(processar_cidade, session, codigo) for codigo in codigo_cidades]

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
