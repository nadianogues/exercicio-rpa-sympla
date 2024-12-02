import os
import logging as log
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from extrair_informacoes_estados import acessar_extrair_dados
from ler_estruturar_arquivo import ler_estruturar_arquivo_entrada
from manipular_banco_dados import criar_inserir_banco_dados, consultar_salvar_dados

def main():
    """
    Função principal que organiza o fluxo de execução do robô.
    """
    # Variáveis 
    url_estados_brasileiros = "https://inanyplace.blogspot.com/2017/01/lista-de-estados-brasileiros-sigla-estado-capital-e-regiao.html"

    # Manipulação dos diretorios para organização dos arquivos
    diretorio_atual = os.path.realpath('__file__')
    diretorio_atual = os.path.dirname(diretorio_atual)
    diretorio_atual = os.path.dirname(diretorio_atual)

    pasta_log = os.path.join(diretorio_atual,"logs")
    pasta_resultados = os.path.join(diretorio_atual,"resultados")
    pasta_bd = os.path.join(diretorio_atual,"banco de dados")
    pasta_arquivo = os.path.join(diretorio_atual,"arquivo")

    # Cria o diretório 'logs' se não existir
    if not os.path.exists(pasta_log):
        os.makedirs(pasta_log)

    # Cria o diretório 'resultados' se não existir
        if not os.path.exists(pasta_resultados):
            os.makedirs(pasta_resultados)
            
    # Cria o diretório 'banco de dados' se não existir
        if not os.path.exists(pasta_bd):
            os.makedirs(pasta_bd)
            
    # Configura o log
    configurar_log(pasta_log)
    
    log.info("Início da automação")
    
    # Configura o WebDriver
    driver = inicializar_driver()

    try:
        # Acessa a página e extrai os dados
        dados_estados = acessar_extrair_dados(
            driver, url_estados_brasileiros
        )
        
        # Le e estrutura o arquivo de entrada
        df_unificado = ler_estruturar_arquivo_entrada(
            pasta_arquivo, dados_estados
        )
        
        # Manipula o banco de dados
        # Cria e insere dados no bd
        conexao = criar_inserir_banco_dados(pasta_bd, df_unificado)
        
        # Consulta no banco de dados e salva os dados
        consultar_salvar_dados(conexao, pasta_resultados)
        
        log.info("Finalizou com sucesso")
        
    except ValueError as e:
        log.error(f"Impossível prosseguir, automação parou!")
        
    finally:
        # Fecha o WebDriver
        fechar_driver(driver)
        log.info("Fim da automação")

def configurar_log(pasta_log):
    '''
    Configuração incial do log
    
    Args:
    pasta_log (str): Caminho da pasta para os logs
    '''
    
    try:
        # Cria o diretório 'logs' se não existir
        if not os.path.exists(pasta_log):
            os.makedirs(pasta_log)

        # Gera o nome do arquivo de log com a data e hora atual
        data_atual = datetime.now().strftime('%Y%m%d%H%M%S')  # Formato: '20241127151811'
        arquivo_log = os.path.join(pasta_log, f'log_{data_atual}.log')  # Nome do log: log_20241127151811.log

        # Configura o logging
        log.basicConfig(
            level=log.INFO,  # Define o nível mínimo de log
            format='%(asctime)s - %(levelname)s - Linha: %(lineno)d - %(funcName)s - %(message)s',  # Formato do log
            handlers=[
                log.FileHandler(arquivo_log),  # Grava os logs no arquivo com data no nome
                log.StreamHandler()  # Exibe os logs no console também
            ],
            datefmt='%Y-%m-%d %H:%M'  # Formato da data e hora sem segundos
        )
    except Exception as e:
        log.error(f"Erro ao configurar o log: {e}")
        
    
def inicializar_driver():
    """
    Função para iniciar corretamente o Webdriver.
    """
    
    # Definir opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')  # Desabilita a aceleração de hardware

    # Inicializa o WebDriver
    log.info("Iniciando o WebDriver")
    
    try:
        driver = webdriver.Chrome()
        return driver
    except Exception as e:
        log.error(f"Erro ao inicializar o WebDriver: {e}")


def fechar_driver(driver):
    """
    Função para fechar corretamente o Webdriver.
    
    driver (Webdriver): Instância do Webdriver.
    """
    
    # Fecha o WebDriver
    log.info("Fechando o Webdriver")
    
    try:
        driver.quit()
        log.info("Webdriver fechado com sucesso.")
        
    except Exception as e:
        log.error(f"Erro ao fechar o Webdriver: {e}")


# Executa a função principal
if __name__ == "__main__":
    main()