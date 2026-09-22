# Cartola FC API ETL

Este projeto coleta dados públicos do mercado de atletas da API do Cartola FC e grava as informações em MongoDB em coleções estruturadas para análise.

O fluxo principal está em `cartola_etl.py`, que realiza:

- extração do endpoint `https://api.cartola.globo.com/atletas/mercado`
- transformação dos dados do mercado
- carga em MongoDB

---

## Índice

- [Visão geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Configuração do ambiente](#configuração-do-ambiente)
- [Subindo o MongoDB com Docker](#subindo-o-mongodb-com-docker)
- [Executando o ETL](#executando-o-etl)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Coleções no MongoDB](#coleções-no-mongodb)
- [Exemplo de uso da API Cartola](#exemplo-de-uso-da-api-cartola)
- [Verificando os dados](#verificando-os-dados)
- [Troubleshooting](#troubleshooting)

---

## Visão geral

A API da Cartola FC expõe os dados do mercado e dos atletas em tempo real. O script deste projeto usa esse endpoint:

```text
https://api.cartola.globo.com/atletas/mercado
```

Esse endpoint retorna um JSON com dados como:

- clubes
- atletas
- rodada_atual
- status_mercado
- aviso
- fechamento

Os dados são armazenados em MongoDB para consultas posteriores, sem a necessidade de depender da API em cada leitura.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.10+
- pip
- Docker
- Docker Compose
- Git

---

## Estrutura do projeto

```text
cartola-api/
├── api/
│   ├── cartola_etl.py
│   └── datacollector.py
├── cartola_etl.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .env
├── README.md
└── venv/
```

Arquivos importantes:

- `cartola_etl.py`: script principal de extração, transformação e carga
- `api/datacollector.py`: wrapper para executar o ETL com convenção de projeto
- `docker-compose.yml`: orquestra o MongoDB
- `.env`: variáveis locais da aplicação

---

## Configuração do ambiente

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd igbd-nosql/cartola-api
```

### 2. Crie um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

Dependências principais:

- `requests`
- `pymongo`
- `python-dotenv`

---

## Subindo o MongoDB com Docker

O projeto já inclui um `docker-compose.yml` para executar o MongoDB em contêiner.

```bash
docker compose up -d
```

Para verificar se o banco subiu corretamente:

```bash
docker compose ps
```

Você pode validar a conexão com o MongoDB com:

```bash
docker compose logs -f mongodb
```

O MongoDB fica acessível em:

```text
mongodb://localhost:27017
```

---

## Executando o ETL

### Opção 1: executar o script principal

```bash
python cartola_etl.py
```

### Opção 2: executar via wrapper em `api/`

```bash
python api/datacollector.py
```

Esse segundo comando é útil para manter compatibilidade com convenções de execução do projeto.

### O que acontece ao executar

1. o script conecta ao MongoDB
2. faz a requisição para a API do Cartola
3. carrega os dados em coleções
4. registra logs do processo

Exemplo de saída esperada:

```text
2026-09-22T12:00:00Z [INFO] Iniciando ETL Cartola FC...
2026-09-22T12:00:00Z [INFO] Buscando dados na API do Cartola FC...
2026-09-22T12:00:00Z [INFO] Processando e gravando dados...
2026-09-22T12:00:00Z [INFO] Status do mercado gravado com sucesso.
2026-09-22T12:00:00Z [INFO] Finalizado com sucesso.
```

---

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no exemplo:

```bash
cp .env.example .env
```

Exemplo de `.env`:

```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=cartola_fc_db
LOG_LEVEL=INFO
```

### Variáveis disponíveis

| Variável | Descrição | Valor padrão |
|---|---|---|
| `MONGO_URI` | String de conexão do MongoDB | `mongodb://localhost:27017` |
| `MONGO_DB_NAME` | Nome do banco de dados | `cartola_fc_db` |
| `LOG_LEVEL` | Nível de log do Python | `INFO` |

> O projeto também usa as constantes internas `COL_CLUBES`, `COL_ATLETAS` e `COL_MERCADO`, definidas no código.

---

## Coleções no MongoDB

O ETL grava os dados nas seguintes coleções:

- `clubes_rodada_atual`
- `atletas_rodada_atual`
- `mercado_rodada_atual`

### Estrutura resumida

#### `clubes_rodada_atual`

Cada documento representa um clube do mercado atual.

```json
{
  "_id": 262,
  "nome": "Flamengo",
  "abreviacao": "FLA",
  "escudos": { ... },
  "nome_fantasia": "CRF",
  "timestamp_coleta": "2026-09-22T12:00:00+00:00"
}
```

#### `atletas_rodada_atual`

Cada documento representa um atleta do mercado da rodada atual.

```json
{
  "_id": 123,
  "nome": "Pedro",
  "posicao_id": 5,
  "clube_id": 262,
  "status": "provavel",
  "preco_num": 12.5,
  "timestamp_coleta": "2026-09-22T12:00:00+00:00"
}
```

#### `mercado_rodada_atual`

Armazena o estado do mercado e os metadados da rodada.

```json
{
  "rodada_atual": 25,
  "status_mercado": 2,
  "aviso": "Mercado fechado",
  "fechamento": { ... },
  "timestamp_coleta": "2026-09-22T12:00:00+00:00"
}
```

---

## Exemplo de uso da API Cartola

A API pública da Cartola FC pode ser consultada diretamente no navegador ou via `curl`.

### Consultando o mercado

```bash
curl -X GET "https://api.cartola.globo.com/atletas/mercado" \
  -H "Accept: application/json" \
  -H "User-Agent: cartola-etl/1.0"
```

### Python: consumindo a API

```python
import requests

url = "https://api.cartola.globo.com/atletas/mercado"
response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()
print(data["rodada_atual"])
print(len(data.get("atletas", [])))
```

> O projeto usa essa mesma chamada em `buscar_dados_mercado()` para alimentar o MongoDB.

---

## Verificando os dados

Você pode consultar os dados diretamente no MongoDB usando o shell `mongosh`.

### Entrando no container

```bash
docker exec -it cartola-mongodb mongosh
```

### Listando bancos

```javascript
show dbs
```

### Selecionando o banco

```javascript
use cartola_fc_db
```

### Listando coleções

```javascript
show collections
```

### Consultando a coleção de mercado

```javascript
db.mercado_rodada_atual.find().pretty()
```

### Consultando alguns atletas

```javascript
db.atletas_rodada_atual.find().limit(5).pretty()
```

---

## Troubleshooting

### Erro de conexão com MongoDB

Verifique se o Docker está rodando:

```bash
docker compose ps
```

Se necessário, reinicie:

```bash
docker compose down
docker compose up -d
```

### Erro de importação de módulos

Confirme que o ambiente virtual está ativo e que as dependências foram instaladas:

```bash
pip install -r requirements.txt
```

### API indisponível ou lenta

A função `buscar_dados_mercado()` já aplica retries com backoff. Se a API estiver instável, o script tenta novamente antes de falhar.

### May have issue with .env

As variáveis de ambiente são carregadas automaticamente pelo `python-dotenv` no início do script. Verifique se o arquivo `.env` existe e está corretamente preenchido.

---

## Observações finais

Este projeto é uma solução simples de ETL para coleta de dados públicos do Cartola FC e persistência em MongoDB. Ele foi pensado para:

- facilitar a coleta automatizada de dados do mercado
- manter as informações em um banco NoSQL para consultas analíticas
- servir como base para dashboards, relatórios e processamento posterior
