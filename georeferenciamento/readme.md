# Georreferenciamento de UBS com MongoDB e GeoJSON

Este projeto é uma solução em Python para extrair, tratar e armazenar dados georreferenciados de fontes abertas do Governo Federal do Brasil (Unidades Básicas de Saúde - UBS). Os dados são processados, convertidos para o padrão **GeoJSON** e armazenados em um banco de dados **MongoDB** com suporte a índices geoespaciais (2dsphere).

## 🚀 Funcionalidades

* Leitura e tratamento de dados espaciais a partir de arquivos estruturados (CSV).

* Tratamento de dados e tipagem (conversão de strings para numéricos, tratamento de decimais no padrão brasileiro).

* Estruturação dos dados no formato GeoJSON (`Feature`, `Point`).

* Criação de índices geoespaciais (`GEOSPHERE`) no MongoDB.

* Consultas espaciais baseadas em proximidade utilizando o operador `$near` do MongoDB.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x

* **Banco de Dados:** MongoDB (Local ou Atlas)

* **Bibliotecas Python:**

  * `pandas`: Limpeza, filtragem e manipulação do conjunto de dados.

  * `pymongo`: Driver oficial para comunicação e persistência de dados no MongoDB.

  * `requests` / `geopandas`: (Disponíveis para expansões futuras envolvendo APIs e análises vetoriais avançadas).

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

* [Python 3.x](https://www.python.org/downloads/?utm_source=gemini)

* [MongoDB Community Server](https://www.mongodb.com/try/download/community?utm_source=gemini) rodando na porta padrão (`27017`) ou o MongoDB Compass para visualização.

Você também precisará baixar a base de dados das **Unidades Básicas de Saúde (UBS)** no portal [dados.gov.br](https://dados.gov.br?utm_source=gemini) em formato CSV.

## 🔧 Instalação e Configuração

1. **Clone o repositório ou crie a pasta do projeto:**
   Crie um ambiente virtual (recomendado) para isolar as dependências do projeto:

   ```
   python -m venv .venv
   
   ```

2. **Ative o ambiente virtual:**

   * No Windows (PowerShell):

     ```
     .\.venv\Scripts\Activate.ps1
     
     ```

   * No Linux/macOS:

     ```
     source .venv/bin/activate
     
     ```

3. **Instale as dependências:**

   ```
   pip install pandas pymongo geopandas requests
   
   ```

   *(Opcional: você pode salvar essas dependências em um arquivo rodando `pip freeze > requirements.txt`)*

4. **Prepare os dados:**
   Baixe o arquivo CSV do portal de dados abertos e salve-o na mesma pasta dos scripts com o nome `ubs.csv`.

## ⚙️ Como Executar

### 1. Carga e Tratamento dos Dados

Para ler o CSV, realizar a limpeza e salvar os registros no MongoDB usando o formato GeoJSON, execute:

```
python carga_ubs.py

```

O console exibirá a quantidade de registros que foram inseridos com sucesso no banco de dados.

### 2. Busca por Proximidade

Para testar o índice geoespacial do banco de dados e encontrar as unidades mais próximas de uma determinada coordenada (em um raio de 5 km, por exemplo), execute:

```
python busca_ubs.py

```

*Dica: Você pode editar o arquivo `busca_ubs.py` para colocar as coordenadas de latitude e longitude do seu bairro e testar os resultados na sua região.*

## 📁 Estrutura do Projeto

```
/
├── carga_ubs.py      # Script de tratamento e inserção dos dados no MongoDB
├── busca_ubs.py      # Script de consulta espacial de UBS por proximidade
├── ubs.csv           # Base de dados original (Ignorado no controle de versão)
├── .gitignore        # Arquivos ignorados pelo Git (ex: .venv, *.csv)
└── README.md         # Documentação atual

```