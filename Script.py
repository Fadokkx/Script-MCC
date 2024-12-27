import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Define a variáveis dos sites das Processadoras

#Zetra
Proc_EMBU = "https://portal.econsig.com.br/embudasartes/v3/autenticarUsuario?t=20241226140450#no-back"
Proc_IGEPREV = "https://portal.econsig.com.br/igeprev/v3/autenticarUsuario#no-back"
Proc_PrefSBC ="https://www.econsig.com.br/sbc/v3/autenticarUsuario?t=20190520100728#no-back"
Proc_Pref_Serra_ES = "https://www.econsig.com.br/serra"
Proc_PrefUberlandia = "https://www.econsig.com.br/uberlandia"
"""
Achar erro na corretora do Paraná (Conexão não particular)
Proc_Parana = "https://www.prconsig.seap.pr.gov.br/pr/v3/autenticarUsuario?t=20221012152301#no-back"

"""
Proc_PrefCuritiba = "https://www2.econsig.com.br/curitiba/v3/autenticarUsuario?t=20230904104333#no-back"
Proc_HospDoServPubSP = "https://www2.econsig.com.br/hspm/v3/autenticarUsuario#no-back"

#NEOCONSIG
Proc_RJ = "https://rioconsig.com.br/rioconsig/"

#Mesmo Site NeoConsig
Proc_Guarulhos=	"https://www.neoconsig.com.br/neoconsig/" 
Proc_GovGoias = "https://www.neoconsig.com.br/neoconsig/"
Proc_Sorocaba = "https://www.neoconsig.com.br/neoconsig/"
Proc_Alagoas = "https://www.neoconsig.com.br/neoconsig/"

#CIP
Proc_GovPefSP = "https://www.portaldoconsignado.org.br/home?37"
Proc_MatoGrosso = "https://www.portaldoconsignado.com.br/home?9"

#CONSIGFACIL
Proc_PIAUI = "https://consigfacil.sead.pi.gov.br/index.php"
Proc_PrefCampinaGrande ="https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Proc_IPSEM_CampinaGrande = "https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Proc_PrefJoaoPessoa = "https://www.faciltecnologia.com.br/consigfacil/joaopessoa/index.php"
Proc_GovMaranhao = "https://www.faciltecnologia.com.br/consigfacil/maranhao/index.php"
Proc_PrefPortoVelho = "https://www.faciltecnologia.com.br/consigfacil/portovelho/"
Proc_GovPernambuco = "https://www.peconsig.pe.gov.br/index.php"
Proc_PrefRecife = "https://www.faciltecnologia.com.br/consigfacil/recife/index.php"

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
    NeoConsig_Psw_Values = os.getenv("NeoConsig_Psw_Values")
    if not all ([NeoConsig_Username_Values,NeoConsig_Psw_Values]):
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
"""
# Pega variaveis de login CONSIGFACIL de ambiente do sistema
try:
    ConsigFacil_Username_Values = os.getenv("ConsigFacil_Username_Values")
    ConsigFacil_Psw_Values = os.getenv("ConsigFacil_Psw_Values")
    if not all ([ConsigFacil_Username_Values, Password_Values]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

#Variaveis Comandos Selenium
driver = webdriver.Edge()
Seta_Baixo = Keys.ARROW_DOWN
Enter = Keys.RETURN
Tab = Keys.TAB
#Logins na ZETRA---------------------------------------------------------

#Começa o login na Processadora de EMBU
driver.get(Proc_EMBU)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Enter)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Enter)
time.sleep(1)
#assert "No results found." not in driver.page_source

#Começa o login na Processadora do Hospital do Servidor Público de São Paulo
driver.get(Proc_HospDoServPubSP)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Enter)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source

#Começa o login na Processadora dA IGPREV
driver.get(Proc_IGEPREV)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source

"""
# Só liberar Corretora da Prefeitura do Paraná Após resolver o erro da Variável

#Começa o login na corretora do Paraná
driver.get(Proc_Parana)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source
"""

#Começa o login na Processadora da Prefeitura da Serra ES
driver.get(Proc_Pref_Serra_ES)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source

#Começa o login na Processadora da prefeitura de Curitiba
driver.get(Proc_PrefCuritiba)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source

#Começa o login na Processadora de São Bernardo do Campo
driver.get(Proc_PrefSBC)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source

#Começa o login na Processadora de Uberlândia
driver.get(Proc_PrefUberlandia)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
time.sleep(10) #Tempo pra resolver o captcha
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys("123")
CZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Keys.RETURN)
time.sleep(1)
#assert "No results found." not in driver.page_source


#Logins na NEOCONSIG---------------------------------------------------------

#Começa o login na Processadora de Alagoas
driver.get(Proc_Alagoas)

#Começa o login na Processadora de Goias
driver.get(Proc_GovGoias)

#Começa o login na Processadora de Guarulhos
driver.get(Proc_Guarulhos)

#Começa o login na Processadora de Sorocaba
driver.get(Proc_Sorocaba)

#Começa o login na Processadora do Rio De Janeiro
driver.get(Proc_RJ)
Click_LogPage = driver.find_element(By.ID, "btn-acessar-sistema")
Click_LogPage.send_keys(Keys.LEFT)
Select_Acess = driver.find_element(By.ID, "tipo_acesso")
Select_Acess.send_keys(Seta_Baixo)





#Logins na CIP---------------------------------------------------------

#Começa o login na Processadora da Prefeitura e governo de São Paulo
driver.get(Proc_GovPefSP)

#Começa o login na Processadora do Mato Grosso
driver.get(Proc_MatoGrosso)

#Logins na CONSIGFACIL---------------------------------------------------------

#Começa o login na Processadora do Maranhão
driver.get(Proc_GovMaranhao)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o login na Processadora de Pernambuco
driver.get(Proc_GovPernambuco)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o Login no Processadora de previdência de Campina Grande
driver.get(Proc_IPSEM_CampinaGrande)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o login na Processadora do Piauí
driver.get(Proc_PIAUI)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o login na Processadora de João Pessoa
driver.get(Proc_PrefJoaoPessoa)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o login na Processadora de Porto Velho
driver.get(Proc_PrefPortoVelho)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o login na Processadora da prefeitura de Recife
driver.get(Proc_PrefRecife)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 

#Começa o login na Processadora da prefeitura de Campina Grande
driver.get(Proc_PrefCampinaGrande)
#assert "ConsigFácil - Campina Grande" in driver.title
User_ConsigFacil = driver.find_element (By.ID, "usuario")
User_ConsigFacil.clear()
User_ConsigFacil.send_keys("ConsigFacil_Username_Values")
Psw_ConsigFacil = driver.find_element (By.ID, "senha")
Psw_ConsigFacil.clear()
Psw_ConsigFacil.send_keys("ConsigFacil_Psw_Value")
ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
Psw_ConsigFacil.send_keys(Keys.RETURN)
time.sleep(1) 


