import requests
from urllib3.exceptions import InsecureRequestWarning
from modules.refs import cidades, codigo_cidade  # Certifique-se de ter o módulo cidades importado corretamente

# Desabilita os warnings de certificado SSL (apenas para ambiente de teste, não use em produção)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/beneficiario"

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

# Dicionário para armazenar os códigos das cidades
codigos_cidades = {}

# Itera sobre as cidades
for cidade in cidades:
    # Monta os dados da requisição
    payload = {"nomeBeneficiarioEntrada": cidade,"codigoFundoBaseSaida": 4,
               	"siglaFundoSaida": "FPM",
			"nomeFundoSaida": "FUNDO DE PARTICIPACAO"}

    try:
        # Realiza a requisição POST
        response = requests.post(url, json=payload, headers=headers, verify=False)

        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            # Extrai e armazena o código da cidade, se houver na resposta
            json_data = response.json()
            if 'listaBeneficiario' in json_data and json_data['listaBeneficiario']:
                codigo_cidade = json_data['listaBeneficiario'][0]['codigoBeneficiarioSaida']
                codigos_cidades[cidade] = codigo_cidade
                print(f'Cidade: {cidade} - Código: {codigo_cidade}')
            else:
                print(f'Não foi possível encontrar o código para {cidade}. Resposta: {json_data}')
        else:
            print(f'Falha ao buscar código para {cidade}. Status Code: {response.status_code}')

    except Exception as e:
        print(f'Erro ao processar requisição para {cidade}: {str(e)}')

# Exibe os códigos das cidades
print('\nCódigos das cidades:')
print(codigos_cidades)
