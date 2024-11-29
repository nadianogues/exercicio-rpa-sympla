import pandas as pd
import logging as log

def ler_estruturar_arquivo_entrada(arquivo_populacao_capital, dados_estados):
    
    log.info("Inicio da função de ler e estruturar o arquivo de entrada")
    
    # Leitura do arquivo excel para dataframe
    log.info("Leitura do arquivo excel PopulaçãoxCapital.xlsx")
    df_arquivo = pd.read_excel(arquivo_populacao_capital)

    # Separação dos dados em colunas
    df_arquivo[['Capital', 'População']] = df_arquivo['Capital/populacao'].str.split(':', expand=True)

    # Exclui a coluna inicial (não será usada)
    df_arquivo = df_arquivo.drop('Capital/populacao', axis=1)

    # Manipulação da coluna Capital para letra maiusculas
    # Necessário para futura comparação entre dfs
    df_arquivo['Capital'] = df_arquivo['Capital'].str.upper()

    # Remove as linhas duplicadas da coluna 'Capital', mantendo a primeira ocorrência
    df_arquivo = df_arquivo.drop_duplicates(subset='Capital', keep='first')
    
    log.info("Fim da leitura e manipulação do arquivo de entrada")

    # Dataframe com os dados da lista extraída do site
    log.info("Transformando a lista de dados do estado em um data frame")
    df_estados = pd.DataFrame(dados_estados, columns=['Estado', 'Capital', 'Região'])

    # Unificação entre as dfs utilizando Capital como coluna em comum
    log.info("Unindo os data frames para obter todas as informações dos estados")
    df_unificado = pd.merge(df_arquivo, df_estados, on='Capital', how='inner')
    df_unificado = df_unificado.reindex(columns=['Estado', 'Capital', 'Região', 'População'])
    
    log.info(f"df unificado: \n{df_unificado}")
    
    log.info("Fim da função de ler e estruturar o arquivo de entrada")
    
