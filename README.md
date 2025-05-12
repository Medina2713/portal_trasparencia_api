# Portal da Transparência - API

## Introdução
Este projeto tem como objetivo coletar, processar e armazenar dados dos beneficiários do programa Bolsa Família na cidade de Curitiba, utilizando a API pública do Portal da Transparência do Governo Federal.

O pipeline é composto por etapas de coleta, processamento e armazenamento dos dados em um banco de dados em uma instância PostgreSQL do Google Cloud, permitindo análises futuras e consultas aos dados históricos.

## Esquema de Arquivos
```

├── data/
│   └── raw/
│   └── temp/
└── scripts/
    ├── init.py
    ├── data_collection.py
    ├── data_processing.py
    ├── database.py
    └── temp_files.py
    ├── .env
├── config.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
```

## Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### Passos para instalação

1. Clone o repositório e vá para o diretório do projeto:
```shell
    git clone https://github.com/Medina2713/portal_trasparencia_api.git
    
```
Mudando para o diretorio do projeto
```shell
   cd .\portal_trasparencia_api\
```
 


2. Crie e ative um ambiente virtual (recomendado):
```shell
    python -m venv venv
```
Ative a venv
```shell
    source venv/bin/activate # Linux/Mac
    venv\Scripts\activate # Windows 
```


3. Instale as dependências:
```shell
     pip install -r requirements.txt
```

4. Crie uma cópia do arquivo .env.example:
```shell
     cp .env.example .env
```

5. Edite o arquivo .env com suas credenciais (API_KEY,DB_HOST,etc...) e configurações

6. Edite o arquivo config.py com os limites desejados

## Limites e Configurações

O projeto possui alguns limites configuráveis:

1. **Limite de páginas**: Definido em `config.py` como `PAGES_LIMIT`. Valor padrão: 3. Número máximo de paginas para considerar ao fazer a requisição dos endpoints.

2. **Município**: Filtro para Curitiba definido em `config.py` como `CITY_CODE`
3. **Período temporal**: Definido em `config.py` como `YEAR_RQST` e `MONTH_RQST`

Para alterar esses limites, edite o arquivo `config.py` com os valores desejados.


# Documentação das Funções

## data_collection.py

### `get_bf_withdrawals_by_city_api(year, month, city_code)`

**Descrição**:  
Função principal para coleta de dados da API do Bolsa Família por município.

**Parâmetros**:
- `year` (int): Ano da competência dos dados
- `month` (int): Mês inicial da competência (1-12)
- `city_code` (str): Código IBGE do município

**Fluxo**:
1. Prepara a pasta `data/raw`, limpando arquivos JSON existentes
2. Configura headers da API com a chave de autenticação
3. Itera pelos meses (do mês inicial até dezembro)
4. Para cada mês, faz requisições paginadas à API
5. Salva cada página como um arquivo JSON separado

**Decisões de implementação**:
- Limpeza da pasta raw antes de cada execução para evitar dados desatualizados
- Controle de paginação com `PAGES_LIMIT` para evitar loops infinitos
- Intervalo entre requisições (`API_RATE_LIMIT`) para respeitar limites da API
- Nomeação clara dos arquivos com padrão `Saques_BF_YYYY_MM_PAGE.json`

**Tratamento de erros**:
- Verificação de resposta vazia para encerrar paginação
- Try-catch para capturar erros de requisição
- Limite de páginas configurável para evitar excesso de requisições

## data_processing.py

### `process_data()`

**Descrição**:  
Processa os dados brutos coletados da API, normalizando a estrutura aninhada.

**Fluxo**:
1. Combina todos os arquivos JSON da pasta raw
2. Cria três DataFrames separados:
   - `df_municipio`: Dados do município
   - `df_beneficiario`: Dados dos beneficiários
   - `df_saque`: Dados dos saques

**Decisões de implementação**:
- Uso de `pd.json_normalize` para desaninhar estruturas JSON complexas
- Seleção explícita de colunas relevantes para cada entidade
- Renomeação de colunas para padrão snake_case
- Limpeza do CPF (remoção de caracteres não numéricos)
- Conversão de `valorSaque` para numérico com tratamento de erros

**Estrutura dos DataFrames**:
- `df_municipio`: Contém dados geográficos (IBGE, região, UF)
- `df_beneficiario`: Contém dados pessoais (NIS, CPF, nome)
- `df_saque`: Contém transações com chaves estrangeiras para as outras tabelas

## database.py

### `@contextmanager get_db_connection()`

**Descrição**:  
Gerenciador de contexto para conexões com o banco de dados PostgreSQL.

**Características**:
- Lê credenciais do arquivo .env
- Implementado como context manager para garantir fechamento da conexão
- Retorna a conexão estabelecida para uso em blocos with

**Tratamento de erros**:
- Captura `psycopg2.OperationalError` para problemas de conexão
- Garante fechamento da conexão no finally

### `test_db_conn()`

**Descrição**:  
Testa a conexão com o banco de dados e verifica tabelas existentes.

**Saídas**:
- Versão do PostgreSQL
- Lista de tabelas no schema public
- Status da conexão (True/False)

### `create_tables()`

**Descrição**:  
Cria as tabelas no banco de dados seguindo modelo relacional.

**Estrutura das tabelas**:
1. `municipio`: Dados geográficos (chave primária: codigo_ibge)
2. `beneficiario`: Dados pessoais (chave primária: nis)
3. `saque`: Transações com chaves estrangeiras

**Decisões de implementação**:
- Uso de `ON CONFLICT DO NOTHING` para evitar duplicatas
- Campos de timestamp para auditoria (created_at, updated_at)
- Tipos de dados apropriados para cada campo
- Relacionamentos via FOREIGN KEY

### `insert_data_on_db(df_municipio, df_beneficiario, df_saque)`


**Descrição**:  
Insere os dados processados nas tabelas do banco de dados.

**Fluxo**:
1. Insere municípios (ignora duplicatas)
2. Insere beneficiários (ignora duplicatas)
3. Insere saques (permite múltiplos saques por beneficiário)

**Otimizações**:
- Uso de transação única para todas as operações
- Commit apenas após todas as inserções
- Tratamento de conflitos com ON CONFLICT

### `truncate_db()`

**Descrição**:  
Remove todos os dados das tabelas do banco de dados.

**Características**:
- Identifica dinamicamente todas as tabelas no schema public
- Usa TRUNCATE com CASCADE para limpar tabelas relacionadas
- Transação segura com rollback em caso de erro

## temp_files.py

### `save_temp_data(df_municipio, df_beneficiario, df_saque)`


**Descrição**:  
Salva os DataFrames processados em arquivos Parquet temporários.

**Vantagens do Parquet**:
- Formato binário eficiente
- Preserva tipos de dados
- Compactação automática

### `load_temp_data()`

**Descrição**:  
Carrega os DataFrames dos arquivos Parquet temporários.

**Retorno**:  
Tupla com os três DataFrames (municipio, beneficiario, saque)

### `clear_temp_data()`


**Descrição**:  
Remove todos os arquivos temporários da pasta data/temp.

### `temp_data_exists()`


**Descrição**:  
Verifica se existem dados temporários salvos.

**Uso típico**:  
Checkpoint para continuar processamento após falhas

# Documentação do main.py

## Parte 1: Análise da Sintaxe e Decisões de Implementação

### Estrutura do ArgumentParser
parser = argparse.ArgumentParser(description="Pipeline de dados do Bolsa Família")

**Decisões de sintaxe**:
1. **Modularidade**: Uso de flags booleanas (`store_true`) para permitir combinação de operações
2. **Nomenclatura**: Nomes de argumentos intuitivos em português para facilitar o uso
3. **Descrições claras**: Help texts explicativos para cada operação

**Argumentos definidos**:
- `--coletar`: Ativa apenas a coleta de dados
- `--processar`: Ativa apenas o processamento
- `--banco`: Ativa apenas o carregamento no banco
- `--limpar`: Limpeza completa dos dados
- `--tudo`: Executa todo o pipeline (equivalente a --coletar --processar --banco)

### Fluxo de Controle Principal
if args.limpar:
# ...
elif args.coletar or args.tudo:
# ...


**Lógica implementada**:
1. **Precedência da limpeza**: Se --limpar for usado, executa apenas isso e sai
2. **Dependências implícitas**: --tudo ativa todas as etapas em sequência
3. **Verificação de pré-requisitos**: Checagem se dados temporários existem antes do carregamento

### Gerenciamento de Estado

-   save_temp_data(*dfs)
-   load_temp_data()
-   temp_data_exists()

**Estratégia adotada**:
1. **Armazenamento intermediário**: Uso de arquivos Parquet como checkpoint
2. **Verificação de integridade**: Checagem se todos DataFrames foram carregados
3. **Limpeza seletiva**: Dados temporários só são removidos após carga bem-sucedida quando não em --tudo

## Parte 2: Guia de Execução e Fluxo de Uso

### Argumentos e Modos de Operação

1. **Modo completo**:
```shell
    python main.py --tudo
```
- Executa todas as etapas sequencialmente
- Fluxo: Coleta → Processamento → Carga no banco
- Mantém arquivos temporários para debug

2. **Modo por etapas**:
```shell
python main.py --coletar --processar --banco
```
- Equivalente a --tudo, mas com controle explícito
- Permite inspeção intermediária entre etapas

3. **Modo individual**:
```shell
python main.py --coletar
```
- Apenas coleta dados da API
- Dados são salvos em `data/raw/`

4. **Limpeza**:
```shell
python main.py --limpar
```
- Apaga todas as tabelas do banco (TRUNCATE)
- Remove arquivos temporários
- Útil para reiniciar o pipeline do zero

### Fluxo de Execução Detalhado

1. **Coleta (--coletar)**:
   - Chama `get_bf_withdrawals_by_city_api`
   - Parâmetros fixos importados de config:
     - `YEAR_RQST`: Ano dos dados
     - `MONTH_RQST`: Mês inicial
     - `CITY_CODE`: Código IBGE do município

2. **Processamento (--processar)**:
   - Executa `process_data()`
   - Salva resultados em:
     - `data/temp/municipio.parquet`
     - `data/temp/beneficiario.parquet`
     - `data/temp/saque.parquet`

3. **Banco de dados (--banco)**:
   - Verifica existência dos arquivos temporários
   - Cria tabelas se não existirem (`create_tables()`)
   - Carrega dados (`insert_data_on_db()`)
   - Limpa temporários (exceto quando usando --tudo)

### Tratamento de Erros

1. **Falta de pré-requisitos**:
   - Se tentar --banco sem --processar primeiro, avisa usuário
   - Mensagem clara: "Execute --processar primeiro"

2. **Dados corrompidos**:
   - Verifica integridade dos DataFrames carregados
   - Se algum for None, sugere reprocessamento

3. **Gerenciamento de recursos**:
   - Limpeza explícita necessária para evitar acumulação
   - Arquivos raw não são apagados automaticamente

### Exemplos de Uso Avançado

1. **Coleta + Processamento sem carga**:
```shell
python main.py --coletar --processar
```
- Útil para desenvolvimento/teste

2. **Reprocessamento completo**:
```shell
python main.py --limpar && python main.py --tudo
```
- Garante ambiente limpo antes da execução

3. **Atualização incremental**:
```shell
python main.py --processar --banco
```
- Reutiliza dados já coletados
- Útil quando só o processamento mudou

## Próximas Melhorias

1. Fazer o INSERT de dados por batches (Performance)
2. Implementar agendamento automático de coletas periódicas 
3. Adicionar suporte a Docker para facilitar a implantação 
4. Adicionar suporte a outros municípios além de Curitiba 
5. Desenvolver uma interface simples para consulta aos dados 
6. Criar testes automatizados para as funções principais 
7. Implementar logging detalhado para monitoramento 







