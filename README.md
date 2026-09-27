# Implementação e Gerenciamento de Bancos de Dados NoSQL

Repositório desenvolvido para a disciplina de Implementação e Gerenciamento de Bancos de Dados NoSQL, do Prof. Ricardo Roberto. Reúne aplicações que exploram coleta, transformação, armazenamento e consulta de dados usando bancos NoSQL, com foco em MongoDB e dados geoespaciais.

## Integrantes

- Maihrendson Cauã de Carvalho Cassiano
- Lucas Espindola Rodrigues

## Relatório geral das aplicações

### Cartola FC

Coleta os dados públicos do mercado de atletas do Cartola FC, transforma as informações recebidas pela API e as armazena no MongoDB para consultas e análises posteriores. O fluxo é implementado em Python como um processo ETL.

Documentação e execução: [cartola-api/README.md](cartola-api/README.md).

### GeoLog

Aplicação de monitoramento logístico que combina dados cadastrais e transacionais em SQLite com telemetria de veículos em MongoDB. Oferece mapa de frota, indicadores e gráficos analíticos, busca geoespacial e simulação de dados IoT, usando Streamlit, Folium e Plotly.

Documentação e execução: [geolog/README.md](geolog/README.md).

### Georreferenciamento de UBS

Processa dados de Unidades Básicas de Saúde a partir de CSV, converte coordenadas para GeoJSON e armazena os registros no MongoDB. Índices geoespaciais permitem consultar unidades próximas a uma localização.

Documentação e execução: [georeferenciamento/readme.md](georeferenciamento/readme.md).

### OpenF1

Coleta dados da API pública OpenF1 sobre sessões, pilotos e voltas de eventos de Fórmula 1. O pipeline em Python persiste os resultados no MongoDB e usa operações de upsert para evitar duplicações entre execuções.

Documentação e execução: [openf1-api/README.md](openf1-api/README.md).

## Visão geral

Em conjunto, os projetos aplicam conceitos de persistência de documentos, pipelines ETL, integração de fontes de dados e consultas geoespaciais. Cartola FC e OpenF1 trabalham com dados obtidos de APIs públicas; o projeto de UBS explora dados geográficos; e o GeoLog demonstra persistência poliglota, combinando bancos relacionais e NoSQL em uma aplicação analítica.
