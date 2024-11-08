import asyncio
import aiohttp
from modules.refs import cidades
# Lista de cidades para verificar
VAR = cidades
# URL e cabeçalhos para a requisição HTTP
url = "https://demonstrativos.api.daf.bb.com.br/v1/demonstrativo/daf/beneficiario"
headers = {
    "cookie": "a8e750f0330a68375b193d281411cbc4=53c055a30b41a5ee3ae65167887be724",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://demonstrativos.apps.bb.com.br",
    "Referer": "https://demonstrativos.apps.bb.com.br/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
}

async def fetch(session, url, payload):
    try:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                print(f"Erro: Status code {response.status} para payload {payload}")
                return None
            
            data = await response.json()
            lista_beneficiario = data.get('listaBeneficiario', [])
            if not lista_beneficiario:
                return None
            
            resultados = []
            for item in lista_beneficiario:
                nome_beneficiario = item.get('nomeBeneficiarioSaida')
                uf_beneficiario = item.get('siglaUnidadeFederacaoSaida')
                codigo_beneficiario = item.get('codigoBeneficiarioSaida')
                
                if nome_beneficiario in VAR and uf_beneficiario == "BA":
                    resultados.append(codigo_beneficiario)
            
            return resultados if resultados else None
    
    except aiohttp.ClientError as e:
        print(f"Erro de cliente HTTP: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for cidade in VAR:
            payload = {"nomeBeneficiarioEntrada": cidade}
            tasks.append(fetch(session, url, payload))
        
        results = await asyncio.gather(*tasks)
        
        # Filtrar valores None e unir todos os códigos encontrados
        filtered_results = set(codigo for result in results if result for codigo in result)
        
        # Salvar os resultados em um arquivo
        with open("codigos.txt", 'w', encoding='utf-8') as file:
            file.write(',\n'.join(map(str, filtered_results)))

if __name__ == '__main__':
    asyncio.run(main())
