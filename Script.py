import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Define a variáveis dos sites das corretoras
Corr_EMBU = "https://portal.econsig.com.br/embudasartes/v3/autenticarUsuario?t=20241226140450#no-back"
Corr_PIAUI = "https://consigfacil.sead.pi.gov.br/index.php"
Corr_IGEPREV = "https://portal.econsig.com.br/igeprev/v3/autenticarUsuario#no-back"
Corr_RJ = "https://rioconsig.com.br/rioconsig/"
Corr_PrefSBC ="https://www.econsig.com.br/sbc/v3/autenticarUsuario?t=20190520100728#no-back"
Corr_Pref_Serra_ES = "https://www.econsig.com.br/serra"
Corr_PrefUberlandia = "https://www.econsig.com.br/uberlandia"
Corr_PrefCampinaGrande ="https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Corr_IPSEM_CampinaGrande = "https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Corr_PrefJoaoPessoa = "https://www.faciltecnologia.com.br/consigfacil/joaopessoa/index.php"
Corr_GovMaranhao = "https://www.faciltecnologia.com.br/consigfacil/maranhao/index.php"
Corr_PrefPortoVelho = "https://www.faciltecnologia.com.br/consigfacil/portovelho/"
Corr_Guarulhos=	"https://www.neoconsig.com.br/neoconsig/"
Corr_GovGoias = "https://www.neoconsig.com.br/neoconsig/"
Corr_Sorocaba = "https://www.neoconsig.com.br/neoconsig/"
Corr_Alagoas = "https://www.neoconsig.com.br/neoconsig/"
Corr_GovPernambuco = "https://www.peconsig.pe.gov.br/index.php"
Corr_MatoGrosso = "https://www.portaldoconsignado.com.br/home?9"
Corr_GovPefSP = "https://www.portaldoconsignado.org.br/home?37"
"""
Achar erro na corretora do Paraná (Conexão não particular)
Corr_Parana = "https://www.prconsig.seap.pr.gov.br/pr/v3/autenticarUsuario?t=20221012152301#no-back"
"""
Corr_PrefCuritiba = "https://www2.econsig.com.br/curitiba/v3/autenticarUsuario?t=20230904104333#no-back"
Corr_HospDoServPubSP = "https://www2.econsig.com.br/hspm/v3/autenticarUsuario#no-back"
"""
Achar erro na Corretora da prefeitura de Recife
Corr_PrefRecife = "www.faciltecnologia.com.br/consigfacil/recife/index.php"
"""

# Pega variaveis de login de ambiente do sistema 
try:
    Username_Values = os.getenv("Username_Values")
    Password_Values = os.getenv("Password_Values")
    if not all ([Username_Values,Password_Values]):
        raise ValueError("Coloque as variáveis do ambiente")   
except Exception as e:
    print("Não foi possível achar os valores")

#Começa o login na corretora de EMBU
driver = webdriver.Edge()
driver.get(Corr_EMBU)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
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
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#Começa o login na corretora dA IGPREV
driver.get(Corr_IGEPREV)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#Começa o Login no Instituto de previdência de Campina Grande
driver.get(Corr_IPSEM_CampinaGrande)

"""
#Começa o login na corretora do Paraná
driver.get(Corr_Parana)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
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
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#Começa o login na corretora da prefeitura de Curitiba
driver.get(Corr_PrefCuritiba)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#Começa o login na corretora de João Pessoa
driver.get(Corr_PrefJoaoPessoa)

#Começa o login na corretora de Porto Velho
driver.get(Corr_PrefPortoVelho)

#Só liberar Corretora da Prefeitura de Recife Após resolver a Variável
#driver.get(Corr_PrefRecife)

#Começa o login na corretora de São Bernardo do Campo
driver.get(Corr_PrefSBC)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#Começa o login na corretora de Uberlândia
driver.get(Corr_PrefUberlandia)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
elem = driver.find_element(By.ID, "username")
elem.clear()
elem.send_keys(Username_Values)
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#Começa o login na corretora do Rio De Janeiro
driver.get(Corr_RJ)

#Começa o login na corretora de Sorocaba
driver.get(Corr_Sorocaba)

#Começa o login na corretora da prefeitura de Campina Grande
driver.get(Corr_PrefCampinaGrande)

