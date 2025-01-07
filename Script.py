import os
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import date, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Define a variáveis dos sites das Processadoras

#Zetra
Proc_EMBU = "https://portal.econsig.com.br/embudasartes/v3/autenticarUsuario?t=20241226140450#no-back"
Proc_IGEPREV = "https://portal.econsig.com.br/igeprev/v3/autenticarUsuario#no-back"
Proc_PrefSBC ="https://www.econsig.com.br/sbc/v3/autenticarUsuario?t=20190520100728#no-back"
Proc_Pref_Serra_ES = "https://www.econsig.com.br/serra"
Proc_PrefUberlandia = "https://www.econsig.com.br/uberlandia"
Proc_PrefCuritiba = "https://www2.econsig.com.br/curitiba/v3/autenticarUsuario?t=20230904104333#no-back"
Proc_HospDoServPubSP = "https://www2.econsig.com.br/hspm/v3/autenticarUsuario#no-back"

#CIP
Proc_GovPefSP = "https://www.portaldoconsignado.org.br/home?37"
Proc_MatoGrosso = "https://www.portaldoconsignado.com.br/home?9"
Proc_SEFAZ = "https://www.portaldoconsignado.com.br/home?76"

#CONSIGFACIL
Proc_PIAUI = "https://consigfacil.sead.pi.gov.br/index.php" #!!
Proc_PrefJoaoPessoa = "https://www.faciltecnologia.com.br/consigfacil/joaopessoa/index.php"
Proc_GovMaranhao = "https://www.faciltecnologia.com.br/consigfacil/maranhao/index.php"
Proc_PrefPortoVelho = "https://www.faciltecnologia.com.br/consigfacil/portovelho/"
Proc_GovPernambuco = "https://www.peconsig.pe.gov.br/index.php"
Proc_PrefRecife = "https://www.faciltecnologia.com.br/consigfacil/recife/index.php"
Proc_PrefCampinaGrande ="https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"
Proc_IPSEM_CampinaGrande = "https://www.faciltecnologia.com.br/consigfacil/campinagrande/index.php"

#CONSIG
Proc_Parana = "https://www.paranaconsig.pr.gov.br/parquetec/"


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

# Pega variaveis de login NeoConsig de ambiente do sistema (PlaceHolders)
try:
    NeoConsig_Username_Values = os.getenv("NeoConsig_Username_Values")
    if not all ([NeoConsig_Username_Values]):
        raise ValueError("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

#Pega variaveis de login CIP de ambiente do sistema (PlaceHolders)
try:
    User_CIP = os.getenv("User_CIP")
    Senha_CIP = os.getenv("Senha_CIP")
    if not all ([User_CIP,Senha_CIP]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

# Pega variaveis de login CONSIGFACIL de ambiente do sistema (PlaceHolders)
try:
    ConsigFacil_Username_Values = os.getenv("ConsigFacil_Username_Values")
    ConsigFacil_Psw_Values = os.getenv("ConsigFacil_Psw_Values")
    if not all ([ConsigFacil_Username_Values, ConsigFacil_Psw_Values]):
        raise ValueError ("Coloque valores nas variáveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

#Pega variavel de login NEOCONSIG do ambiente do sistema
try:
    Acesso_NeoConsigRJ = os.getenv("User_NeoConsigRJ")
    if not all ([Acesso_NeoConsigRJ]):
        raise ValueError ("Coloque os valores nas variaveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

#Variaveis Comandos Selenium
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)
driver.maximize_window() #Recomendo desabilitar caso não use monitor secundário

#Keys para chamada mais rápida
Seta_Baixo = Keys.ARROW_DOWN
Enter = Keys.RETURN
Tab = Keys.TAB

#Variaveis Data
data_atual = date.today()
data_atual_txt = data_atual.strftime('%d/%m/%Y')
data_de_ontem = data_atual - timedelta(days=1) # Convert string back to date and subtract
data_ontem_txt = data_de_ontem.strftime('%d/%m/%Y')
data_finalDeSemana = data_atual - timedelta(days=3)
data_finalDeSemana_txt = data_finalDeSemana.strftime('%d/%m/%y')

RodarTesteVar = input ("Pressione 's' caso queira rodar o teste da funcionabilidade das variaveis. \nCaso não queira, pressione qualquer outra tecla: \n")
if RodarTesteVar == 's':
    #Teste Funcionabilidade Variáveis data
    print("Ontem foi dia: ", data_ontem_txt)
    print("O final de semana começou no dia: ", data_finalDeSemana_txt)
    print(data_ontem_txt)
    #Testa Getenv para verificar se há erros nas variáveis
    print(ZETRA_Username_Values)
    print(ZETRA_Password_Values)
    print(User_CIP)
    print(Senha_CIP)
    print(ConsigFacil_Username_Values)
    print(ConsigFacil_Psw_Values)
    print(Acesso_NeoConsigRJ)
    print(NeoConsig_Username_Values)
    print('\n')
else:
    print("")

#Logins na ZETRA---------------------------------------------------------
def Relatorios_Zetra():
    #Começa o login na Processadora de EMBU
    driver.get(Proc_EMBU)
    assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    #Data de inclusão/Alteração
    time.sleep(2)
    """
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)


    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)
    """
    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    #Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    #FALTA ARRUMAR ABAIXO !!!
    #Começa o login na Processadora da IGPREV
    driver.get(Proc_IGEPREV)
    assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[3]/a').click()
    driver.find_element(By.XPATH,'//*[@id="menuRelatorio"]/ul/li[2]/a').click() #ERRO
    #Data de inclusão/Alteração
    time.sleep(2)

    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)

    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    #Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)

    #Começa o login na Processadora do Hospital do Servidor Público de São Paulo
    driver.get(Proc_HospDoServPubSP)
    assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    #Data de inclusão/Alteração
    time.sleep(2)

    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)

    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    #Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)

    #Começa o login na Processadora da Prefeitura da Serra ES
    driver.get(Proc_Pref_Serra_ES)
    assert "SISTEMA DIGITAL DE CONSIGNAÇÕES" in driver.title
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    #Data de inclusão/Alteração
    time.sleep(2)

    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)

    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    #Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)

    #Começa o login na Processadora da prefeitura de Curitiba
    driver.get(Proc_PrefCuritiba)
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    #Data de inclusão/Alteração
    time.sleep(2)

    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)

    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/thead/tr/th[3]")
    Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/div/a[1]").click()
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()

    #Começa o login na Processadora de São Bernardo do Campo
    driver.get(Proc_PrefSBC)
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    #Data de inclusão/Alteração
    time.sleep(2)

    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)

    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    #Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)

    #Começa o login na Processadora de Uberlândia
    UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
    UserZetra.send_keys(ZETRA_Username_Values)
    UserZetra.send_keys(Enter)
    PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
    PswZetra.send_keys(ZETRA_Password_Values)
    ZetraCaptcha_Resolver = input("Digite o Captcha: ")
    CaptchaZetra = driver.find_element(By.ID, "captcha")
    CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
    CaptchaZetra.send_keys(Enter)
    time.sleep(1)
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    #Data de inclusão/Alteração
    time.sleep(2)

    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_ontem_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)
    Selec_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select").click()
    Achar_Estabelecim = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[4]/select")
    Achar_Estabelecim.send_keys(Seta_Baixo)
    Achar_Estabelecim.send_keys(Enter)

    #CheckBox

    #Situação servidor
    Sit_Servidor_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Situação do contrato
    #Sit_contrato_Zetra = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[2]/div[2]/div/div[7]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    #driver.find_element(By.ID, "formato").click()
    Selec_tipo_Arquivo = driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select")
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Seta_Baixo)
    Selec_tipo_Arquivo.send_keys(Enter)

    driver.find_element(By.ID, "btnEnvia")
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[2]/a").click()
    #Selec_BotEnv = driver.find_element(By.ID, "btnEnvia")
    #Selec_BotEnv.send_keys(Enter)
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    #Click_OpRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]').click()
    time.sleep(1)
    Click_DownloadRel = driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)



#Logins na CIP---------------------------------------------------------

def Relatorios_CIP():
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

def Relatorios_ConsigFacil():
    #Começa o login na Processadora de João Pessoa
    driver.get(Proc_PrefJoaoPessoa)
    User_ConsigFacil = driver.find_element (By.ID, "usuario")
    User_ConsigFacil.clear()
    User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
    Psw_ConsigFacil = driver.find_element (By.ID, "senha")
    Psw_ConsigFacil.clear()
    Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
    ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
    ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
    ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
    Psw_ConsigFacil.send_keys(Keys.RETURN)
    time.sleep(1) 

    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
    time.sleep(1)

    driver.execute_script ("document.body.style.zoom='50%'")
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,'//*[@id="sidebar"]/ul/div[1]/div[2]/div/div/div/li[6]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[6]/ul/li[15]/a').click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(1)
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="folha"]').click()

    #EMLUR
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[2]').click()
    time.sleep(2)
    #Box impede visualização em tela do Download
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div/div/div[2]/div[5]/div[2]/div/input").click()
    time.sleep(2)
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(10)

    #FUNJOPE
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[3]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(7)

    #IPM Ativos e Inativos
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[4]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(7)

    #IPM Pensionistas
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[5]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(7)

    #PMJP
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[6]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(7)

    #SEMOB
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[7]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(7)

    #SMS
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[8]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(7)


    time.sleep(15)

    """
    #Começa o login na Processadora do Maranhão
    driver.get(Proc_GovMaranhao)
    User_ConsigFacil = driver.find_element (By.ID, "usuario")
    User_ConsigFacil.clear()
    User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
    Psw_ConsigFacil = driver.find_element (By.ID, "senha")
    Psw_ConsigFacil.clear()
    Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
    ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
    ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
    ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
    Psw_ConsigFacil.send_keys(Keys.RETURN)
    time.sleep(1) 

    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
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
    """
    #Começa o Login no Processadora do Instituto de previdência de Campina Grande
    driver.get(Proc_IPSEM_CampinaGrande)
    #assert "ConsigFácil - Campina Grande" in driver.title
    User_ConsigFacil = driver.find_element (By.ID, "usuario")
    User_ConsigFacil.clear()
    User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
    Psw_ConsigFacil = driver.find_element (By.ID, "senha")
    Psw_ConsigFacil.clear()
    Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
    ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
    ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
    ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
    Psw_ConsigFacil.send_keys(Keys.RETURN)
    time.sleep(1) 
    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
    time.sleep(1)

    driver.execute_script ("document.body.style.zoom='50%'")
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,'//*[@id="sidebar"]/ul/div[1]/div[2]/div/div/div/li[6]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[6]/ul/li[13]/a').click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(1)
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="folha"]').click()

    #IPSEM - Instituto de Previdência 
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[2]').click()
    time.sleep(2)
    #Box impede visualização em tela do Download
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/div/div/div[2]/div[5]/div[2]/div/input").click()
    time.sleep(2)
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(10)

    #Prefeitura Municipal de Campina Grande
    driver.find_element(By.XPATH, '//*[@id="folha"]/option[3]').click()
    #Gera relatório
    driver.find_element(By.XPATH,'//*[@id="frmservico"]/div/div/div[2]/div[6]/div/button').click()
    time.sleep(10)

    """
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
    driver.find_element(By.XPATH, '//*[@id="staticBackdrop"]/div/div/div[3]/button[1]').click()
    """

    #Começa o login na Processadora de Porto Velho
    driver.get(Proc_PrefPortoVelho)
    #assert "ConsigFácil - Campina Grande" in driver.title
    User_ConsigFacil = driver.find_element (By.ID, "usuario")
    User_ConsigFacil.clear()
    User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
    Psw_ConsigFacil = driver.find_element (By.ID, "senha")
    Psw_ConsigFacil.clear()
    Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
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
    User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
    Psw_ConsigFacil = driver.find_element (By.ID, "senha")
    Psw_ConsigFacil.clear()
    Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
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
    User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
    Psw_ConsigFacil = driver.find_element (By.ID, "senha")
    Psw_ConsigFacil.clear()
    Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
    ConsigFacil_CaptchaResolver = input("Digite o Captcha: ")
    ConsigFacilCaptcha = driver.find_element(By.ID, "captcha")
    ConsigFacilCaptcha.send_keys(ConsigFacil_CaptchaResolver)
    Psw_ConsigFacil.send_keys(Keys.RETURN)
    time.sleep(1) 

    time.sleep(20) #Tempo para abrir a conexão Forticlient

#Logins na NEOCONSIG (NECESSÁRIO CONEXÃO FORTICLIENT)---------------------------------------------------------
def Relatorios_NeoConsig():
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
    
    #Logins Consig (Necessário Conexão FortiClient)
    
def Relatorios_ConsigPR():
    #Login Processadora Paraná 
    driver.get(Proc_Parana)
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/a/button").click()
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/ul/li[3]/a").click()
    Insert_Login_PR = driver.find_element(By.XPATH, '//*[@id="login"]')
    Insert_Login_PR.send_keys(Acesso_NeoConsigRJ)
    Insert_Login_PR.send_keys(Enter)
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="s2id_cod_convenio"]/a').click()
    Selec_Gov_PR = driver.find_element(By.XPATH, '//*[@id="s2id_cod_convenio"]/a')
    Selec_Gov_PR.send_keys(Seta_Baixo)
    Selec_Gov_PR.send_keys(Enter)
    driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/form/div[3]/select').click()
    Selec_Conv = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div/form/div[3]/select')
    Selec_Conv.send_keys(Seta_Baixo)
    Selec_Conv.send_keys(Enter)
    ConsigCaptcha_Resolver = input ("Digite o captcha: ")
    Consig_Captcha = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[6]/div[3]/input")
    Consig_Captcha.send_keys(ConsigCaptcha_Resolver)
    driver.find_element(By.XPATH, '//*[@id="servidor-form"]/div[7]/a').click()
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/p/a").click
    time.sleep(20) #Tempo para fechar a conexão Forticlient      
    
    #FECHA CONEXÃO FORTICLIENT
def Relatorios_ProcRJ():
        #Coeça o login na Processadora do Rio De Janeiro
        driver.get(Proc_RJ)
        driver.find_element(By.ID, "btn-acessar-sistema").click()
        Click_Acess = driver.find_element(By.ID, "tipo_acesso")
        Click_Acess.send_keys(Enter)
        Select_Acess = driver.find_element(By.ID, "tipo_acesso")
        Select_Acess.send_keys(Seta_Baixo)
        Login_Proc_RJ = driver.find_element (By.ID, "cod_acesso")
        Login_Proc_RJ.send_keys(Acesso_NeoConsigRJ)
        NeoConsig_Captcha_Resolver = input("Digite o Captcha: ")
        NeoConsig_Captcha = driver.find_element(By.ID, "captcha_code")
        NeoConsig_Captcha.send_keys(NeoConsig_Captcha_Resolver)
        Login_Proc_RJ.send_keys(Tab)
        Login_Proc_RJ.send_keys(Enter)
        driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div[1]/p/a").click()
        time.sleep(10)#TEMPO PARA COLOCAR A SENHA NO TECLADO DIGITAL
        
        #Abe a aba de relatório
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/a/span[1]").click()
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/a").click()
        time.sleep(2)

        #Seleciona o Produto para Relatório
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[1]/div/div/a/span[1]").click()
        Digita_Produto_Desejado = input("Digite o produto que você deseja ver relatórios: ")        #Opções: Empréstimo, Cartão de crédito, 
        Selec_Produto_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')     # Beneficio Saque, Beneficio compras
        Selec_Produto_Desejado.send_keys(Digita_Produto_Desejado)
        Selec_Produto_Desejado.send_keys(Enter)

        #Seleciona órgão 

        #FUNDAÇÃO PARQUES E JARDINS
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[2]").click()

        #Selecionando Mês 
        Digita_Mes_Desejado = input("Digite o mês que você gostaria de gerar o relatório referente: ")
        driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/a/span[1]").click()
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen3_search"]')
        Selec_Mes_Desejado.send_keys(Digita_Mes_Desejado)
        Selec_Mes_Desejado.send_keys(Enter)

        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/div/select/option[12]").click

        #Seleciona ANO
        Digita_Ano_Desejado = input("Digite o ano que você gostaria de gerar o relatório referente: ")
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/div/div/a/span[1]").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen5_search"]')
        Selec_Ano_Desejado.send_keys(Digita_Ano_Desejado)
        Selec_Ano_Desejado.send_keys(Enter)

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #PENSIONISTAS DO MUNICIPIO DO RIO DE JANEIRO RJ
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[3]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #EMPRESA MUNICIPAL DE MULTIMEIOS LTDA
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[4]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #GUARDA MUNICIPAL DO RIO DE JANEIRO
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[5]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #EMPRESA PUBLICA DE SAUDE DO RIO DE JANEIRO
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[6]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #INSTITUTO DE PREVIDENCIA E ASSISTENCIA DO M.R.J
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[7]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #Prefeitura RJ
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[8]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

        #Seleciona órgão 
        #FUNDO MESPECIAL DE PREVIDENCIA DO MUNICIPIO DO RJ
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/div/select/option[9]").click()

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[4]/div/div/a[2]").click()
        time.sleep(10)

#------------------ Chama as funções para gerar relatórios --------------------------------


#Relatorios_Zetra()


#Relatorios_ConsigFacil() #João Pessoa e Campina grande Funcional 


Relatorios_CIP() # Necessita terminar o portal da SEFAZ

RodarProcsVPN = input("Digite 's' se deseja rodar as processadoras que necessitam de VPN ou 'n' para pular\n")

if RodarProcsVPN == 's':
    Relatorios_NeoConsig() # Precisa ser feito conectado a forticlient
    Relatorios_ConsigPR() # Precisa ser feito conectado a forticlient
elif RodarProcsVPN =='n':
    print("")
elif RodarProcsVPN == 'S':
    Relatorios_NeoConsig() # Precisa ser feito conectado a forticlient
    Relatorios_ConsigPR() # Precisa ser feito conectado a forticlient
elif RodarProcsVPN =='N':
    print("")
else:
    print("Digite 'n' ou 's'")
    quit()

Relatorios_ProcRJ() #100% Funcional