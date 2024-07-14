from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from refs import data_inicial, data_final, cidades
import pandas as pd
import time
import openpyxl

service = EdgeService()
options = webdriver.EdgeOptions()
options.add_argument('--log-level=1')
options.add_argument('--disable-extensions')
options.add_argument('headless')

driver = webdriver.Edge(service=service, options=options)
driver.get("https://demonstrativos.apps.bb.com.br/arrecadacao-federal")
city_input = driver.find_element_by_ID('f54c28be-df02-4fb8-8851-79d602a9955f')
clicar = driver.find_element_by_CSSSELECTOR('.bb-button.bb-icon-button.default.size-regular')
clicar.click()
fundo = driver.find_element_by_XPATH("//span[normalize-space()='FPM - FUNDO DE PARTICIPACAO']")
fundo.click()
continue_button = driver.find_element_by_XPATH('//*[@id="root"]/div[3]/div[1]/apw-ng-app/app-template/bb-layout/div[1]/div/div/div/div/bb-layout-column/ng-component/div/div/div/app-demonstrativo-daf-selecao/div/div[2]/div/div/form/bb-card/bb-card-footer/div/button[2]')


# Definição das variáveis de origem e destinos
# dicionário que recebe a lista de destinos do módulo regions	e associa esses valores a chave origem(que é a cidade de origem)
# Criar dicionário onde cada cidade é a chave e o valor é uma lista de dicionários com as datas inicial e final


# Iterar sobre o dicionário e imprimir os períodos de cada cidade sem labels
for cidade in cidades:
    for data_i, data_f in data_inicial, data_final:
#         try:
        city_input
#             # Abrir página inicial do Google Maps
#             driver.get("https://www.google.com/maps")
#             wait = WebDriverWait(driver, 15)  #   tempo de espera
#             # Aguardar até que o campo de pesquisa esteja disponível
#             search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]')))
#             search_box.clear()
#             search_box.send_keys(f"{origem} to {destino}")
#             search_box.send_keys(Keys.ENTER)
#             click = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="omnibox-directions"]/div/div[2]/div/div/div/div[2]')))
#             click.click()

#             # Aguardar até que a distância da rota seja carregada
#             distancia = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="section-directions-trip-0"]/div[1]/div/div[1]/div[2]/div')))
#             distancia_texto = distancia.text
#             print(f"Distância de {origem} para {destino}: {distancia_texto}")
            
            
#             # Armazenar o resultado na lista
#             resultados.append({
#                 'Origem': origem,
#                 'Destino': destino,
#                 'Distância': distancia_texto
#             })
        
#         except Exception as e:
#             print(f"Erro ao calcular a rota de {origem} para {destino}: {str(e)}")

# driver.quit()

# # Converter resultados para DataFrame do pandas
# df = pd.DataFrame(resultados)

# # Salvar em Excel
# nome_arquivo = 'distancias_rotas.xlsx'
# df.to_excel(nome_arquivo, index=False)

# print(f"Resultados salvos em '{nome_arquivo}'")
# input("Pressione Enter para sair") # adicione system pause no terminal