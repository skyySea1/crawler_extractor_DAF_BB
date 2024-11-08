import aiohttp
import asyncio
import json
from modules.refs import cidades

url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/beneficiario"

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

async def fetch_city_code(session, cidade):
    payload = {
        "nomeBeneficiarioEntrada": cidade,
        "codigoFundoBaseSaida": 4,
        "siglaFundoSaida": "FPM",
        "nomeFundoSaida": "FUNDO DE PARTICIPACAO"
    }
    try:
        async with session.post(url, json=payload, headers=headers, ssl=False) as response:
            if response.status == 200:
                json_data = await response.json()
                if 'listaBeneficiario' in json_data and json_data['listaBeneficiario']:
                    for beneficiario in json_data['listaBeneficiario']:
                        codigo = beneficiario['codigoBeneficiarioSaida']
                        nome = beneficiario['nomeBeneficiarioSaida']
                        if nome.strip().lower() == cidade.strip().lower():
                            return cidade, codigo
                    print(f'Código não encontrado para {cidade}. Resposta: {json_data}')
                else:
                    print(f'Não há dados de beneficiário para {cidade}. Resposta: {json_data}')
            else:
                print(f'Falha ao buscar código para {cidade}. Status Code: {response.status}')
    except Exception as e:
        print(f'Erro ao processar requisição para {cidade}: {str(e)}')

    return cidade, None

async def main():
    codigos_cidades = {}
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_city_code(session, cidade) for cidade in cidades]
        results = await asyncio.gather(*tasks)

        for cidade, codigo in results:
            if codigo:
                codigos_cidades[cidade] = codigo
                print(f'Cidade: {cidade} - Código: {codigo}')

    # Salvar os resultados em um arquivo JSON
    with open("codigos_por.json", 'w', encoding='utf-8') as file:
        json.dump(codigos_cidades, file, ensure_ascii=False, indent=4)

    print('\nCódigos das cidades salvos em "codigos_por.json"')

if __name__ == "__main__":
    asyncio.run(main())
