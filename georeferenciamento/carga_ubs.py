import pandas as pd
from pymongo import MongoClient, GEOSPHERE

# 1. Configuração da Conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dados_governamentais"]
colecao_ubs = db["unidades_basicas_saude"]

# Limpando a coleção para não duplicar dados caso rode mais de uma vez
colecao_ubs.delete_many({})

colecao_ubs.create_index([("geometry", GEOSPHERE)])

# 2. Leitura do Arquivo Local
print("Lendo os dados a partir do arquivo local...")
caminho_arquivo = 'ubs.csv'
df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')

# 3. Tratamento dos Dados
# Substituindo vírgulas por pontos nas coordenadas e convertendo para numérico
df['LATITUDE'] = df['LATITUDE'].astype(str).str.replace(',', '.')
df['LONGITUDE'] = df['LONGITUDE'].astype(str).str.replace(',', '.')

df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')

# Removendo registros que ficaram sem latitude ou longitude válidas
df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# 4. Conversão para GeoJSON e Inserção no MongoDB
documentos_geojson = []

for index, row in df.iterrows():
    documento = {
        "type": "Feature",
        "properties": {
            "nome": row.get('NOME', 'Sem Nome'),
            "bairro": row.get('BAIRRO', 'Desconhecido'),
            "estado": row.get('UF', 'Desconhecido'),
            "cnes": row.get('CNES', '')
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row['LONGITUDE'], row['LATITUDE']]
        }
    }
    documentos_geojson.append(documento)

# 5. Persistência dos dados
if documentos_geojson:
    resultado = colecao_ubs.insert_many(documentos_geojson)
    print(f"Sucesso! {len(resultado.inserted_ids)} Unidades Básicas de Saúde foram inseridas no MongoDB.")
else:
    print("Nenhum dado válido encontrado para inserção. Verifique o conteúdo do CSV.")