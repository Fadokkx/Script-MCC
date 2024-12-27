import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Define a variáveis dos sites das corretoras

#Zetra
Corr_EMBU = "https://portal.econsig.com.br/embudasartes/v3/autenticarUsuario?t=20241226140450#no-back"
Corr_IGEPREV = "https://portal.econsig.com.br/igeprev/v3/autenticarUsuario#no-back"
Corr_PrefSBC ="https://www.econsig.com.br/sbc/v3/autenticarUsuario?t=20190520100728#no-back"
Corr_Pref_Serra_ES = "https://www.econsig.com.br/serra"
Corr_PrefUberlandia = "https://www.econsig.com.br/uberlandia"
"""
Achar erro na corretora do Paraná (Conexão não particular)
Corr_Parana = "https://www.prconsig.seap.pr.gov.br/pr/v3/autenticarUsuario?t=20221012152301#no-back"

"""
Corr_PrefCuritiba = "https://www2.econsig.com.br/curitiba/v3/autenticarUsuario?t=20230904104333#no-back"
Corr_HospDoServPubSP = "https://www2.econsig.com.br/hspm/v3/autenticarUsuario#no-back"

#NEOCONSIG
Corr_RJ = "https://rioconsig.com.br/rioconsig/"
Corr_Guarulhos=	"https://www.neoconsig.com.br/neoconsig/"
Corr_GovGoias = "https://www.neoconsig.com.br/neoconsig/"
Corr_Sorocaba = "https://www.neoconsig.com.br/neoconsig/"
Corr_Alagoas = "https://www.neoconsig.com.br/neoconsig/"

#CIP
Corr_GovPefSP = "https://www.portaldoconsignado.org.br/home?37"
Corr_MatoGrosso = "https://www.portaldoconsignado.com.br/home?9"

#CONSIGFACIL
Corr_PIAUI = "https://consigfacil.sead.pi.gov.br/index.php"
Corr_PrefCampinaGrande ="https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Corr_IPSEM_CampinaGrande = "https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Corr_PrefJoaoPessoa = "https://www.faciltecnologia.com.br/consigfacil/joaopessoa/index.php"
Corr_GovMaranhao = "https://www.faciltecnologia.com.br/consigfacil/maranhao/index.php"
Corr_PrefPortoVelho = "https://www.faciltecnologia.com.br/consigfacil/portovelho/"
Corr_GovPernambuco = "https://www.peconsig.pe.gov.br/index.php"
Corr_PrefRecife = "https://www.faciltecnologia.com.br/consigfacil/recife/index.php"

# Pega variaveis de login Zetra de ambiente do sistema 
try:
    ZETRA_Username_Values = os.getenv("ZETRA_Username_Values")
    Password_Values = os.getenv("Password_Values")
    if not all ([ZETRA_Username_Values,Password_Values]):
        raise ValueError("Coloque as variáveis do ambiente")   
except Exception as e:
    print("Não foi possível achar os valores")

"""
Aguardando Valores para evitar erros

# Pega variaveis de login NeoConsig de ambiente do sistema 
try:
    NeoConsig_Username_Values = os.getenv("NeoConsig_Username_Values")
    if not all ([NeoConsig_Username_Values,Password_Values]):
        raise ValueError("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

# Pega variaveis de login CIP de ambiente do sistema 
try:
    Cip_Username_Values = os.getenv("Cip_Username_Values")
    if not all ([Cip_Username_Values,Password_Values]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

# Pega variaveis de login CONSIGFACIL de ambiente do sistema
try:
    ConsigFacil_Username_Values = os.getenv("ConsigFacil_Username_Values")
    if not all ([ConsigFacil_Username_Values, Password_Values]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

"""

#Começa o login na corretora de EMBU
driver = webdriver.Edge()
driver.get(Corr_EMBU)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

#Começa o login na corretora de Alagoas
driver.get(Corr_Alagoas)

#Começa o login na corretora de Goias
driver.get(Corr_GovGoias)

#Começa o login na corretora do Maranhão
driver.get(Corr_GovMaranhao)

#Começa o login na correta da Prefeitura e governo de São Paulo
driver.get(Corr_GovPefSP)

#Começa o login na corretora de Pernambuco
driver.get(Corr_GovPernambuco)

#Começa o login na corretora de Guarulhos
driver.get(Corr_Guarulhos)

#Começa o login na corretora do Hospital do Servidor Público de São Paulo
driver.get(Corr_HospDoServPubSP)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

#Começa o login na corretora dA IGPREV
driver.get(Corr_IGEPREV)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN) #Tempo pra resolver o captcha
time.sleep(10)
assert "No results found." not in driver.page_source

#Começa o Login no Instituto de previdência de Campina Grande
driver.get(Corr_IPSEM_CampinaGrande)

"""
Só liberar Corretora da Prefeitura do Paraná Após resolver o erro da Variável

#Começa o login na corretora do Paraná
driver.get(Corr_Parana)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
time.sleep(30) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

"""

#Começa o login na corretora do Mato Grosso
driver.get(Corr_MatoGrosso)

#Começa o login na corretora do Piauí
driver.get(Corr_PIAUI)

#Começa o login na corretora da Prefeitura da Serra ES
driver.get(Corr_Pref_Serra_ES)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

#Começa o login na corretora da prefeitura de Curitiba
driver.get(Corr_PrefCuritiba)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

#Começa o login na corretora de João Pessoa
driver.get(Corr_PrefJoaoPessoa)

#Começa o login na corretora de Porto Velho
driver.get(Corr_PrefPortoVelho)

#Começa o login na corretora da prefeitura de Recife
driver.get(Corr_PrefRecife)

#Começa o login na corretora de São Bernardo do Campo
driver.get(Corr_PrefSBC)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN) 
time.sleep(10) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

#Começa o login na corretora de Uberlândia
driver.get(Corr_PrefUberlandia)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(ZETRA_Username_Values)
elem.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
assert "No results found." not in driver.page_source

#Começa o login na corretora do Rio De Janeiro
driver.get(Corr_RJ)

#Começa o login na corretora de Sorocaba
driver.get(Corr_Sorocaba)

#Começa o login na corretora da prefeitura de Campina Grande
driver.get(Corr_PrefCampinaGrande)


