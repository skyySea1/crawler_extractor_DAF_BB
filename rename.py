from refs import cidades, codigo_cidade

# Imprimindo os tamanhos das listas
print(f"Tamanho de cidades: {len(cidades)}")
print(f"Tamanho de codigo_cidade: {len(codigo_cidade)}")

# Imprimindo as primeiras e últimas entradas de ambas as listas para inspeção
print("Primeiras entradas de cidades:", cidades[:5])
print("Últimas entradas de cidades:", cidades[-5:])
print("Primeiras entradas de codigo_cidade:", codigo_cidade[:5])
print("Últimas entradas de codigo_cidade:", codigo_cidade[-5:])

# Assegurando que as listas têm o mesmo tamanho
assert len(cidades) == len(codigo_cidade), "As listas de cidades e códigos têm tamanhos diferentes!"

# Criando um dicionário que mapeia cada cidade ao seu código
cidade_para_codigo = dict(zip(cidades, codigo_cidade))

print(cidade_para_codigo)
