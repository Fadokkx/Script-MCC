import os
import time
import locale
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

#Define Locale
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

#Define a variáveis dos sites das Processadoras

#Zetra
Proc_EMBU = "https://portal.econsig.com.br/embudasartes/v3/autenticarUsuario?t=20241226140450#no-back"
Proc_IGEPREV = "https://portal.econsig.com.br/igeprev/v3/autenticarUsuario#no-back"
Proc_PrefSBC ="https://www.econsig.com.br/sbc/v3/autenticarUsuario?t=20190520100728#no-back"
Proc_Pref_Serra_ES = "https://www.econsig.com.br/serra"
Proc_PrefUberlandia = "https://www.econsig.com.br/uberlandia"
Proc_PrefCuritiba = "https://www2.econsig.com.br/curitiba/v3/autenticarUsuario?t=20230904104333#no-back"
Proc_HospDoServPubSP = "https://www2.econsig.com.br/hspm/v3/autenticarUsuario#no-back"

#SIAPE
SIAPE = ""

#CIP
Proc_GovPefSP = "https://www.portaldoconsignado.org.br/home?37"
Proc_MatoGrosso = "https://www.portaldoconsignado.com.br/home?9"
Proc_SEFAZ = "https://www.portaldoconsignado.com.br/home?76"

#CONSIGFACIL
Proc_PIAUI = "https://consigfacil.sead.pi.gov.br/index.php" 
Proc_PrefJoaoPessoa = "https://www.faciltecnologia.com.br/consigfacil/joaopessoa/index.php" 
Proc_GovMaranhao = "https://www.faciltecnologia.com.br/consigfacil/maranhao/index.php" #!!
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

#BPO
BPO = "https://front.meucashcard.com.br/WebAppBPOCartao/Login/ICLogin?ReturnUrl=%2FWebAppBPOCartao%2FPages%2FProposta%2FICPropostaCartao"

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

#Pega variavel de login BPO do ambiente do sistema
try:
    Login_BPO = os.getenv("User_BPO_Value")
    Senha_BPO = os.getenv("BPO_Psw_Value")
    if not all ([Login_BPO, Senha_BPO]):
        raise ValueError ("Coloque os valores nas variaveis do ambiente")
except Exception as e:
    print(f"Erro {e}")

pasta_downloads = os.path.expanduser("~/Downloads")
 
def renomear_e_mover_arquivos(pasta_origem, pasta_destino, parametro_nome, novo_nome_base):
    """
    Renomeia e move arquivos que contenham um parâmetro no nome para uma pasta de destino.
 
    :param pasta_origem: Caminho da pasta onde os arquivos estão localizados (ex.: Downloads).
    :param pasta_destino: Caminho da pasta para onde os arquivos serão movidos.
    :param parametro_nome: Texto que deve estar no nome dos arquivos a serem renomeados e movidos.
    :param novo_nome_base: Base do novo nome para os arquivos renomeados.
    """
    
    try:
        # Criar a pasta de destino, se não existir
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)
            print(f"Pasta de destino criada: {pasta_destino}")
 
        # Listar arquivos na pasta de origem
        arquivos = os.listdir(pasta_origem)
        contador = 1  # Contador para evitar nomes duplicados
 
        for arquivo in arquivos:
            caminho_origem = os.path.join(pasta_origem, arquivo)
 
            # Ignorar pastas
            if os.path.isdir(caminho_origem):
                continue
 
            # Verificar se o parâmetro está no nome do arquivo
            if parametro_nome in arquivo:
                # Criar o novo nome do arquivo
                extensao = os.path.splitext(arquivo)[1]  # Pega a extensão do arquivo
                novo_nome = f"{novo_nome_base}{extensao}"
                contador += 1
 
                caminho_destino = os.path.join(pasta_destino, novo_nome)
 
                # Renomear e mover o arquivo
                shutil.move(caminho_origem, caminho_destino)
                print(f"Renomeado e movido: {arquivo} -> {novo_nome}")
 
        print("Renomeação e movimentação concluídas!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
 
#Variaveis Comandos Selenium
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)
driver.maximize_window() #Recomendo desabilitar caso não use monitor secundário

#Keys para chamada mais rápida
Seta_Baixo = Keys.ARROW_DOWN
Enter = Keys.RETURN
Tab = Keys.TAB

#Variaveis Texto 
Agosto = 'agosto' #Mês para geração de relatório retroativo
Setembro = 'setembro' #Mês para geração de relatório retroativo
Outubro = 'outubro' #Mês para geração de relatório retroativo
Novembro = 'novembro' #Mês para geração de relatório retroativo

#Variaveis Data
data_completa = datetime.now()
data_atual = date.today()
data_inicio_mes = datetime(data_atual.year,data_atual.month,1 )
data_inicio_mes_txt = data_inicio_mes.strftime('%d/%m/%Y')
mes_anterior = (data_atual.replace(day=1) - timedelta(days=1)).strftime("%B")
Dia_atual = data_atual.day
Mes_Atual = data_completa.strftime("%B")
Ano_Anterior = data_atual.year - 1 
Ano_Atual = data_atual.year
data_atual_txt = data_atual.strftime('%d/%m/%Y')
data_de_ontem = data_atual - timedelta(days=1) # Convert string back to date and subtract
data_ontem_txt = data_de_ontem.strftime('%d/%m/%Y')
data_finalDeSemana = data_atual - timedelta(days=3)
data_finalDeSemana_txt = data_finalDeSemana.strftime('%d/%m/%y')
InfoData = datetime.now().strftime('%B')
data_arquivo = datetime.now().strftime("%d%m%Y")
data_pasta = datetime.now().strftime("%d-%m-%Y")
data_inicio_Mes_ConsigFacil = data_inicio_mes.strftime('%d%m%Y')
data_final_Mes_ConsigFacil = data_arquivo

def teste_variaveis():

    #Teste Funcionabilidade Variáveis data
    print("Ontem foi dia: ", data_ontem_txt)
    print("O final de semana começou no dia: ", data_finalDeSemana_txt)
    print(data_ontem_txt)
    print(data_inicio_mes_txt)
    print(mes_anterior)
    print(Mes_Atual)
    print(Ano_Anterior)
    print(Ano_Atual)
    print(InfoData)
    print(Dia_atual)
    print("\n")

    #Testa Getenv para verificar se há erros nas variáveis
    print(ZETRA_Username_Values)
    print(ZETRA_Password_Values)
    print(User_CIP)
    print(Senha_CIP)
    print(ConsigFacil_Username_Values)
    print(ConsigFacil_Psw_Values)
    print(Acesso_NeoConsigRJ)
    print(NeoConsig_Username_Values)
    print(Login_BPO)
    print(Senha_BPO)
    print('\n')

    #Testa Variaveis de texto
    print(Agosto)
    print(Outubro)
    print(Novembro)

#Cria pasta pra evitar perder arquivos
renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "Arquivo",
        novo_nome_base= f"Abertura de Pasta_{data_arquivo}"
)

#Logins na ZETRA---------------------------------------------------------
def Relatorios_Zetra():
    #Começa o login na Processadora de EMBU
    driver.get(Proc_EMBU)
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

    #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")
    
    #Começa a geração de relatório
    driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[3]/a").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click()
    
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.clear()
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.clear()
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")
    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    
    time.sleep(3)
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(14)
    
    #Download Relatório
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
 
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_embu_{data_arquivo}"
)
     
    #Começa o login na Processadora da IGPREV
    driver.get(Proc_IGEPREV)
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

    #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")
    
    time.sleep(2)

    #Começa a geração de relatório
    driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[3]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[2]/a").click() #ERRO
    
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")

    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    #Download Relatório
    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_igeprev_{data_arquivo}"
)

    #Começa o login na Processadora do Hospital do Servidor Público de São Paulo
    driver.get(Proc_HospDoServPubSP)
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

        #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")

    #Começa a geração de relatório
    driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[3]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[2]/a").click() #ERRO
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")

    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(7)

    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_hospital_do_servidor_publico_de_sp_{data_arquivo}"
)

    #Começa o login na Processadora da Prefeitura da Serra ES
    driver.get(Proc_Pref_Serra_ES)
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

        #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")

    #Começa a geração de relatório
    driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[3]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click() #ERRO
    
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")

    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    time.sleep(3)

    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)

    #Autorização Gerador
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/form")
    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/button[2]").click()
    time.sleep(7)

    #Download relatório
    time.sleep(7)
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_prefeitura_da_serra_es_{data_arquivo}"
)

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

        #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")
    
    #Começa a geração de relatório
    driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[3]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click() #ERRO
    
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")

    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    driver.execute_script ("document.body.style.zoom='100%'")    
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

    #Download Relatório
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_prefeitura_de_curitiba_{data_arquivo}"
)

    #Começa o login na Processadora de Uberlândia
    driver.get(Proc_PrefUberlandia)
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

    #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")

    #Começa a geração de relatório
    driver.find_element(By.XPATH, '//*[@id="container"]/ul/li[3]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[2]/ul/li[1]/a").click() #ERRO
    
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")

    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)

    #Autorização Gerador

    Senha_Autorizador = driver.find_element(By.ID, "senha2aAutorizacao")
    time.sleep(1)
    Senha_Autorizador.send_keys(ZETRA_Password_Values)
    driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/button[2]").click()
    time.sleep(7)

    time.sleep(7)
    
    #Download Relatório
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_uberlandia_{data_arquivo}"
    )

    #Começa o login na Processadora de SBC
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

        #Segunda chance Captcha
    try:
        driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        UserZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[1]/input")
        UserZetra.send_keys(ZETRA_Username_Values)
        UserZetra.send_keys(Enter)
        PswZetra = driver.find_element(By.XPATH, "/html/body/section/div/div[1]/form/div[3]/input[1]")
        PswZetra.send_keys(ZETRA_Password_Values)
        ZetraCaptcha_Resolver = input("Digite o Captcha: ")
        CaptchaZetra = driver.find_element(By.ID, "captcha")
        CaptchaZetra.send_keys(ZetraCaptcha_Resolver)
        CaptchaZetra.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")

    #Começa a geração de relatório
    driver.find_element(By.XPATH, '/html/body/section/div[2]/div/div/div[1]/div[2]/ul/li[2]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/section/div[2]/div/div/div[1]/div[2]/ul/div[1]/ul/li/a").click() #ERRO
    
    #Data de inclusão/Alteração
    time.sleep(2)
    Selec_data = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[1]/div/div[2]/input")
    Selec_data.send_keys(data_inicio_mes_txt)
    Selec_data_final = driver.find_element(By.XPATH,"/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    Selec_data_final.send_keys(data_atual_txt)

    driver.execute_script ("document.body.style.zoom='33%'")

    #CheckBox

    #Situação servidor
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/fieldset[1]/div[2]/div/div[1]/span/input").click()

    #Fim das checkbox

    #Selecionar tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select").click()
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[1]/div[2]/div/div[11]/select/option[4]").click()

    driver.find_element(By.ID, "btnEnvia").click()
    driver.execute_script ("document.body.style.zoom='100%'")
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
    
    #Download Relatório
    driver.execute_script ("document.body.style.zoom='33%'")
    remenda_Bug = driver.find_element(By.XPATH, "/html/body")
    remenda_Bug.send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, "/html/body/section/div[3]/div/form/div[3]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/div/div/a")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="userMenu"]/div').click()
    driver.find_element(By.XPATH, '//*[@id="dataTables"]/tbody/tr[1]/td[4]/div/div/div/a[1]').click()
    driver.execute_script ("document.body.style.zoom='100%'")

    time.sleep(7)
    
    #Renomeia e move arquivo download
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "consignacoes_",
        novo_nome_base= f"zetra_prefeitura_de_sao_bernardo_do_campo_{data_arquivo}"
)

#Logins na CIP---------------------------------------------------------
def Relatorios_CIP():
    #Começa o login na Processadora do Mato Grosso
    driver.get(Proc_GovPefSP)
    
    #Login no portal
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/span/span").click()
    Insira_User_CIP = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[3]/input")
    Insira_User_CIP.send_keys(User_CIP)
    Insira_Senha_CIP = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[4]/input")
    Insira_Senha_CIP.send_keys(Senha_CIP)
    Cip_Captcha_Resolver = input("Digite o Captcha: ")
    Cip_Captcha = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[5]/div/input")
    Cip_Captcha.send_keys(Cip_Captcha_Resolver)
    Cip_Captcha.send_keys(Enter)
    time.sleep(2)
        #Segunda chance Captcha
    try:
        driver.find_element(By.ID, "captcha")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        Insira_Senha_CIP = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[4]/input")
        Insira_Senha_CIP.send_keys(Senha_CIP)
        Cip_Captcha_Resolver = input("Digite o Captcha: ")
        Cip_Captcha = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/form/div[3]/div/div/div/div[5]/div/input")
        Cip_Captcha.send_keys(Cip_Captcha_Resolver)
        Cip_Captcha.send_keys(Enter)
    except Exception:
        print("Elemento não encontrado!")
    
    time.sleep(2)

    #Seleciona Portal Do Mato Grosso
    driver.find_element(By.CLASS_NAME, "btExpandir").click()
    driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[4]/div[2]/fieldset/div/div[2]/fieldset/span/label").click()
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[2]/div/div[7]/input").click()
    time.sleep(4)
    
    #Seleciona o gerador de relatório no portal
    driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/a/span").click()
    driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/div/div/a").click()
    
    #Seleciona a Opção de Visão do Relatório
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select").click
    Achar_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select")
    Achar_OP_Vis.send_keys(Seta_Baixo)
    Achar_OP_Vis.send_keys(Enter)
    
    #Tempo pro site Carregar
    time.sleep(4)
    
    #Seleciona o Relatório disponível com a opção de visão
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select").click()
    AcharOP_Rel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select")
    AcharOP_Rel.send_keys(Seta_Baixo)
    AcharOP_Rel.send_keys(Enter)
    time.sleep(4)
    
    #Seleciona os orgãos disponíveis pra Orgãos selecionados
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[6]/div/div[2]/span/div[2]/div/button[3]").click()
    
    #Seleciona as espécies disponíveis pra Espécieis selecionadas
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[9]/div/div[2]/span/div[2]/div/button[3]").click()

    #Seleciona Data Inicio & Data Fim
    Selec_Data_Inicio_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[3]/div[1]/input")
    Selec_Data_Inicio_CIP.send_keys(data_inicio_mes_txt)
    Selec_Data_Fim_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[3]/div[3]/input")
    Selec_Data_Fim_CIP.send_keys(data_atual_txt)

    #Seleciona as caixas desejadas pro relatório
    
    #Selecionar Matricula
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[2]/td[2]/input").click()
    #Selecionar CPF
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[3]/td[2]/input").click()
    #Selecionar Nome 
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[7]/td[1]/input").click()
    #Selcionar Nome reduzido do Órgão
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[6]/td[1]/input").click()
    #Selecionar Descrição da espécie
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[3]/td[1]/input").click()
    #Selecionar Número da averbação
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[6]/td[1]/input").click()
    #Selecionar Número do contrato
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[7]/td[1]/input").click()
    #Selecionar situação da averbação
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[9]/td[1]/input").click()
    #Selecionar Qtde de Parcela
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[11]/td[1]/input").click()
    #Selecionar Valor da Parcela
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[12]/td[1]/input").click()
    #Selecionar Valor liberado
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[3]/td[2]/input").click()
    #Selecionar Número da última parcela processada
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[7]/td[2]/input").click()
    #Selecionar Data de início de contrato
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[11]/td[2]/input").click()
    #Selecionar Data da inclusão da averbação
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[13]/td[2]/input").click()
    
    #Fim das checkbox

    #Click Gerar Relatório
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[7]/input[2]").click()
    time.sleep(6)
    
    #Baixar Relatório NA MÃO !
    time.sleep(15)
    
    #Renomeia e move arquivos
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "RA015 - Relatório Customizável de Averbação",
        novo_nome_base= f"cip_mato_grosso_{data_arquivo}"
    )
    time.sleep(5)
    #Volta pra home
    driver.get("https://www.portaldoconsignado.org.br/consignatario/autenticado?74")
    
    # Seleciona Troca de Perfil da CIP 
    driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[3]/a/span").click()
    
    # Abre Box MS 
    driver.find_element(By.CLASS_NAME, "btExpandir").click()
    
    # Abre Box PrefSP  
    driver.find_element(By.CLASS_NAME, "btExpandir").click()
    
    #Começa o login na Processadora da Prefeitura e governo de São Paulo
    driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[5]/div[2]/fieldset/div/div[2]/fieldset/span/label/input").click()
    driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[7]/input").click()
    time.sleep(2)
    
    #Seleciona o gerador de relatório no portal
    driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/a").click()
    driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/div/div/a").click()
    time.sleep(1)
    #Seleciona a Opção de Visão do Relatório
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select").click
    Achar_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select")
    Achar_OP_Vis.send_keys(Seta_Baixo)
    Achar_OP_Vis.send_keys(Enter)
    
    #Tempo pro site Carregar
    time.sleep(4)
    
    #Seleciona o Relatório disponível com a opção de visão
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select").click()
    AcharOP_Rel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select")
    AcharOP_Rel.send_keys(Seta_Baixo)
    AcharOP_Rel.send_keys(Enter)
    time.sleep(4)
    
    #Seleciona os orgãos disponíveis pra Orgãos selecionados
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[6]/div/div[2]/span/div[2]/div/button[3]").click()
    
    #Seleciona as espécies disponíveis pra Espécieis selecionadas
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[9]/div/div[2]/span/div[2]/div/button[3]").click()

    #Seleciona Data Inicio & Data Fim
    Selec_Data_Inicio_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[3]/div[1]/input")
    Selec_Data_Inicio_CIP.send_keys(data_inicio_mes_txt)
    Selec_Data_Fim_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[3]/div[3]/input")
    Selec_Data_Fim_CIP.send_keys(data_atual_txt)

    #Seleciona as caixas desejadas pro relatório
    
    #Selecionar Matricula
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[2]/td[2]/input").click()
    #Selecionar CPF
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[3]/td[2]/input").click()
    #Selecionar Nome 
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[7]/td[1]/input").click()
    #Selcionar Nome reduzido do Órgão
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[6]/td[1]/input").click()
    #Selecionar Descrição da espécie
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[3]/td[1]/input").click()
    #Selecionar Número da averbação
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[6]/td[1]/input").click()
    #Selecionar Número do contrato
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[7]/td[1]/input").click()
    #Selecionar situação da averbação
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[9]/td[1]/input").click()
    #Selecionar Qtde de Parcela
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[11]/td[1]/input").click()
    #Selecionar Valor da Parcela
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[12]/td[1]/input").click()
    #Selecionar Valor liberado
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[3]/td[2]/input").click()
    #Selecionar Número da última parcela processada
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[7]/td[2]/input").click()
    #Selecionar Data de início de contrato
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[11]/td[2]/input").click()
    #Selecionar Data da inclusão da averbação
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[13]/td[2]/input").click()
    
    #Fim das checkbox

    #Click Gerar Relatório
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[7]/input[2]").click()
    time.sleep(6)
    
    #Baixar Relatório NA MÃO !
    time.sleep(15)

    #Renomeia e move arquivos
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "RA015 - Relatório Customizável de Averbação",
        novo_nome_base= f"cip_prefeitura_de_são_paulo_{data_arquivo}"
    )
    time.sleep(5)

    #Volta pra Home
    driver.get("https://www.portaldoconsignado.org.br/consignatario/autenticado?74")
    
    #Seleciona Troca de Perfil CIP  
    driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/div[3]/a/span").click()
    
    # Abre Box MS 
    driver.find_element(By.CLASS_NAME, "btExpandir").click()
    
    # Abre Box PrefSP 
    driver.find_element(By.CLASS_NAME, "btExpandir").click()
    
    # Abre Box SEFAZ 
    driver.find_element(By.CLASS_NAME, "btExpandir").click()
    
    #Começa o login na Processadora da SEFAZ
    driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[6]/div[2]/fieldset/div/div[2]/fieldset/span/label/input").click()
    driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/div/div[7]/input").click()
    time.sleep(3)
    
    #Seleciona o gerador de relatório no portal
    driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/a").click()
    driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div[2]/div/div/a").click()
    time.sleep(1)
    
    #Seleciona a Opção de Visão do Relatório
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select").click
    Achar_OP_Vis = driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[1]/select")
    Achar_OP_Vis.send_keys(Seta_Baixo)
    Achar_OP_Vis.send_keys(Enter)
    
    #Tempo pro site Carregar
    time.sleep(4)
    
    #Seleciona o Relatório disponível com a opção de visão
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select").click()
    AcharOP_Rel = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[4]/div[2]/select")
    AcharOP_Rel.send_keys(Seta_Baixo)
    AcharOP_Rel.send_keys(Enter)
    time.sleep(4)
    
    #Seleciona os orgãos disponíveis pra Orgãos selecionados
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[6]/div/div[2]/span/div[2]/div/button[3]").click()
    
    #Seleciona as espécies disponíveis pra Espécieis selecionadas
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[9]/div/div[2]/span/div[2]/div/button[3]").click()

    #Seleciona Data Inicio & Data Fim
    Selec_Data_Inicio_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[3]/div[1]/input")
    Selec_Data_Inicio_CIP.send_keys(data_inicio_mes_txt)
    Selec_Data_Fim_CIP = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[5]/div[2]/div[3]/div[3]/input")
    Selec_Data_Fim_CIP.send_keys(data_atual_txt)

    #Seleciona as caixas desejadas pro relatório
    
    #Selecionar Matricula
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[2]/td[2]/input").click()
    #Selecionar CPF
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[3]/td[2]/input").click()
    #Selecionar Nome 
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[7]/td[1]/input").click()
    #Selcionar Nome reduzido do Órgão
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[1]/tbody/tr[6]/td[1]/input").click()
    #Selecionar Descrição da espécie
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[3]/td[1]/input").click()
    #Selecionar Número da averbação
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[6]/td[1]/input").click()
    #Selecionar Número do contrato
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[7]/td[1]/input").click()
    #Selecionar situação da averbação
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[9]/td[1]/input").click()
    #Selecionar Qtde de Parcela
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[11]/td[1]/input").click()
    #Selecionar Valor da Parcela
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[12]/td[1]/input").click()
    #Selecionar Valor liberado
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[3]/td[2]/input").click()
    #Selecionar Número da última parcela processada
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[7]/td[2]/input").click()
    #Selecionar Data de início de contrato
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[11]/td[2]/input").click()
    #Selecionar Data da inclusão da averbação
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[6]/div/div[2]/table[3]/tbody/tr[13]/td[2]/input").click()
    
    #Fim das checkbox
    
    #Click Gerar Relatório
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/form/div[4]/div/div[7]/input[2]").click()
    time.sleep(6)
    
    #Baixar Relatório NA MÃO !
    time.sleep(7)

    #Renomeia e move arquivos
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "RA015 - Relatório Customizável de Averbação",
        novo_nome_base= f"cip_sefaz_{data_arquivo}"
    )
    time.sleep(5)

#Logins na CONSIGFACIL---------------------------------------------------------
def Relatorios_ConsigFacil():
#Começa o login na processadora do Pernambuco
    driver.get(Proc_PIAUI)
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
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/button").click()
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)
    
    #Fecha aviso do navegador
    driver.find_element(By.XPATH, "/html/body").click()
    time.sleep(2)
    #Fecha Janela de novidades
    driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div/div[1]/button").click()
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[2]")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[1]").click()
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)
    
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,"/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[3]/a").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[3]/ul/li[2]/a").click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(3)
    
    #Selec Periodo Folha
    driver.execute_script("document.body.style.zoom='50%'")
    time.sleep(1)
    Selec_Data_inicio = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[3]/td[2]/input")
    Selec_Data_inicio.send_keys(data_inicio_Mes_ConsigFacil)
    Selec_Data_Fim = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[3]/td[3]/input")
    Selec_Data_Fim.send_keys(data_final_Mes_ConsigFacil)
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select/option[3]").click()
    element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select/option[3]")
    try:
        element.send_keys(Enter)
    except Exception:
        print("Não consegue interagir com o elemento !")
    time.sleep(3)

    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select/option[2]").click()   
    time.sleep(3)
    element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select/option[2]")
    try:
        element.send_keys(Enter)
    except Exception:
        print("Não consegue interagir com o elemento !")
    time.sleep(3)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]")
    try:
        element.send_keys(Enter)
    except Exception:
        print("Não consegue interagir com o elemento !")
    time.sleep(3)

    #Download Arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(10)
    
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_piaui_{data_arquivo}"
    )

    #Começa o login na processadora do Pernambuco
    driver.get(Proc_GovPernambuco)
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
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/button").click()
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)
    
    #Fecha aviso do navegador
    driver.find_element(By.XPATH, "/html/body").click()
    time.sleep(2)
    #Fecha Janela de novidades
    driver.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[1]/button").click()
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[2]")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[1]").click()
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)
    
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/ul/li[2]/a").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/ul/li[2]/ul/li[2]/a").click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(3)
    
    #Selec Periodo Folha
    Selec_Data_inicio = driver.find_element(By.XPATH,"/html/body/div[2]/div[5]/form/table[2]/tbody/tr[3]/td[2]/input")
    Selec_Data_inicio.send_keys(data_inicio_Mes_ConsigFacil)
    Selec_Data_Fim = driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/form/table[2]/tbody/tr[3]/td[3]/input")
    Selec_Data_Fim.send_keys(data_final_Mes_ConsigFacil)
    time.sleep(3)

    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,"/html/body/div[2]/div[5]/form/table[2]/tbody/tr[9]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/form/table[2]/tbody/tr[9]/td[2]/select/option[2]").click()   
    time.sleep(3)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/form/table[2]/tbody/tr[12]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    
    #Download Arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div[5]/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(10)
    
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_pernambuco_{data_arquivo}"
    )

#Começa o login na processadora do Recife
    driver.get(Proc_PrefRecife)
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
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/button").click()
    except Exception:
        print("Elemento não encontrado!")

    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[2]")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[1]").click()
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)
    
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,"/html/body/div[2]/ul/div[1]/div[2]/div/div/div/li[3]/a").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[2]/ul/div[1]/div[2]/div/div/div/li[3]/ul/li[2]/a").click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(3)
    
    #Selec Folha
    driver.execute_script ("document.body.style.zoom='50%'")
    driver.find_element(By.XPATH, '//*[@id="ordenar"]').click()
    driver.find_element(By.XPATH, '//*[@id="periodo"]/option[3]').click() #Mudar data de acordo com o requerimento (Atualmente: Janeiro 2025)
    time.sleep(3)

    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,'//*[@id="ordenar"]').click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select/option[2]").click()   
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]").click()
    time.sleep(7)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    
    #Download Arquivo
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(10)
    
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_recife_{data_arquivo}"
    )

    #Começa o login na processadora do PortoVelho
    driver.get(Proc_PrefPortoVelho)
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
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/button").click()
    except Exception:
        print("Elemento não encontrado!")

    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[2]")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[3]/div/div/div[3]/button[1]").click()
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)
    
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,'//*[@id="sidebar"]/ul/div[1]/div[2]/div/div/div/li[2]/a').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="objeto_1009"]').click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(3)
    
    #Selec Folha
    driver.execute_script ("document.body.style.zoom='50%'")
    driver.find_element(By.XPATH, '//*[@id="ordenar"]').click()
    driver.find_element(By.XPATH, '//*[@id="periodo"]/option[3]').click() #Mudar data de acordo com o requerimento (Atualmente: Janeiro 2025)
    time.sleep(3)

    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,'//*[@id="ordenar"]').click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select/option[2]").click()   
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]").click()
    time.sleep(7)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    
    #Download Arquivo
    driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(10)
    
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_porto_velho_{data_arquivo}"
    )

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
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
        driver.find_element(By.XPATH, "/html/body/div/div[2]/form/button").click()
    except Exception:
        print("Elemento não encontrado!")

    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
    time.sleep(1)

    try:
        element = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[2]/div/div/div[3]/button[1]")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/div[6]/div[2]/ul/div[2]/div/div/div[3]/button[1]").click()
    except Exception:
        print("Elemento não encontrado!")
    
    

    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,'//*[@id="sidebar"]/ul/div[1]/div[2]/div/div/div/li[6]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[6]/ul/li[2]/a').click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(1)
    driver.execute_script ("document.body.style.zoom='50%'")
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select/option[3]").click() #Mudar para Mês referente do Relatório (Atualmente "Janeiro 2025")
    time.sleep(2)
    
    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select").click()
    Selec_Order_By = driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select")
    Selec_Order_By.send_keys(Seta_Baixo)
    Selec_Order_By.send_keys(Enter)    
    time.sleep(1)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select").click()
    Selec_CSV_arquivo = driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select")
    Selec_CSV_arquivo.send_keys(Seta_Baixo)
    Selec_CSV_arquivo.send_keys(Enter)
    
    #Download Arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)
    
    renomear_e_mover_arquivos(
    pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_governo_de_joao_pessoa_{data_arquivo}"
    )

    #Começa o login na Processadora da prefeitura de Campina Grande
    driver.get(Proc_PrefCampinaGrande)
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
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
    except Exception:
        print("Elemento não encontrado!")
    time.sleep(2)

    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[1]/button").click()
    
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,'//*[@id="sidebar"]/ul/div[1]/div[2]/div/div/div/li[6]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[6]/ul/li[2]/a').click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    time.sleep(2)
    
    #Seleciona tipo de folha
    driver.execute_script ("document.body.style.zoom='50%'")
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[4]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[4]/td[2]/select/option[3]").click()
    
    #Seleciona data folha
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select/option[2]").click() #Mudar para Mês referente do Relatório (Atualmente "Janeiro 2025")
    time.sleep(2)
    
    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select").click()
    Selec_Order_By = driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select")
    Selec_Order_By.send_keys(Seta_Baixo)
    Selec_Order_By.send_keys(Enter)    
    time.sleep(1)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select").click()
    Selec_CSV_arquivo = driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select")
    Selec_CSV_arquivo.send_keys(Seta_Baixo)
    Selec_CSV_arquivo.send_keys(Enter)
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)
    
    #Renomeia e move arquivos
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_prefeitura_de_campina_grande_{data_arquivo}"
    )
    
    #Começa o login na processadora da IPSEM de Campina Grande
    driver.get(Proc_IPSEM_CampinaGrande)
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
    
    try:
        element = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[5]/input")
        # Aqui o código não interage com o elemento, apenas o armazena em uma variável
        print("Elemento encontrado!")
        Segundo_Captcha = input("Captcha digitado errado, tente novamente: ")
        element.send_keys(Segundo_Captcha)
        User_ConsigFacil = driver.find_element (By.ID, "usuario")
        User_ConsigFacil.clear()
        User_ConsigFacil.send_keys(ConsigFacil_Username_Values)
        Psw_ConsigFacil = driver.find_element (By.ID, "senha")
        Psw_ConsigFacil.clear()
        Psw_ConsigFacil.send_keys(ConsigFacil_Psw_Values)
    except Exception:
        print("Elemento não encontrado!")

    time.sleep(1) 
    
    #Fecha Janela de novidades
    driver.find_element(By.XPATH,'//*[@id="modalExibeBanners"]/div/div/div[1]/button').click()
    time.sleep(1)
    
    #SELECIONA A ABA RELATÓRIO
    driver.find_element(By.XPATH,'//*[@id="sidebar"]/ul/div[1]/div[2]/div/div/div/li[6]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '/html/body/div[1]/ul/div[1]/div[2]/div/div/div/li[6]/ul/li[2]/a').click() #SELECIONA O TIPO DE RELATORIO
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    time.sleep(2)
    
    #Seleciona tipo de folha
    driver.execute_script ("document.body.style.zoom='50%'")
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[4]/td[2]/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[4]/td[2]/select/option[2]").click()
    
    #Seleciona data folha
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[5]/td[2]/div/select/option[2]").click() #Mudar para Mês referente do Relatório (Atualmente "Janeiro 2025")
    time.sleep(2)
    
    #Seleciona OrderBy Data
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select").click()
    Selec_Order_By = driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[9]/td[2]/select")
    Selec_Order_By.send_keys(Seta_Baixo)
    Selec_Order_By.send_keys(Enter)    
    time.sleep(1)
    
    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select").click()
    driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[12]/td[2]/select/option[2]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[2]/div/div/div/div/div/form/table[2]/tbody/tr[13]/td/p/input").click()
    driver.execute_script ("document.body.style.zoom='100%'")
    time.sleep(3)
    
    #Renomeia e move arquivos
    renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "relatorio",
        novo_nome_base= f"consigfacil_ipsem_campina_grande_{data_arquivo}"
    )
    time.sleep(2)
    print("Conecte e certifique que está funcional a rede Forticlient")
    time.sleep(20) #Tempo para abrir a conexão Forticlient

#Logins na NEOCONSIG (NECESSÁRIO CONEXÃO FORTICLIENT)---------------------------------------------------------
def Relatorios_NeoConsig():
    #Começa o login na Processadora de Goias
    driver.get(Proc_GovGoias)
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/a/button").click()
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/ul/li[3]/a").click()
    time.sleep(2)
    Login_NeoConsig = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[4]/form/input[1]")
    Login_NeoConsig.send_keys(NeoConsig_Username_Values)
    driver.find_element(By.XPATH,"/html/body/header/nav/div/div[4]/form/div/button").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[1]/div/a/span[1]").click()
    Selec_Conv = driver.find_element(By.XPATH, "/html/body/div[7]/div/input")
    Selec_Conv.send_keys("Goi")
    Selec_Conv.send_keys(Enter)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[2]/select").click()
    Selec_acessNC = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[2]/select")
    Selec_acessNC.send_keys(Seta_Baixo)
    Selec_acessNC.send_keys(Enter)
    NeoConsig_Captcha_Resolver = input ("Digite o Captcha: ")
    NeoConsig_Captcha = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[5]/div[3]/input")
    NeoConsig_Captcha.send_keys(NeoConsig_Captcha_Resolver)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[6]/a").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/p/a").click()
    time.sleep(10) # Tempo pra colocar a senha no teclado digital
    time.sleep(3)
    
    #Seleciona Aba Relatórios
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/a").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/a").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/ul/li/a").click()
    time.sleep(5)
    
    #Selecionando Mês 
    driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]/div/div/a/span[1]").click()
    if Dia_atual >= 2:
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
        Selec_Mes_Desejado.send_keys(Mes_Atual) #Default Mes_Atual
        Selec_Mes_Desejado.send_keys(Enter)
    else:
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
        Selec_Mes_Desejado.send_keys(mes_anterior) #Default mes_anterior
        Selec_Mes_Desejado.send_keys(Enter)

    #Seleciona ANO
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a/span[1]").click    
    if InfoData == 'janeiro' and Dia_atual < 2:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
        Selec_Ano_Desejado.send_keys(Ano_Anterior) # default Ano_anterior
        Selec_Ano_Desejado.send_keys(Enter)
    else:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
        Selec_Ano_Desejado.send_keys(Ano_Atual) #Default Ano_Atual
        Selec_Ano_Desejado.send_keys(Enter)
    
    #Tempo carregamento das informações 
    time.sleep(2)
    time.sleep(4)
    
    #Download Relatório
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/a[2]").click()
    time.sleep(30)

    #Renomeia e move arquivo
    renomear_e_mover_arquivos(
    pasta_origem= pasta_downloads,
    pasta_destino= rf"C:\Relatórios\{data_pasta}",
    parametro_nome= "operacaoEmprestimo",
    novo_nome_base= f"neoconsig_governo_de_goias_{data_arquivo}"
    )
    time.sleep(5)
    
    #Começa o login na Processadora de Alagoas
    driver.get(Proc_Alagoas)
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/a/button").click()
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/ul/li[3]/a").click()
    time.sleep(2)
    Login_NeoConsig = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[4]/form/input[1]")
    Login_NeoConsig.send_keys(NeoConsig_Username_Values)
    time.sleep(4)
    driver.find_element(By.XPATH,"/html/body/header/nav/div/div[4]/form/div/button").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[1]/div/a/span[1]").click()
    Selec_Conv = driver.find_element(By.XPATH, "/html/body/div[7]/div/input")
    Selec_Conv.send_keys("alag")
    Selec_Conv.send_keys(Enter)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[2]/select").click()
    Selec_acessNC = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[2]/select")
    Selec_acessNC.send_keys(Seta_Baixo)
    Selec_acessNC.send_keys(Enter)
    NeoConsig_Captcha_Resolver = input ("Digite o Captcha: ")
    NeoConsig_Captcha = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[5]/div[3]/input")
    NeoConsig_Captcha.send_keys(NeoConsig_Captcha_Resolver)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[6]/a").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/p/a").click()
    time.sleep(10) # Tempo pra colocar a senha no teclado digital
    
    #Seleciona Aba Relatórios
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/a").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/a").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/ul/li/a").click()
    time.sleep(5)
    
    #Selecionando Mês 
    driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]/div/div/a/span[1]").click()
    if Dia_atual >= 2:
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
        Selec_Mes_Desejado.send_keys(Mes_Atual) #Default Mes_Atual
        Selec_Mes_Desejado.send_keys(Enter)
    else:
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
        Selec_Mes_Desejado.send_keys(mes_anterior) #Default mes_anterior
        Selec_Mes_Desejado.send_keys(Enter)

    #Seleciona ANO
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a/span[1]").click        
    if InfoData == 'janeiro' and Dia_atual < 2:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
        Selec_Ano_Desejado.send_keys(Ano_Anterior) # default Ano_anterior
        Selec_Ano_Desejado.send_keys(Enter)
    else:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
        Selec_Ano_Desejado.send_keys(Ano_Atual) #Default Ano_Atual
        Selec_Ano_Desejado.send_keys(Enter)
    #Tempo pra processar as informações
    time.sleep(2)
    time.sleep(4)
    
    #Download relatório
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/a[2]").click()
    time.sleep(30)

    #Renomeia e move arquivo
    renomear_e_mover_arquivos(
    pasta_origem= pasta_downloads,
    pasta_destino= rf"C:\Relatórios\{data_pasta}",
    parametro_nome= "operacaoEmprestimo",
    novo_nome_base= f"neoconsig_governo_de_alagoas{data_arquivo}"
    )
    time.sleep(5)

    #Começa o login na Processadora de Sorocaba
    driver.get(Proc_Sorocaba)
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/a/button").click()
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/ul/li[3]/a").click()
    time.sleep(2)
    Login_NeoConsig = driver.find_element(By.XPATH, "/html/body/header/nav/div/div[4]/form/input[1]")
    Login_NeoConsig.send_keys(NeoConsig_Username_Values)
    time.sleep(4)
    driver.find_element(By.XPATH,"/html/body/header/nav/div/div[4]/form/div/button").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[1]/div/a/span[1]").click()
    Selec_Conv = driver.find_element(By.XPATH, "/html/body/div[7]/div/input")
    Selec_Conv.send_keys("soroc")
    Selec_Conv.send_keys(Enter)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[2]/select").click()
    Selec_acessNC = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[2]/select")
    Selec_acessNC.send_keys(Seta_Baixo)
    Selec_acessNC.send_keys(Enter)
    NeoConsig_Captcha_Resolver = input ("Digite o Captcha: ")
    NeoConsig_Captcha = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[5]/div[3]/input")
    NeoConsig_Captcha.send_keys(NeoConsig_Captcha_Resolver)
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/form/div[6]/a").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[1]/p/a").click()
    time.sleep(15) # Tempo pra colocar a senha no teclado digital
    
    #Seleciona Aba Relatórios
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/a").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/a").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[5]/ul/li/ul/li[2]/a").click()
    time.sleep(5)
    
    #Selecionando Mês 
    driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]/div/div/a/span[1]").click()
    if Dia_atual >= 2:
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
        Selec_Mes_Desejado.send_keys(Mes_Atual) #Default Mes_Atual
        Selec_Mes_Desejado.send_keys(Enter)
    else:
        Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
        Selec_Mes_Desejado.send_keys(mes_anterior) #Default mes_anterior
        Selec_Mes_Desejado.send_keys(Enter)

    #Seleciona ANO
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a/span[1]").click        
    if InfoData == 'janeiro' and Dia_atual < 2:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
        Selec_Ano_Desejado.send_keys(Ano_Anterior) # default Ano_anterior
        Selec_Ano_Desejado.send_keys(Enter)
    else:
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
        Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
        Selec_Ano_Desejado.send_keys(Ano_Atual) #Default Ano_Atual
        Selec_Ano_Desejado.send_keys(Enter)

    #Tempo para processamento das informações
    time.sleep(2)
    time.sleep(4)

    #Download Relatório
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/a[2]").click()
    time.sleep(30)

    #Renomeia e move arquivo
    renomear_e_mover_arquivos(
    pasta_origem= pasta_downloads,
    pasta_destino= rf"C:\Relatórios\{data_pasta}",
    parametro_nome= "operacaoEmprestimo",
    novo_nome_base= f"neoconsig_governo_de_sorocaba{data_arquivo}"
    )
    time.sleep(5)

#Logins Consig (Necessário Conexão FortiClient)
def Relatorios_ConsigPR():
    #Login Processadora Paraná 
    driver.get(Proc_Parana)
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/a/button").click()
    driver.find_element(By.XPATH, "/html/body/header/nav/div/div[2]/ul/li/ul/li[3]/a").click()
    Insert_Login_PR = driver.find_element(By.XPATH, '//*[@id="login"]')
    Insert_Login_PR.send_keys(Acesso_NeoConsigRJ)
    Insert_Login_PR.send_keys(Enter)
    time.sleep(10)
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
    time.sleep(15) #Tempo pra colocar a senha no teclado digital
    
    #Seleciona Aba Relatórios
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[1]/div/button").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[4]/a").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[4]/ul/li/a").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[4]/ul/li/ul/li[4]/a").click()
    time.sleep(3)
    
    #Seleciona Mês  
    driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]/div/div/a/span[1]").click()
    if Dia_atual >= 2:
            Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
            Selec_Mes_Desejado.send_keys(Mes_Atual) #Default Mes_Atual
            Selec_Mes_Desejado.send_keys(Enter)
    else:
            Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
            Selec_Mes_Desejado.send_keys(mes_anterior) #Default mes_anterior
            Selec_Mes_Desejado.send_keys(Enter)
    time.sleep(2)

    #Seleciona ANO
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a/span[1]").click       
    if InfoData == 'janeiro' and Dia_atual < 2:
            driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
            Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
            Selec_Ano_Desejado.send_keys(Ano_Anterior) # default Ano_anterior
            Selec_Ano_Desejado.send_keys(Enter)
    else:
            driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
            Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
            Selec_Ano_Desejado.send_keys(Ano_Atual) #Default Ano_Atual
            Selec_Ano_Desejado.send_keys(Enter)
    time.sleep(2)

    #Seleciona Tipo de arquivo
    driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/a[2]").click()
    time.sleep(10)
    
    #Renomeia e move arquivo
    renomear_e_mover_arquivos(
    pasta_origem= pasta_downloads,
    pasta_destino= rf"C:\Relatórios\{data_pasta}",
    parametro_nome= "operacaoEmprestimo",
    novo_nome_base= f"neoconsig_governo_do_parana_{data_arquivo}"
    )

    #FECHA CONEXÃO FORTICLIENT
    print("Fechar conexão com a VPN")
    time.sleep(20)

#Logins na NeoConsig (Sem necessidade de conexão Forticlient)---------------------------------------------------------
def Relatorios_ProcRJ():
        #Começa o login na Processadora do Rio De Janeiro
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
        
        #Abre a aba de relatório
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[4]/a/span[1]").click()
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[4]/ul/li/a").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/ul/li[4]/ul/li/ul/li/a").click()
        driver.get("https://rioconsig.com.br/rioconsig/credenciado/operacao/listar")
        time.sleep(3)
        
        #Selecionando Mês 
        driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[1]/div/div/a/span[1]").click()
        if Dia_atual >= 2:
            Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
            Selec_Mes_Desejado.send_keys(Mes_Atual) #Default Mes_Atual
            Selec_Mes_Desejado.send_keys(Enter)
        else:
            Selec_Mes_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen1_search"]')
            Selec_Mes_Desejado.send_keys(mes_anterior) #Default mes_anterior
            Selec_Mes_Desejado.send_keys(Enter)

        #Seleciona ANO
        driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a/span[1]").click       
        if InfoData == 'janeiro' and Dia_atual < 2:
            driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
            Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
            Selec_Ano_Desejado.send_keys(Ano_Anterior) # default Ano_anterior
            Selec_Ano_Desejado.send_keys(Enter)
        else:
            driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div/div/a").click()
            Selec_Ano_Desejado = driver.find_element(By.XPATH, '//*[@id="s2id_autogen2_search"]')
            Selec_Ano_Desejado.send_keys(Ano_Atual) #Default Ano_Atual
            Selec_Ano_Desejado.send_keys(Enter)
        time.sleep(2)

        #Seleciona Arquivo CSV Export
        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div/div[1]/div[3]/div[3]/div/div/div/a[2]').click()
        time.sleep(25)
         
        #Renomeia e move arquivo
        renomear_e_mover_arquivos(
        pasta_origem= pasta_downloads,
        pasta_destino= rf"C:\Relatórios\{data_pasta}",
        parametro_nome= "operacaoEmprestimo",
        novo_nome_base= f"neoconsig_prefeitura_do_rio_de_janeiro{data_arquivo}"
        )

#Login BPO e extração de relatório (Se Necessário)---------------------------------------------------------
def Relatorios_BPO():
    driver.get(BPO)
    User_BPO = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[3]/input")
    User_BPO.send_keys(Login_BPO)
    Psw_BPO = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[4]/input")
    Psw_BPO.send_keys(Senha_BPO)
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/input").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[2]/div/div/div[2]/ul/li[4]/a").click()
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[2]/div/div/div[2]/ul/li[4]/div/a[1]").click()
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[3]/div/div[1]/div[3]/div/label/table/tbody/tr/td[2]/label").click()
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[3]/div/div[1]/div[5]/div/div/select").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/form/div[3]/div/div[3]/div/div[1]/div[6]/div/div/a[2]").click()
    time.sleep(45)

    #Renomeia e move arquivos
    renomear_e_mover_arquivos(
    pasta_origem= pasta_downloads,
    pasta_destino= r"C:\Relatórios\BPO",
    parametro_nome= "RelatorioProducaoAnalitico",
    novo_nome_base= f"Relatório_Analítico_BPO_{data_arquivo}"
    )

    time.sleep(5)
#------------------ Chama as funções para gerar relatórios --------------------------------

teste_variaveis()

Relatorios_Zetra() #100% Funcional Relatório Definitivo

Relatorios_CIP() # 100% Funcional Relatório Definitivo

Relatorios_ConsigFacil() #90% Funcional (Falta reset Maranhão) 

RodarProcsVPN = input("Digite 's' se deseja rodar as processadoras que necessitam de VPN ou 'n' para pular\n")

#100% Funcional Relatório Definitivo (Falta acesso Alagoas e Sorocaba)
if RodarProcsVPN == 's':
    Relatorios_NeoConsig() # Precisa ser feito conectado a forticlient 
    Relatorios_ConsigPR() # Precisa ser feito conectado a forticlient
elif RodarProcsVPN =='n':
    print("Pulando para a processadora do Rio de Janeiro")
elif RodarProcsVPN == 'S':
    Relatorios_NeoConsig() # Precisa ser feito conectado a forticlient
    Relatorios_ConsigPR() # Precisa ser feito conectado a forticlient
elif RodarProcsVPN =='N':
    print("Pulando para a processadora do Rio de Janeiro")
else:
    print("")

Relatorios_ProcRJ() #100% Funcional Relatório Definitivo

Relatorios_BPO() #100% Funcional Relatório Definitivo