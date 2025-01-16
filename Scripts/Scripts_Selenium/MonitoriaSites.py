import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import date, timedelta, datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Define as variáveis do Selenium
options = webdriver.EdgeOptions()
driver = webdriver.ChromiumEdge

#Define Variáveis de sites que serão baixados relatórios para monitoração
Leadpage = "https://backoffice-spa.appmeucashcard.com/"
S3 = "https://us-east-2.console.aws.amazon.com/s3/buckets/endorsement-monitoring?region=us-east-2&bucketType=general&tab=objects"
Mcc_Site = "https://www.meucashcard.com.br/"

#Define valores de variáveis de conexão
try:
    LeadpageUser = os.getenv("BackOffice_User")
    LeadpagePsw = os.getenv("BackOffice_Psw")
    if not all ([LeadpageUser, LeadpagePsw]):
        raise ValueError("Coloque as variáveis da leadpage no ambiente")   
except Exception as e:
    print(f"Erro {e}")

#Cria função Para verificação de dados no ambiente do sistema
def TesteVariaveis():
    print(LeadpageUser)
    print(LeadpagePsw)

def MonitoraLeadPage():
    driver.get(Leadpage)
    LeadPage_User = driver.find_element(By.XPATH, "/html/body/app-root/app-layout/app-login/app-sign-in/div/div/div/div/div/div/div/div[2]/form/mat-form-field[1]/div/div[1]/div[3]/input")
    LeadPage_User.send_keys(LeadpageUser)
    LeadPage_Psw = driver.find_element(By.XPATH, "/html/body/app-root/app-layout/app-login/app-sign-in/div/div/div/div/div/div/div/div[2]/form/mat-form-field[1]/div/div[1]/div[3]/input")
    LeadPage_Psw.send_keys(LeadpagePsw)
    driver.find_element(By.XPATH, "/html/body/app-root/app-layout/app-login/app-sign-in/div/div/div/div/div/div/div/div[2]/form/div[2]/button").click()
    time.sleep(2)

    #Seleciona a parte de relatórios
    driver.find_element(By.XPATH, "/html/body/app-root/app-layout/div/div[1]/div/sidebar-cmp/div[2]/ul/li[8]/a").click()

    #Seleciona a parte de Operacional 
    driver.find_element(By.XPATH, "/html/body/app-root/app-layout/div/div[1]/div/sidebar-cmp/div[2]/ul/li[9]/div/ul/li[2]/a").click()

    #Seleciona a opção de Leadpage
    driver.find_element(By.XPATH, "/html/body/app-root/app-layout/div/div[1]/div/sidebar-cmp/div[2]/ul/li[9]/div/ul/li[2]/div/ul/li[4]/a").click()

    time.sleep(3)

    #Seleciona a opção de download relatório Leadpage
    driver.find_element(By.XPATH, "/html/body/app-root/app-layout/div/div[2]/app-reports/app-potential-lead/div/div/div/div/div/app-table/div/div/div[1]/div[2]/div/img").click()


#Chama a função de monitoria da Leadpage
MonitoraLeadPage()