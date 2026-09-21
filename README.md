# Financial Data Pipeline

## Sobre o Projeto

Este projeto é uma Pipeline de Dados Financeiros (End-to-End) projetada para extrair informações de uma API financeira, processá-las e disponibilizá-las para análise de negócios. O objetivo é demonstrar proficiência em Engenharia de Dados através de um fluxo estruturado, robusto e escalável.

A pipeline realiza a extração dos dados brutos, aplica transformações e regras de qualidade, armazena os dados de forma estruturada em um banco de dados relacional e, por fim, consome esses dados através de views otimizadas em um dashboard interativo no Power BI.

## Arquitetura e Fluxo de Dados

O pipeline segue o padrão ETL (Extract, Transform, Load):

1. **Extraction**: Consome dados de uma API financeira e salva o JSON original na camada `data/raw/` para histórico.
2. **Transformation**: Limpa os dados, formata tipos e cria novas métricas necessárias para a análise de negócios.
3. **Validation**: Valida a qualidade dos dados (ex: checagem de nulos, consistência de valores) antes da ingestão.
4. **Load**: Grava os dados tratados e validados em tabelas no PostgreSQL.
5. **Analytics & BI**: Executa scripts SQL para criar Views analíticas no banco de dados. O Power BI conecta-se diretamente a essas views para renderizar os gráficos de acompanhamento.

## Tecnologias Utilizadas

- **Linguagem**: Python (requests, manipulação de dados, etc.)
- **Banco de Dados**: PostgreSQL (Tabelas e Views analíticas)
- **Infraestrutura**: Docker & Docker Compose (para orquestrar o banco de dados localmente)
- **Visualização (BI)**: Power BI
- **Boas Práticas**: Logging centralizado, testes automatizados (Pytest), variáveis de ambiente (.env)

## Estrutura do Repositório

financial-data-pipeline/
│
├── src/
│ ├── pipeline/
│ │ ├── init.py
│ │ ├── extraction.py # Lógica de consumo da API e salvamento raw
│ │ ├── transformation.py # Limpeza e formatação de dados
│ │ ├── validation.py # Testes de qualidade dos dados (Data Quality)
│ │ └── database.py # Conexão e ingestão no PostgreSQL
│ │
│ ├── config.py # Gestão de credenciais (via .env) e endpoints
│ ├── logger.py # Setup centralizado de logs da aplicação
│ └── main.py # Orquestrador do pipeline (Extract -> Transform -> Validate -> Load)
│
├── tests/
│ ├── test_transformation.py # Testes unitários de transformação
│ └── test_validation.py # Testes unitários de validação de qualidade
│
├── data/
│ └── raw/ # Armazenamento local dos arquivos JSON brutos
│
├── sql/
│ ├── schema.sql # DDL (Criação das tabelas)
│ └── analysis.sql # DDL (Criação das Views analíticas para o Power BI)
│
├── dashboard/ # Arquivo .pbix do Power BI e imagens do dashboard
│
├── docker-compose.yml # Configuração do contêiner PostgreSQL
├── requirements.txt # Dependências do projeto Python
├── .gitignore # Arquivos ignorados pelo Git (ex: .env, pycache, venv)
└── README.md


## Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python 3.10+, o Docker e o Git instalados em sua máquina.

### Passo a Passo

1. Clone este repositório:

```bash
git clone https://github.com/SEU_USUARIO/financial-data-pipeline.git
cd financial-data-pipeline
```

2. Configure as variáveis de ambiente:

Crie um arquivo chamado `.env` na raiz do projeto e insira suas credenciais do banco de dados e a chave da API (se houver).

3. Suba a infraestrutura (PostgreSQL):

```bash
docker-compose up -d
```

4. Instale as dependências do Python:

Recomenda-se o uso de um ambiente virtual (venv).

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

5. Crie as tabelas e views no Banco de Dados:

Execute os scripts da pasta `sql/` no seu SGBD preferido ou via linha de comando para preparar o banco de dados.

6. Execute o Pipeline:

```bash
python src/main.py
```

Você poderá acompanhar o status do processamento através dos logs exibidos no console ou gravados em arquivo.

7. Visualização:

Abra o arquivo localizado na pasta `dashboard/` com o Power BI Desktop, atualize as credenciais do banco de dados (se necessário) e recarregue os dados para visualizar o dashboard operando nas views do PostgreSQL.

## Dashboard em Power BI

Os dados transformados pelo Python e armazenados no PostgreSQL são consumidos pelo Power BI através de Views (`sql/analysis.sql`). A utilização de views permite que o Power BI importe apenas os dados estritamente necessários, já agregados e pré-calculados, garantindo alta performance e governança na camada de dados.
