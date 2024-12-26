import os
import shutil

import re
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Vai de corretora em corretora

Corretora1 = "https://www.portaldoconsignado.com.br/home?9" 
# Pega variaveis de login de ambiente do sistema 
try:
    UsernameValues = os.getenv("Username_Values")
    PasswordValues = os.getenv("Password_Values")   
except Exception as e:
    print("Não foi possível achar os valores")

try:
    servico = EdgeService(EdgeChromiumDriverManager().install())
    nav = webdriver.Edge(service=servico)
except:
   
    servico = Service(ChromeDriverManager().install())
    options = Options()
    nav = webdriver.Chrome()

# Caminho da pasta "Relatórios"
caminho_Relatorios = r"C:\Users\FelipeApolinárioPere\Downloads\Relatorios"
 
# Lista para armazenar pastas com mais de 1 arquivo
pastas_com_mais_de_um_arquivo = []
 
# Listar conteúdo da pasta "CCBS"
conteudo_relatorios = os.listdir(caminho_Relatorios)

# Faz login no site
nav.get(Corretora1)
    
    

  
time.sleep(30)


    # Switch frame by id
EdgeService.switch_to.frame('txtCPF')

    # Now, Click on the button
EdgeService.find_element(By.ID_NAME, 'txtCPF').insert(UsernameValues)
  
#Erro
#Exception has occurred: AttributeError
#type object 'Service' has no attribute 'find_element'
# File "C:\Automatização_Script\Script.py", line 52, in <module>
#  iframe = EdgeService.find_element(By.CSS_SELECTOR, "#modal > iframe")
#          ^^^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: type object 'Service' has no attribute 'find_element'
 