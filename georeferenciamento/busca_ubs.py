from pymongo import MongoClient

# 1. Configuração da Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dados_governamentais"]
colecao_ubs = db["unidades_basicas_saude"]

# 2. Definindo o ponto de origem para a busca
# Exemplo usando uma coordenada na região central de São Paulo
# Importante: O formato GeoJSON exige a ordem [Longitude, Latitude]
ponto_busca = {
    "type": "Point",
    "coordinates": [-46.656, -23.561]
}

# 3. Montando a consulta (query) geoespacial
query = {
    "geometry": {
        "$near": {
            "$geometry": ponto_busca,
            "$maxDistance": 5000  # Busca em um raio máximo de 5000 metros (5km)
        }
    }
}

# 4. Executando a busca e limitando aos 3 resultados mais próximos
print("Buscando as 3 UBS mais próximas num raio de 5km...")
ubs_proximas = colecao_ubs.find(query).limit(3)

# 5. Iterando e exibindo os resultados
encontrou = False
for ubs in ubs_proximas:
    encontrou = True
    nome = ubs['properties'].get('nome', 'Sem Nome')
    cidade = ubs['properties'].get('cidade', 'Desconhecida')
    estado = ubs['properties'].get('estado', 'Desconhecido')

    print(f"- {nome} em {cidade}-{estado}")

if not encontrou:
    print("Nenhuma UBS encontrada nesse raio de distância para as coordenadas informadas.")