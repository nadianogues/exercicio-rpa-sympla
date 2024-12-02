import logging as log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def acessar_extrair_dados(driver, url_estados_brasileiros):
    """
    Acessa a página, extrai e organiza os dados de estados, capitais e regiões.
    
    Args:
    driver (WebDriver): Instância do WebDriver.
    url_estados_brasileiros (str): URL dos estados brasileiros.

    Returns:
    dados_estados (list): Lista com os dados de estados, capitais e regiões.
    """
    
    try:
        log.info("Acessando site com os estados brasileiros")
        driver.get(url_estados_brasileiros)

        try:
            # Aguarda até que a tabela esteja presente na página
            log.info("Aguardando a tabela com os estados ser carregada")
            WebDriverWait(url_estados_brasileiros, 120).until(
                EC.visibility_of(driver.find_element(
                    By.XPATH, '//*[@id="post-body-161801306241062754"]/blockquote/div[2]/table')
                )
            )
        except Exception as e:
            log.error(f"Erro ao acessar a tabela na página {e}")
            raise ValueError()

        # Localiza a tabela com os dados dos estados
        log.info("Extraindo as informações da tabela")
        tabela = driver.find_element(
            By.XPATH, '//*[@id="post-body-161801306241062754"]/blockquote/div[2]/table'
        )

        # Localiza todas as linhas da tabela
        linhas = tabela.find_elements(By.TAG_NAME, "tr")

        # Lista para armazenar os dados extraídos dos estados
        dados_estados = []

        # Itera sobre as linhas da tabela, menos cabeçalho
        for linha in linhas[1:]:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            
            estado = colunas[1].text.strip()  # Nome do estado
            capital = colunas[2].text.strip() # Capital
            regiao = colunas[3].text.strip()  # Região
            
            dados_estados.append((estado, capital, regiao))
                
        quant_estados = len(dados_estados)
    
        if quant_estados != 26:
            log.error(f"Erro: Esperado 26 estados, mas foram extraídos {quant_estados}.")
            raise ValueError()
        
        log.info("Dados extraidos da tabela: ")
        log.info("Nome do estado - Capital - Região")
        log.info(f"\n{dados_estados}")
                
        return dados_estados
    
    except Exception as e:
        log.error(f"Erro ao extrair dados: {e}")
        raise ValueError()
