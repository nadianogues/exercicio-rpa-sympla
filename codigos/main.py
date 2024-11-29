import os
import logging as log
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from extrair_informacoes_estados import acessar_extrair_dados
from ler_estruturar_arquivo import ler_estruturar_arquivo_entrada

def main():
    """
    Função principal que organiza o fluxo de execução do robô.
    """
    # Variaveis 
    url_estados_brasileiros = "https://inanyplace.blogspot.com/2017/01/lista-de-estados-brasileiros-sigla-estado-capital-e-regiao.html"
    arquivo_populacao_capital = r'C:\Users\Nadia Nogues\Documents\2024\sympla\exercicio-rpa-sympla\arquivo\PopulaçãoxCapital.xlsx'

    # Manipulação dos diretorios para organização dos arquivos
    diretorio_atual = os.path.realpath('__file__')
    diretorio_atual = os.path.dirname(diretorio_atual)
    diretorio_atual = os.path.dirname(diretorio_atual)

    pasta_log = os.path.join(diretorio_atual,"logs")
    pasta_resultados = os.path.join(diretorio_atual,"resultados")
    pasta_bd = os.path.join(diretorio_atual,"banco de dados")

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
    configurar_log()
    
    log.info("Inicio da automação")
    
    # Configura o WebDriver
    driver = inicializar_driver()

    try:
        # Acessa a página e extrai os dados
        dados_estados = acessar_extrair_dados(
            driver, url_estados_brasileiros
        )
        
        # Le e estrutura o arquivo de entrada
        ler_estruturar_arquivo_entrada(
            arquivo_populacao_capital, dados_estados
        )
        
    finally:
        # Fecha o WebDriver
        fechar_driver(driver)
        log.info("Fim da automação")

def configurar_log():
    '''
    Configuração incial do log
    '''
    
    try:
        # Cria o diretório 'logs' se não existir
        pasta_log = os.path.join(os.path.dirname(os.path.realpath('__file__')),"logs")
        if not os.path.exists(pasta_log):
            os.makedirs(pasta_log)

        # Gera o nome do arquivo de log com a data e hora atual
        data_atual = datetime.now().strftime('%Y%m%d%H%M%S')  # Formato: '20241127151811'
        arquivo_log = os.path.join(pasta_log, f'log_{data_atual}.log')  # Nome do log: log_20241127151811.log

        # Configura o logging
        log.basicConfig(
            level=log.INFO,  # Define o nível mínimo de log
            format='%(asctime)s - %(levelname)s - %(message)s',  # Formato do log
            handlers=[
                log.FileHandler(arquivo_log),  # Grava os logs no arquivo com data no nome
                log.StreamHandler()  # Exibe os logs no console também
            ]
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