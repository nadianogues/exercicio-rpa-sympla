import pandas as pd

def ler_estruturar_arquivo_entrada(arquivo_populacao_capital, dados_estados):
    
    # Leitura do arquivo escel para dataframe
    df_arquivo = pd.read_excel(arquivo_populacao_capital)

    # Separação dos dados em colunas
    df_arquivo[['Capital', 'População']] = df_arquivo['Capital/populacao'].str.split(':', expand=True)

    # Exclui a coluna inicial (não será usada)
    df_arquivo = df_arquivo.drop('Capital/populacao', axis=1)

    # Manipulação da coluna Capital para letra maiusculas
    # Necessario para futura comparação entre dfs
    df_arquivo['Capital'] = df_arquivo['Capital'].str.upper()

    # Remover as duplicatas da coluna 'Estado', mantendo a primeira ocorrência
    df_arquivo = df_arquivo.drop_duplicates(subset='Capital', keep='first')

    # Dataframe com os dados da lista extraida do site
    df_estados = pd.DataFrame(dados_estados, columns=['Estado', 'Capital', 'Região'])

    # Unificação entre as dfs utilizando Capital como coluna em comum
    df_unificado = pd.merge(df_arquivo, df_estados, on='Capital', how='inner')
    df_unificado = df_unificado.reindex(columns=['Estado', 'Capital', 'Região', 'População'])
