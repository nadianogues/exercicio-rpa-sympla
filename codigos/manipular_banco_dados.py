import os
import sqlite3
import pandas as pd
import xlwings as xw

def criar_inserir_banco_dados(pasta_bd, df_unificado):
    """
    Cria, conecta e insere os dados no banco de dados a partir
    do Data Frame fornecido no parâmetro.
    
    Args:
    pasta_bd (str): Caminho da pasta para salvar o banco de dados.
    df_unificado (DataFrame): Data frame com as informações do site
    e planilha de entrada.

    Returns:
    conexao (Connection): Conexão para manipulação de dados no SQL.
    """
    
    caminho_bd = os.path.join(pasta_bd, 'estados.db')

    # Conectar ao banco de dados SQLite (será criado se não existir)
    conexao = sqlite3.connect(caminho_bd)
    cursor = conexao.cursor()

    # Criar a tabela 'estados' se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS estados (
        estado TEXT PRIMARY KEY,
        capital TEXT,
        regiao TEXT,
        populacao INTEGER
    )
    ''')

    # Inserir ou atualizar os dados no banco de dados
    for _, row in df_unificado.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO estados (estado, capital, regiao, populacao)
        VALUES (?, ?, ?, ?)
        ''', (row['Estado'], row['Capital'], row['Região'], row['População']))
        
    
    # Salva as alterações
    conexao.commit()
        
    return conexao

def consultar_salvar_dados(conexao, pasta_resultados):
    """
    Faz as três consultas no banco de dados, identificando:
        - As 3 regiões mais populosas.
        - As regiões e quantidade de capitais.
        - Os 2 estados com as capitais mais populosas.
    E salva os arquivos com o seguinte nome:
        - top3_regioes_populosas.csv.
        - regioes_n_capitais.xls
        - estados_mais_populosos.xls
        
    Args:
    conexao (Connection): Conexão para manipulação de dados no SQL.
    pasta_resultados (str): Caminho da pasta para salvar os resultados
    das consultas.    
    """

    # Consulta as 3 regiões mais populosas
    query_regioes_populosas = '''
    SELECT regiao, SUM(populacao) AS populacao_total
    FROM estados
    GROUP BY regiao
    ORDER BY populacao_total DESC
    LIMIT 3;
    '''

    # Define nome do arquivo e caminho
    arquivo_regioes_populosas = os.path.join(pasta_resultados, 'top3_regioes_populosas.csv')

    # Executa consulta e exporta para CSV
    df_regioes_populosas = pd.read_sql_query(query_regioes_populosas, conexao)
    df_regioes_populosas.to_csv(arquivo_regioes_populosas, index=False)

    # Consulta regiões e quantidade de capitais
    query_regioes_n_capitais = '''
    SELECT regiao, COUNT(DISTINCT capital) AS quantidade_capitais
    FROM estados
    GROUP BY regiao;
    '''

    # Define nome do arquivo e caminho
    arquivo_regioes_n_capitais = os.path.join(pasta_resultados, 'regioes_n_capitais.xls')

    # Executa consulta e exporta para XLS
    df_regioes_n_capitais = pd.read_sql_query(query_regioes_n_capitais, conexao)
    
    # Abre uma nova instância do Excel
    with xw.App(visible=False) as app:
        # Cria um novo arquivo de excel
        arq_excel = app.books.add()
        
        # Adiciona uma planilha e define os nomes das colunas
        planilha = arq_excel.sheets[0]
        planilha.range('A1').value = list(df_regioes_n_capitais.columns)
        
        # Escreve o DataFrame na planilha
        planilha.range('A2').value = df_regioes_n_capitais.values.tolist()
        
        # Salva o arquivo no formato .xls
        arq_excel.save(arquivo_regioes_n_capitais)

    # Consulta os 2 estados com as capitais mais populosas
    query_estados_mais_populosos = '''
    SELECT estado, capital, populacao
    FROM estados
    ORDER BY populacao DESC
    LIMIT 2;
    '''

    # Define nome do arquivo e caminho
    arquivo_estados_mais_populosos = os.path.join(pasta_resultados, 'estados_mais_populosos.xls')

    # Executa consulta e exportar para XLS
    df_estados_mais_populosos = pd.read_sql_query(query_estados_mais_populosos, conexao)
    
    with xw.App(visible=False) as app:
        # Criar um novo arquivo de excel
        arq_excel = app.books.add()
        
        # Adiciona uma planilha e define os nomes das colunas
        planilha = arq_excel.sheets[0]
        planilha.range('A1').value = list(df_estados_mais_populosos.columns)
        
        # Escreve o DataFrame na planilha
        planilha.range('A2').value = df_estados_mais_populosos.values.tolist()
        
        # Salva o arquivo no formato .xls
        arq_excel.save(arquivo_estados_mais_populosos)

    # Fecha a conexão
    conexao.close()
    