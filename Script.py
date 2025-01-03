import os
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
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

#CIP
Proc_GovPefSP = "https://www.portaldoconsignado.org.br/home?37"
Proc_MatoGrosso = "https://www.portaldoconsignado.com.br/home?9"
Proc_SEFAZ = "https://www.portaldoconsignado.com.br/home?76"

#CONSIGFACIL
Proc_PIAUI = "https://consigfacil.sead.pi.gov.br/index.php"
Proc_PrefCampinaGrande ="https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Proc_IPSEM_CampinaGrande = "https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Proc_PrefJoaoPessoa = "https://www.faciltecnologia.com.br/consigfacil/joaopessoa/index.php"
Proc_GovMaranhao = "https://www.faciltecnologia.com.br/consigfacil/maranhao/index.php"
Proc_PrefPortoVelho = "https://www.faciltecnologia.com.br/consigfacil/portovelho/"
Proc_GovPernambuco = "https://www.peconsig.pe.gov.br/index.php"
Proc_PrefRecife = "https://www.faciltecnologia.com.br/consigfacil/recife/index.php"

#NEOCONSIG
Proc_RJ = "https://rioconsig.com.br/rioconsig/login"

#Mesmo Site da NeoConsig
Proc_Guarulhos=	"https://www.neoconsig.com.br/neoconsig/" 
Proc_GovGoias = "https://www.neoconsig.com.br/neoconsig/"
Proc_Sorocaba = "https://www.neoconsig.com.br/neoconsig/"
Proc_Alagoas = "https://www.neoconsig.com.br/neoconsig/"


# Pega variaveis de login Zetra de ambiente do sistema (Placheholders)
try:
    ZETRA_Username_Values = os.getenv("Zetra_Username_Values")
    ZETRA_Password_Values = os.getenv("Zetra_Password_Values")
    if not all ([ZETRA_Username_Values,ZETRA_Password_Values]):
        raise ValueError("Coloque as variáveis do ambiente")   
except Exception as e:
    print("Não foi possível achar os valores")

"""
Aguardando Valores para evitar erros

# Pega variaveis de login NeoConsig de ambiente do sistema (PlaceHolders)
try:
    NeoConsig_Username_Values = os.getenv("NeoConsig_Username_Values")
    NeoConsig_Psw_Values = os.getenv("NeoConsig_Psw_Values")
    if not all ([NeoConsig_Username_Values,NeoConsig_Psw_Values]):
        raise ValueError("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")
"""
#Pega variaveis de login CIP de ambiente do sistema (PlaceHolders)
try:
    User_CIP = os.getenv("User_CIP")
    Senha_CIP = os.getenv("Senha_CIP")
    if not all ([User_CIP,Senha_CIP]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")
"""
# Pega variaveis de login CONSIGFACIL de ambiente do sistema (PlaceHolders)
try:
    ConsigFacil_Username_Values = os.getenv("ConsigFacil_Username_Values")
    ConsigFacil_Psw_Values = os.getenv("ConsigFacil_Psw_Values")
    if not all ([ConsigFacil_Username_Values, Password_Values]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

#Pega variavel de login NEOCONSIG do ambiente do sistema (PlaceHolders)
try:
    Codigo_NeoConsig = os.gentenv("Codigo_NeoConsig")
    if not all ([Codigo_NeoConsig]):
        raise ValueError ("Coloque os valores nas variaveis do ambiente")
except Exception as e:
    print(f"Erro {e}")
"""
#Variaveis Comandos Selenium
driver = webdriver.Edge()
Cip_Crash = "https://www.portaldoconsignado.org.br/wicket/page?9"
driver.maximize_window() #Recomendo desabilitar caso não use monitor secundário

#Keys para chamada mais rápida
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
PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
PswZetra.send_keys(ZETRA_Password_Values)
ZetraCaptcha_Resolver = input("Digite o Captcha: ")
time.sleep(1)
CaptchaZetra = driver.find_element(By.ID, "captcha")
CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
CaptchaZetra.send_keys(Enter)
time.sleep(1)
#assert "No results found." not in driver.page_source

#Começa o login na Processadora da IGPREV
driver.get(Proc_IGEPREV)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
PswZetra = driver.find_element(By.NAME, "senha")
PswZetra.clear()
PswZetra.send_keys(ZETRA_Password_Values)
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
#Começa o login na Processadora do Hospital do Servidor Público de São Paulo
driver.get(Proc_HospDoServPubSP)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Enter)
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

#Começa o login na Processadora da Prefeitura da Serra ES
driver.get(Proc_Pref_Serra_ES)
assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
UserZetra = driver.find_element(By.ID, "username")
UserZetra.clear()
UserZetra.send_keys(ZETRA_Username_Values)
UserZetra.send_keys(Keys.RETURN)
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

#Logins na CIP---------------------------------------------------------

#Começa o login na Processadora do Mato Grosso
driver.get(Proc_GovPefSP)
#Login no portal
Selec_Aba = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/span/span").click()
Insira_User_CIP = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[3]/input")
Insira_User_CIP.send_keys(User_CIP)
Insira_Senha_CIP = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[4]/input")
Insira_Senha_CIP.send_keys(Senha_CIP)
Cip_Captcha_Resolver = input("Digite o Captcha: ")
Cip_Captcha = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[5]/div/input")
Cip_Captcha.send_keys(Cip_Captcha_Resolver)
Cip_Captcha.send_keys(Enter)
time.sleep(2)

#Seleciona Portal Do Mato Grosso
Selec_Bot_PrefMS = driver.find_element(By.CLASS_NAME, "btExpandir").click()
Selec_Entr_PrefMS = driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[4]/div[2]/fieldset/div/div[2]/fieldset/span/label").click()
Env_Acess = driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/div/div[7]/input").click()
time.sleep(4)
#Seleciona o gerador de relatório no portal
Selec_Tab_Rel = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/a/span").click()
Selec_Tab_GerRel = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/div/div/a").click()
#Seleciona a Opção de Visão do Relatório
Selec_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select").click
Achar_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select")
Achar_OP_Vis.send_keys(Seta_Baixo)
Achar_OP_Vis.send_keys(Enter)
#Tempo pro site Carregar
time.sleep(4)
#Seleciona o Relatório disponível com a opção de visão
Selec_Tab_Rel = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select").click()
AcharOP_Rel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select")
AcharOP_Rel.send_keys(Seta_Baixo)
AcharOP_Rel.send_keys(Enter)
time.sleep(4)
#Seleciona os orgãos disponíveis pra Orgãos selecionados
Selec_OrgD_ORGS = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[6]/div/div[2]/span/div[2]/div/button[3]").click()
#Seleciona as espécies disponíveis pra Espécieis selecionadas
Selec_ESPD_ESPS = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[9]/div/div[2]/span/div[2]/div/button[3]").click()

#Seleciona as caixas desejadas pro relatório

#Selecionar Nome 
Selec_Nome_MS = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[7]/td[1]/input").click()
#Selecionar Matricula
Selec_MatFun_MS = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[2]/td[2]/input").click()
#Selecionar CPF
Selec_CPF_MS = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[3]/td[2]/input").click()
#Selecionar Nome Reduzido CNPJ (MCC)
Selec_Nome_CNPJ_MS = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[2]/tbody/tr[3]/td[1]/input").click() 

#Fim das checkbox

#Click Gerar Relatório
Selec_Bot_GerRel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[7]/input[2]").click()
time.sleep(6)
#Baixar Relatório NA MÃO !
time.sleep(7)
driver.get("https://www.portaldoconsignado.org.br/consignatario/autenticado?74")
Selec_Troca_Perfil_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[3]/a/span").click()
Abre_Box_MS = driver.find_element(By.CLASS_NAME, "btExpandir").click()
Abre_Box_PrefSP = driver.find_element(By.CLASS_NAME, "btExpandir").click()

#Começa o login na Processadora da Prefeitura e governo de São Paulo
driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[5]/div[2]/fieldset/div/div[2]/fieldset/span/label/input").click()
driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[7]/input").click()
time.sleep(2)
#Seleciona o gerador de relatório no portal
Selec_Tab_Rel = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/a").click()
Selec_Tab_GerRel = driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/div/div/a").click()
time.sleep(1)
#Seleciona a Opção de Visão do Relatório
Selec_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select").click
Achar_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select")
Achar_OP_Vis.send_keys(Seta_Baixo)
Achar_OP_Vis.send_keys(Enter)
#Tempo pro site Carregar
time.sleep(4)
#Seleciona o Relatório disponível com a opção de visão
Selec_Tab_Rel = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select").click()
AcharOP_Rel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select")
AcharOP_Rel.send_keys(Seta_Baixo)
AcharOP_Rel.send_keys(Enter)
time.sleep(4)
#Seleciona os orgãos disponíveis pra Orgãos selecionados
Selec_OrgD_ORGS = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[6]/div/div[2]/span/div[2]/div/button[3]").click()
#Seleciona as espécies disponíveis pra Espécieis selecionadas
Selec_ESPD_ESPS = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[9]/div/div[2]/span/div[2]/div/button[3]").click()

#Seleciona as caixas desejadas pro relatório

#Selecionar Nome 
Selec_Nome_SP = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[7]/td[1]/input").click()
#Selecionar Matricula
Selec_MatFun_SP = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[2]/td[2]/input").click()
#Selecionar CPF
Selec_CPF_SP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[3]/td[2]/input").click()
#Selecionar Nome Reduzido CNPJ (MCC)
Selec_Nome_CNPJ_SP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[2]/tbody/tr[3]/td[1]/input").click() 

#Fim das checkbox

#Click Gerar Relatório
Selec_Bot_GerRel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[7]/input[2]").click()
time.sleep(6)
#Baixar Relatório NA MÃO !
time.sleep(7)
driver.get("https://www.portaldoconsignado.org.br/consignatario/autenticado?74")
Selec_Troca_Perfil_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[3]/a/span").click()
Abre_Box_MS = driver.find_element(By.CLASS_NAME, "btExpandir").click()
Abre_Box_PrefSP = driver.find_element(By.CLASS_NAME, "btExpandir").click()
Abre_Box_SEFAZ = driver.find_element(By.CLASS_NAME, "btExpandir").click()
#Começa o login na Processadora da SEFAZ
Selec_Bot_SEFAZ = driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[6]/div[2]/fieldset/div/div[2]/fieldset/span/label/input").click()
Click_Acess_SEFAZ = driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[7]/input").click()

time.sleep(10)

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

#Começa o Login no Processadora do Instituto de previdência de Campina Grande
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

#Logins na NEOCONSIG---------------------------------------------------------

#Começa o login na Processadora de Alagoas
driver.get(Proc_Alagoas)
Find_DropBar = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/a/button").click()
Click_DropBar = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/ul/li[3]/a").click()
#Select_Acess_DropBar = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[1]/ul/li[6]/ul/li[3]/a").click()
#Acess_DropBar = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[4]/form/input[1]")
#Acess_DropBar.send_keys("Login_NeoConsig")
# time.sleep(3)

#Começa o login na Processadora de Goias
driver.get(Proc_GovGoias)

#Começa o login na Processadora de Guarulhos
driver.get(Proc_Guarulhos)

#Começa o login na Processadora de Sorocaba
driver.get(Proc_Sorocaba)

#Começa o login na Processadora do Rio De Janeiro
driver.get(Proc_RJ)
Consig_Log = driver.find_element(By.ID, "btn-acessar-sistema").click()
Click_Acess = driver.find_element(By.ID, "tipo_acesso")
Click_Acess.send_keys(Enter)
Select_Acess = driver.find_element(By.ID, "tipo_acesso")
Select_Acess.send_keys(Seta_Baixo)
Select_Acess.send_keys(Seta_Baixo)
Login_Proc_RJ = driver.find_element (By.ID, "cod_acesso")
Login_Proc_RJ.send_keys("Codigo_NeoConsig")
NeoConsig_Captcha_Resolver = input("Digite o Captcha: ")
NeoConsig_Captcha = driver.find_element(By.ID, "captcha_code")
NeoConsig_Captcha.send_keys(NeoConsig_Captcha_Resolver)
Login_Proc_RJ.send_keys(Tab)
Login_Proc_RJ.send_keys(Enter)
time.sleep(5)


"""
Expected conditions para prosseguir para o donload

try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/center[2]/form/input[2]')))
    driver.find_element(By.XPATH, '//*[@id="container"]/center[2]/form/input[2]').click()
except TimeoutException:
    print("Falha no processo de acesso")

"""