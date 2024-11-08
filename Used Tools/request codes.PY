from urllib3.exceptions import InsecureRequestWarning

import requests
VAR = {'ABAIRA', 'ABARE', 'ACAJUTIBA', 'ADUSTINA', 'AGUA', 'FRIA', 'AIQUARA', 'ALAGOINHAS', 'ALCOBACA', 'ALMADINA', 'AMARGOSA', 'AMELIA', 'RODRIGUES', 'AMERICA', 'DOURADA', 'ANAGE', 'ANDARAI', 'ANDORINHA', 'ANGICAL', 'ANGUERA', 'ANTAS', 'ANTONIO', 'CARDOSO', 'ANTONIO', 'GONCALVES', 'APORA', 'APUAREMA', 'ARACAS', 'ARACATU', 'ARACI', 'ARAMARI', 'ARATACA', 'ARATUIPE', 'AURELINO', 'LEAL', 'BAIANOPOLIS', 'BAIXA', 'GRANDE', 'BANZAE', 'BARRA', 'BARRA', 'DA', 'ESTIVA', 'BARRA', 'DO', 'CHOCA', 'BARRA', 'DO', 'MENDES', 'BARRA', 'DO', 'ROCHA', 'BARREIRAS', 'BARRO', 'ALTO', 'BARRO', 'PRETO', 'BARROCAS', 'BELMONTE', 'BELO', 'CAMPO', 'BIRITINGA', 'BOA', 'NOVA', 'BOA', 'VISTA', 'DO', 'TUPIM', 'BOM', 'JESUS', 'DA', 'LAPA', 'BOM', 'JESUS', 'DA', 'SERRA', 'BONINAL', 'BONITO', 'BOQUIRA', 'BOTUPORA', 'BREJOES', 'BREJOLANDIA', 'BROTAS', 'DE', 'MACAUBAS', 'BRUMADO', 'BUERAREMA', 'BURITIRAMA', 'CAATIBA', 'CABACEIRAS', 'DO', 'PARAGUACU', 'CACHOEIRA', 'CACULE', 'CAEM', 'CAETANOS', 'CAETITE', 'CAFARNAUM', 'CAIRU', 'CALDEIRAO', 'GRANDE', 'CAMACAN', 'CAMACARI', 'CAMAMU', 'CAMPO', 'ALEGRE', 'DE', 'LOURDES', 'CAMPO', 'FORMOSO', 'CANAPOLIS', 'CANARANA', 'CANAVIEIRAS', 'CANDEAL', 'CANDEIAS', 'CANDIBA', 'CANDIDO', 'SALES', 'CANSANCAO', 'CANUDOS', 'CAPELA', 'DO', 'ALTO', 'ALEGRE', 'CAPIM', 'GROSSO', 'CARAIBAS', 'CARAVELAS', 'CARDEAL', 'DA', 'SILVA', 'CARINHANHA', 'CASA', 'NOVA', 'CASTRO', 'ALVES', 'CATOLANDIA', 'CATU', 'CATURAMA', 'CENTRAL', 'CHORROCHO', 'CICERO', 'DANTAS', 'CIPO', 'COARACI', 'COCOS', 'CONCEICAO', 'DA', 'FEIRA', 'CONCEICAO', 'DO', 'ALMEIDA', 'CONCEICAO', 'DO', 'COITE', 'CONCEICAO', 'DO', 'JACUIPE', 'CONDE', 'CONDEUBA', 'CONTENDAS', 'DO', 'SINCORA', 'CORACAO', 'DE', 'MARIA', 'CORDEIROS', 'CORIBE', 'CORONEL', 'JOAO', 'SA', 'CORRENTINA', 'COTEGIPE', 'CRAVOLANDIA', 'CRISOPOLIS', 'CRISTOPOLIS', 'CRUZ', 'DAS', 'ALMAS', 'CURACA', 'DARIO', 'MEIRA', 'DIAS', "D'AVILA", 'DOM', 'BASILIO', 'DOM', 'MACEDO', 'COSTA', 'ELISIO', 'MEDRADO', 'ENCRUZILHADA', 'ENTRE', 'RIOS', 'ERICO', 'CARDOSO', 'ESPLANADA', 'EUCLIDES', 'DA', 'CUNHA', 'EUNAPOLIS', 'FATIMA', 'FEIRA', 'DA', 'MATA', 'FEIRA', 'DE', 'SANTANA', 'FILADELFIA', 'FIRMINO', 'ALVES', 'FLORESTA', 'AZUL', 'FORMOSA', 'DO', 'RIO', 'PRETO', 'GANDU', 'GAVIAO', 'GENTIO', 'DO', 'OURO', 'GLORIA', 'GONGOGI', 'GOVERNADOR', 'MANGABEIRA', 'GUAJERU', 'GUANAMBI', 'GUARATINGA', 'HELIOPOLIS', 'IACU', 'IBIASSUCE', 'IBICARAI', 'IBICOARA', 'IBICUI', 'IBIPEBA', 'IBIPITANGA', 'IBIQUERA', 'IBIRAPITANGA', 'IBIRAPUA', 'IBIRATAIA', 'IBITIARA', 'IBITITA', 'IBOTIRAMA', 'ICHU', 'IGAPORA', 'IGRAPIUNA', 'IGUAI', 'ILHEUS', 'INHAMBUPE', 'IPECAETA', 'IPIAU', 'IPIRA', 'IPUPIARA', 'IRAJUBA', 'IRAMAIA', 'IRAQUARA', 'IRARA', 'IRECE', 'ITABELA', 'ITABERABA', 'ITABUNA', 'ITACARE', 'ITAETE', 'ITAGI', 'ITAGIBA', 'ITAGIMIRIM', 'ITAGUACU', 'DA', 'BAHIA', 'ITAJU', 'DO', 'COLONIA', 'ITAJUIPE', 'ITAMARAJU', 'ITAMARI', 'ITAMBE', 'ITANAGRA', 'ITANHEM', 'ITAPARICA', 'ITAPE', 'ITAPEBI', 'ITAPETINGA', 'ITAPICURU', 'ITAPITANGA', 'ITAQUARA', 'ITARANTIM', 'ITATIM', 'ITIRUCU', 'ITIUBA', 'ITORORO', 'ITUACU', 'ITUBERA', 'IUIU', 'JABORANDI', 'JACARACI', 'JACOBINA', 'JAGUAQUARA', 'JAGUARARI', 'JAGUARIPE', 'JANDAIRA', 'JEQUIE', 'JEREMOABO', 'JIQUIRICA', 'JITAUNA', 'JOAO', 'DOURADO', 'JUAZEIRO', 'JUCURUCU', 'JUSSARA', 'JUSSARI', 'JUSSIAPE', 'LAFAIETE', 'COUTINHO', 'LAGOA', 'REAL', 'LAJE', 'LAJEDAO', 'LAJEDINHO', 'LAJEDO', 'DO', 'TABOCAL', 'LAMARAO', 'LAPAO', 'LAURO', 'DE', 'FREITAS', 'LENCOIS', 'LICINIO', 'DE', 'ALMEIDA', 'LIVRAMENTO', 'DE', 'NOSSA', 'SENHORA', 'LUIS', 'EDUARDO', 'MAGALHAES', 'MACAJUBA', 'MACARANI', 'MACAUBAS', 'MACURURE', 'MADRE', 'DE', 'DEUS', 'MAETINGA', 'MAIQUINIQUE', 'MAIRI', 'MALHADA', 'MALHADA', 'DE', 'PEDRAS', 'MANOEL', 'VITORINO', 'MANSIDAO', 'MARACAS', 'MARAGOGIPE', 'MARAU', 'MARCIONILIO', 'SOUZA', 'MASCOTE', 'MATA', 'DE', 'SAO', 'JOAO', 'MATINA', 'MEDEIROS', 'NETO', 'MIGUEL', 'CALMON', 'MILAGRES', 'MIRANGABA', 'MIRANTE', 'MONTE', 'SANTO', 'MORPARA', 'MORRO', 'DO', 'CHAPEU', 'MORTUGABA', 'MUCUGE', 'MUCURI', 'MULUNGU', 'DO', 'MORRO', 'MUNDO', 'NOVO', 'MUNIZ', 'FERREIRA', 'MUQUEM', 'DO', 'SAO', 'FRANCISCO', 'MURITIBA', 'MUTUIPE', 'NAZARE', 'NILO', 'PECANHA', 'NORDESTINA', 'NOVA', 'CANAA', 'NOVA', 'FATIMA', 'NOVA', 'IBIA', 'NOVA', 'ITARANA', 'NOVA', 'REDENCAO', 'NOVA', 'SOURE', 'NOVA', 'VICOSA', 'NOVO', 'HORIZONTE', 'NOVO', 'TRIUNFO', 'OLINDINA', 'OLIVEIRA', 'DOS', 'BREJINHOS', 'OURICANGAS', 'OUROLANDIA', 'PALMAS', 'DE', 'MONTE', 'ALTO', 'PALMEIRAS', 'PARAMIRIM', 'PARATINGA', 'PARIPIRANGA', 'PAU', 'BRASIL', 'PAULO', 'AFONSO', 'PE', 'DE', 'SERRA', 'PEDRAO', 'PEDRO', 'ALEXANDRE', 'PIATA', 'PILAO', 'ARCADO', 'PINDAI', 'PINDOBACU', 'PINTADAS', 'PIRAI', 'DO', 'NORTE', 'PIRIPA', 'PIRITIBA', 'PLANALTINO', 'PLANALTO', 'POCOES', 'POJUCA', 'PONTO', 'NOVO', 'PORTO', 'SEGURO', 'POTIRAGUA', 'PRADO', 'PRESIDENTE', 'DUTRA', 'PRESIDENTE', 'JANIO', 'QUADROS', 'PRESIDENTE', 'TANCREDO', 'NEVES', 'QUEIMADAS', 'QUIJINGUE', 'QUIXABEIRA', 'RAFAEL', 'JAMBEIRO', 'REMANSO', 'RETIROLANDIA', 'RIACHAO', 'DAS', 'NEVES', 'RIACHAO', 'DO', 'JACUIPE', 'RIACHO', 'DE', 'SANTANA', 'RIBEIRA', 'DO', 'AMPARO', 'RIBEIRA', 'DO', 'POMBAL', 'RIBEIRAO', 'DO', 'LARGO', 'RIO', 'DE', 'CONTAS', 'RIO', 'DO', 'ANTONIO', 'RIO', 'DO', 'PIRES', 'RIO', 'REAL', 'RODELAS', 'RUY', 'BARBOSA', 'SALINAS', 'DA', 'MARGARIDA', 'SALVADOR', 'SANTA', 'BARBARA', 'SANTA', 'BRIGIDA', 'SANTA', 'CRUZ', 'CABRALIA', 'SANTA', 'CRUZ', 'DA', 'VITORIA', 'SANTA', 'INES', 'SANTA', 'LUZIA', 'SANTA', 'MARIA', 'DA', 'VITORIA', 'SANTA', 'RITA', 'DE', 'CASSIA', 'SANTA', 'TEREZINHA', 'SANTALUZ', 'SANTANA', 'SANTANOPOLIS', 'SANTO', 'AMARO', 'SANTO', 'ANTONIO', 'DE', 'JESUS', 'SANTO', 'ESTEVAO', 'SAO', 'DESIDERIO', 'SAO', 'DOMINGOS', 'SAO', 'FELIPE', 'SAO', 'FELIX', 'SAO', 'FELIX', 'DO', 'CORIBE', 'SAO', 'FRANCISCO', 'DO', 'CONDE', 'SAO', 'GABRIEL', 'SAO', 'GONCALO', 'DOS', 'CAMPOS', 'SAO', 'JOSE', 'DA', 'VITORIA', 'SAO', 'JOSE', 'DO', 'JACUIPE', 'SAO', 'MIGUEL', 'DAS', 'MATAS', 'SAO', 'SEBASTIAO', 'DO', 'PASSE', 'SAPEACU', 'SATIRO', 'DIAS', 'SAUBARA', 'SAUDE', 'SEABRA', 'SEBASTIAO', 'LARANJEIRAS', 'SENHOR', 'DO', 'BONFIM', 'SENTO', 'SE', 'SERRA', 'DO', 'RAMALHO', 'SERRA', 'DOURADA', 'SERRA', 'PRETA', 'SERRINHA', 'SERROLANDIA', 'SIMOES', 'FILHO', 'SITIO', 'DO', 'MATO', 'SITIO', 'DO', 'QUINTO', 'SOBRADINHO', 'SOUTO', 'SOARES', 'TABOCAS', 'DO', 'BREJO', 'VELHO', 'TANHACU', 'TANQUE', 'NOVO', 'TANQUINHO', 'TAPEROA', 'TAPIRAMUTA', 'TEIXEIRA', 'DE', 'FREITAS', 'TEODORO', 'SAMPAIO', 'TEOFILANDIA', 'TEOLANDIA', 'TERRA', 'NOVA', 'TREMEDAL', 'TUCANO', 'UAUA', 'UBAIRA', 'UBAITABA', 'UBATA', 'UIBAI', 'UMBURANAS', 'UNA', 'URANDI', 'URUCUCA', 'UTINGA', 'VALENCA', 'VALENTE', 'VARZEA', 'DA', 'ROCA', 'VARZEA', 'DO', 'POCO', 'VARZEA', 'NOVA', 'VARZEDO', 'VERA', 'CRUZ', 'VEREDA', 'VITORIA', 'DA', 'CONQUISTA', 'WAGNER', 'WANDERLEY', 'WENCESLAU', 'GUIMARAES', 'XIQUE-XIQUE'}

import asyncio
import aiohttp


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
    async with session.post(url, json=payload) as response:
        data = await response.json()
        # Extraindo o valor do codigoBeneficiarioSaida
        codigo_beneficiario = data.get('listaBeneficiario', [{}])[0].get('codigoBeneficiarioSaida')
        return codigo_beneficiario

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for cidade in VAR:
            payload = {"nomeBeneficiarioEntrada": cidade}
            tasks.append(fetch(session, url, payload))
        
        results = await asyncio.gather(*tasks)
        
        # Filtrar valores None e remover duplicatas
        filtered_results = set(filter(None, results))
        
        with open("codigos.txt", 'w', encoding='utf-8') as file:
            file.write(',\n'.join(map(str, filtered_results)))

asyncio.run(main())