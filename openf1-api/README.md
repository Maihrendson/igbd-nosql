# 🏎️ OpenF1 Data Collector & NoSQL Pipeline

Pipeline em Python para coleta, tratamento e ingestão de telemetria e dados históricos da Fórmula 1 a partir da API pública [OpenF1](https://openf1.org), persistindo as informações de forma estruturada no banco de dados NoSQL **MongoDB**.

O projeto conta com controle de idempotência (operações de *upsert*) para garantir que execuções sucessivas não gerem registros duplicados nas coleções.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Guia de Instalação e Execução](#-guia-de-instalação-e-execução)
  - [1. Clonar o Repositório](#1-clonar-o-repositório)
  - [2. Configurar o Ambiente Virtual (Python)](#2-configurar-o-ambiente-virtual-python)
  - [3. Instalar Dependências](#3-instalar-dependências)
  - [4. Subir o MongoDB via Docker](#4-subir-o-mongodb-via-docker)
  - [5. Configurar as Variáveis de Ambiente (`.env`)](#5-configurar-as-variáveis-de-ambiente-env)
  - [6. Executar o Coletor de Dados](#6-executar-o-coletor-de-dados)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Como Obter as Chaves da OpenF1](#-como-obter-as-chaves-da-openf1)
- [Estrutura e Modelagem no MongoDB](#-estrutura-e-modelagem-no-mongodb)
- [Verificação e Consulta dos Dados](#-verificação-e-consulta-dos-dados)
- [Comandos Úteis de Suporte](#-comandos-úteis-de-suporte)
- [Resolução de Problemas (Troubleshooting)](#-resolução-de-problemas-troubleshooting)

---

## 🔭 Visão Geral

O script `api/datacollector.py` realiza o fluxo de ETL (Extração, Transformação e Carga) consumindo três endpoints principais da API OpenF1 para uma corrida ou evento específico:

1. **Sessões (`sessions`)**: Metadados da etapa e sessão (treinos, qualificação, sprint ou corrida).
2. **Pilotos (`drivers`)**: Lista de pilotos participantes, números de carro, siglas e equipes.
3. **Voltas (`laps`)**: Tempos por setor, tempo de volta, velocidade e telemetria por piloto.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**: Linguagem de programação principal.
- **Requests**: Cliente HTTP para consultas à API REST OpenF1.
- **PyMongo**: Driver oficial de conexão e manipulação do MongoDB em Python.
- **Python-dotenv**: Gerenciamento seguro de configurações via arquivo `.env`.
- **MongoDB 7**: Banco de dados NoSQL orientado a documentos.
- **Docker & Docker Compose**: Orquestração do contêiner do banco de dados para fácil replicação do ambiente.

---

## 📁 Estrutura do Projeto

```text
openf1-api/
├── api/
│   └── datacollector.py    # Script principal de extração e carga no MongoDB
├── docker-compose.yml      # Configuração do serviço MongoDB (porta 27017)
├── requirements.txt        # Dependências Python do projeto
├── .env.example            # Modelo de configuração de variáveis de ambiente
├── .gitignore              # Ignora ambientes virtuais, .env e arquivos de IDE
└── README.md               # Documentação completa do projeto
```

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/) e o gerenciador de pacotes `pip`
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Guia de Instalação e Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/Maihrendson/openf1-api.git
cd openf1-api
```

### 2. Configurar o Ambiente Virtual (Python)

Recomenda-se criar um ambiente virtual isolado para não misturar as dependências com o sistema global:

```bash
# Cria o ambiente virtual chamado 'venv'
python3 -m venv venv

# Ativa o ambiente virtual no Linux/macOS:
source venv/bin/activate

# Ou no Windows (PowerShell):
# .\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale os pacotes listados no `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Subir o MongoDB via Docker

O repositório já inclui um arquivo `docker-compose.yml` pré-configurado com MongoDB 7 e volume de dados persistente. Inicie o banco em segundo plano:

```bash
docker compose up -d
```

Para verificar se o contêiner está rodando e saudável:

```bash
docker compose ps
```

O contêiner estará acessível na porta padrão `27017`.

### 5. Configurar as Variáveis de Ambiente (`.env`)

Crie o arquivo `.env` a partir do modelo `.env.example`:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e ajuste as variáveis de acordo com a sessão de Fórmula 1 que deseja coletar. Exemplo:

```env
MONGO_URI=mongodb://localhost:27017/
API_BASE_URL=https://api.openf1.org/v1

# Exemplo: GP da Arábia Saudita 2024 (Jeddah - Corrida)
YEAR=2024
MEETING_KEY=1230
SESSION_KEY=9476
```

### 6. Executar o Coletor de Dados

Com o MongoDB em execução e o `.env` configurado, execute o script:

```bash
python api/datacollector.py
```

Exemplo de saída esperada no terminal:

```text
[INFO] 1 registros obtidos de 'sessions'.
[INFO] 1 registros processados na collection 'sessions'.
[INFO] 20 registros obtidos de 'drivers'.
[INFO] 20 registros processados na collection 'drivers'.
[INFO] 980 registros obtidos de 'laps'.
[INFO] 980 registros processados na collection 'laps'.
[SUCESSO] Coleta finalizada!
```

---

## 🔐 Variáveis de Ambiente

As configurações do projeto são gerenciadas centralizadamente pelo arquivo `.env`:

| Variável | Descrição | Exemplo Padrão |
| :--- | :--- | :--- |
| `MONGO_URI` | String de conexão para a instância do MongoDB | `mongodb://localhost:27017/` |
| `API_BASE_URL` | Endpoint base da API REST pública do OpenF1 | `https://api.openf1.org/v1` |
| `YEAR` | Ano da temporada da F1 desejada | `2024` ou `2023` |
| `MEETING_KEY` | Identificador do final de semana de corrida (*Grand Prix*) | `1230` (Jeddah 2024) ou `1219` (Monza 2023) |
| `SESSION_KEY` | Identificador específico da sessão (Corrida, Treino, etc.) | `9476` (Jeddah 2024) ou `9159` (Monza 2023) |

---

## 🔍 Como Obter as Chaves da OpenF1

A API OpenF1 é aberta e não requer chave de autenticação. Para consultar e descobrir novas chaves (`meeting_key` e `session_key`):

1. **Listar reuniões/GPs de um ano:**
   ```bash
   curl "https://api.openf1.org/v1/meetings?year=2024"
   ```
   Procure pelo campo `meeting_key` do evento desejado (ex: `1230` para Arábia Saudita).

2. **Listar as sessões de um GP específico:**
   ```bash
   curl "https://api.openf1.org/v1/sessions?meeting_key=1230"
   ```
   Identifique a sessão desejada pelo campo `session_name` (ex: `Race`, `Qualifying`, `Practice 1`) e copie o `session_key` correspondente.

Documentação oficial completa da API: [https://openf1.org](https://openf1.org).

---

## 🗄️ Estrutura e Modelagem no MongoDB

O script conecta-se à base de dados nomeada **`openf1_data_unipe`** e organiza as coleções da seguinte forma:

| Coleção | Chave(s) Única(s) no Upsert | Descrição |
| :--- | :--- | :--- |
| `sessions` | `session_key` | Armazena informações da sessão (circuito, país, datas e horários). |
| `drivers` | `session_key`, `driver_number` | Armazena dados dos pilotos participantes daquela sessão. |
| `laps` | `session_key`, `driver_number`, `lap_number` | Armazena os dados e tempos de cada volta realizada por piloto. |

> **Garantia de Idempotência:** A função `save_to_collection` utiliza `collection.update_one(query, {"$set": record}, upsert=True)`, atualizando o registro se ele já existir ou inserindo um novo caso contrário. Isso impede duplicação de dados ao executar o script múltiplas vezes.

---

## 🔎 Verificação e Consulta dos Dados

### Via Terminal (`mongosh`)

Você pode acessar o console do MongoDB diretamente dentro do contêiner Docker:

```bash
docker exec -it openf1-mongodb mongosh openf1_data_unipe
```

Dentro do prompt do `mongosh`, execute comandos como:

```javascript
// Exibir coleções disponíveis
show collections

// Contar número de documentos em cada coleção
db.sessions.countDocuments()
db.drivers.countDocuments()
db.laps.countDocuments()

// Consultar uma sessão
db.sessions.findOne()

// Ver os primeiros 3 pilotos
db.drivers.find().limit(3).pretty()

// Consultar as voltas mais rápidas registradas
db.laps.find({ lap_duration: { $ne: null } }).sort({ lap_duration: 1 }).limit(5)

// Sair do shell
exit
```

### Via Interfaces Gráficas (GUI)

Você também pode utilizar clientes visuais como **MongoDB Compass**, **DBeaver** ou a extensão oficial do **VS Code**:

- **URI de Conexão:** `mongodb://localhost:27017`
- **Database:** `openf1_data_unipe`

---

## 🧰 Comandos Úteis de Suporte

### Gerenciamento do Docker

```bash
# Iniciar o banco de dados em segundo plano
docker compose up -d

# Visualizar logs do MongoDB em tempo real
docker compose logs -f mongodb

# Parar os serviços mantendo os dados salvos
docker compose stop

# Remover contêineres mantendo o volume de dados
docker compose down

# ATENÇÃO: Remover contêineres E apagar o volume de dados do MongoDB
docker compose down -v
```

---


## 📄 Licença

Este projeto é desenvolvido para fins educacionais e de estudo sobre bancos de dados NoSQL e pipelines de dados. Os dados de Fórmula 1 são disponibilizados publicamente pela iniciativa OpenF1.
