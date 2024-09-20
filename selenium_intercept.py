from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import io
import gzip
import os

service = Service()

driver = webdriver.Chrome(service=service)

driver.get('https://opcoes.net.br/login')

username_field = driver.find_element(By.ID, 'CPF')
username_field.send_keys(os.getenv("CPF"))

password_field = driver.find_element(By.ID, 'Password')
password_field.send_keys(os.getenv("PASSWORD"))

login_button = driver.find_element(By.CLASS_NAME, 'btn-default')
login_button.click()

try:
    WebDriverWait(driver, 10).until(EC.url_changes('https://opcoes.net.br/login'))
    
    driver.get('https://opcoes.net.br/historico/volatilidade-implicita')
    
    print("Navegou para a página de volatilidade implícita com sucesso!")

    WebDriverWait(driver, 10).until(lambda d: any(
        req.url == 'https://opcoes.net.br/opcoes/dados/tabelaegrafico/volatilidade?idAcao=ABEV3&dataInicial=2023-09-19&dataFinal=2024-09-19&dateTimeGroupOption=Date'
        for req in d.requests
    ))

    for request in driver.requests:
        if request.url == 'https://opcoes.net.br/opcoes/dados/tabelaegrafico/volatilidade?idAcao=ABEV3&dataInicial=2023-09-19&dataFinal=2024-09-19&dateTimeGroupOption=Date' and request.response:
            response_body = request.response.body.decode('utf-8', errors='ignore')

            with gzip.GzipFile(fileobj=io.BytesIO(request.response.body)) as f:
                dados_descomprimidos = f.read()
            
            decodeData = dados_descomprimidos.decode('utf-8')

            jsonData = json.loads(decodeData)
                    
            print("Resposta JSON recebida")
            break

except Exception as e:
    print(f"Ocorreu um erro: {e}")

if 'https://opcoes.net.br/historico/volatilidade-implicita' in driver.current_url:
    print("Acesso à página de volatilidade implícita com sucesso!")
else:
    print("Falha ao acessar a página de volatilidade implícita.")

driver.quit()
