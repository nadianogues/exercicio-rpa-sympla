import pandas as pd
import logging as log

def ler_estruturar_arquivo_entrada(arquivo_populacao_capital, dados_estados):
    """
    Leitura e etruturação do arquivo de entrada e união das informações 
    obtidas no site em um data frame.
    
    Args:
    arquivo_populacao_capital (str): Arquivo de entrada.
    dados_estados (list): Lista com os dados do site de 'Estado', 'Capital', 
    e 'Região' 

    Returns:
    df_unificado (DataFrame): Data frame com as informações do site e 
    planilha de entrada.
    """
   
    log.info("Início da função de ler e estruturar o arquivo de entrada")
    
    try:
        
        try:
            # Leitura do arquivo excel para dataframe
            log.info("Leitura do arquivo excel PopulaçãoxCapital.xlsx")
            df_arquivo = pd.read_excel(arquivo_populacao_capital)
        except FileNotFoundError as e:
            log.error(f"Erro: O arquivo não foi encontrado! Caminho fornecido: {arquivo_populacao_capital}")
            raise ValueError()           
        
        # Leitura do arquivo escel para dataframe
        df_arquivo = pd.read_excel(arquivo_populacao_capital)

        # Separação dos dados em colunas
        df_arquivo[['Capital', 'População']] = df_arquivo['Capital/populacao'].str.split(':', expand=True)

        # Exclui a coluna inicial (não será usada)
        df_arquivo = df_arquivo.drop('Capital/populacao', axis=1)

        # Manipulação da coluna Capital para letra maiusculas
        # Necessario para futura comparação entre dfs
        df_arquivo['Capital'] = df_arquivo['Capital'].str.upper()

        #verificação de quantidade de estados
        quant_estados = len(df_arquivo)

        if quant_estados != 26:
            log.warning(f"Esperado 26 estados, mas foram extraídos {quant_estados}. Possíveis dados duplicados.")

        # Verificar se há linhas duplicadas na coluna 'Capital'
        duplicadas_capital = df_arquivo['Capital'].duplicated().any()

        if duplicadas_capital == True:
            log.info("Dados duplicados de Capitais. Necessário tratamento.")
            # Remover as duplicatas da coluna 'Estado', mantendo a primeira ocorrência
            df_arquivo = df_arquivo.drop_duplicates(subset='Capital', keep='first')

            # Dataframe com os dados da lista extraida do site
            log.info("Transformando a lista de dados do estado em um data frame")
            df_estados = pd.DataFrame(dados_estados, columns=['Estado', 'Capital', 'Região'])

            # Unificação entre as dfs utilizando Capital como coluna em comum
            log.info("Unindo os data frames para obter todas as informações dos estados")
            df_unificado = pd.merge(df_arquivo, df_estados, on='Capital', how='inner')
            df_unificado = df_unificado.reindex(columns=['Estado', 'Capital', 'Região', 'População'])
            
            log.info(f"df unificado: \n{df_unificado}")

            log.info("Fim da função de ler e estruturar o arquivo de entrada")

            return df_unificado
        else:
            log.error(f"Erro: Esperado 26 estados, mas foram encontrados {quant_estados}.")
            raise ValueError()
         
    except Exception as e:
        log.error(f"Erro na função ler_estruturar_arquivo {e}")
        raise ValueError()