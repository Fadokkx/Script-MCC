import os
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import psycopg2
import locale
import shutil
from datetime import date, timedelta, datetime

#Define Locale
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

#Define valores datetime
data_atual = date.today()
data_atual_postgres = data_atual.strftime('%Y-%m-%d')
data_Pasta_Arquivo = data_atual.strftime('%d-%m-%Y')
Data_e_HoraLOG = datetime.now()

#Tenta conexão com o postgre
try:
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("User_Postgres")
    db_password = os.getenv("Senha_Postgres")

        # Confirma que os valores estão inseridos no ambiente do sistema
    if not all([db_host, db_name, db_user, db_password]):
        raise ValueError("Insira valores do banco de dados nas variaveis de ambiente")
    
    # Conecta com o Banco de dados usando as variaveis do ambiente de sistema
    conexao = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        options="-c client_encoding=UTF8"
    )
    # Cria um cursor para execução de Querys
    SQL = conexao.cursor()
except Exception as e:
    print(f"Unable to connect to the database: {e}")

#Função para mover os arquivos editados
def renomear_e_mover_arquivos(pasta_origem, pasta_destino, parametro_nome, novo_nome_base):
    try:
        #Criar a pasta de destino se não existir
        os.makedirs(pasta_destino, exist_ok=True)

        #Listar arquivos na pasta de origem
        arquivos = os.listdir(pasta_origem)
        contador = 1

        for arquivo in arquivos:
            caminho_origem = os.path.join(pasta_origem, arquivo)

            #Ignorar pastas
            if os.path.isdir(caminho_origem):
                continue

            #Verificar se o parâmetro está no nome do arquivo
            if parametro_nome in arquivo:
                #Criar o novo nome do arquivo
                extensao = os.path.splitext(arquivo)[1]  # Pega a extensão do arquivo
                novo_nome = f"{novo_nome_base}_{contador}{extensao}"
                caminho_destino = os.path.join(pasta_destino, novo_nome)

                # Se o arquivo com o novo nome já existe incrementa o contador
                while os.path.exists(caminho_destino):
                    contador += 1
                    novo_nome = f"{novo_nome_base}_{contador}{extensao}"
                    caminho_destino = os.path.join(pasta_destino, novo_nome)

                # Renomear e mover o arquivo
                shutil.move(caminho_origem, caminho_destino)
                print(f"Renomeado e movido: {arquivo} -> {novo_nome}")

                # Incrementa o contador para o próximo arquivo
                contador += 1

        print("Renomeação e movimentação concluídas!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

#Pagamento de Boleto
def salvar_arquivo_Log_Erro_Boleto(conteudo, nome_arquivo=f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de erro
        diretorio_erro = rf"C:\Automatização_Script\Script-MCC\Logs\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_erro, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:  # Alterado para "a" (append)
            # Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"\n{conteudo}\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def salvar_arquivo_Log_Sucesso_Boleto(conteudo, nome_arquivo=f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}.txt"):
    try:
        #Define o caminho para salvar o arquivo
        diretorio_sucesso = rf"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso"
        
        #Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        #Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_sucesso, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def MonitoraPagamentoBoleto():

    hora_log = datetime.now()
    conteudo_sucesso = ""
    conteudo_erro = ""
    
    SQL.execute("""
        SELECT t.id, u.name, u.document, t.description, t.value, DATE(t.created_at) AS created_at, 
             i.total_value, t.invoice_id, a."limit", t.invoice_id
        FROM public.transaction as t 
        INNER JOIN public.invoice as i ON t.invoice_id = i.id
        INNER JOIN public.account as a ON t.account_id = a.id
        INNER JOIN public.user as u ON a.user_id = u.id
        WHERE t.description LIKE %s
        ORDER BY t.created_at DESC 
        LIMIT 5;
    """, ('%Pagamento de Boleto%',))
    
    leituraPagBoleto = SQL.fetchall()

    #Lança Query mais completa para sair a data completa com a hora da transação no TXT
    SQL.execute("""
        SELECT t.id, u.name, u.document, t.description, t.value, t.created_at, 
        i.total_value, t.invoice_id, a."limit", t.invoice_id
        FROM public.transaction as t 
        INNER JOIN public.invoice as i ON t.invoice_id = i.id
        INNER JOIN public.account as a ON t.account_id = a.id
        INNER JOIN public.user as u ON a.user_id = u.id
        WHERE t.description LIKE %s
        ORDER BY t.created_at DESC 
        LIMIT 5;
    """, ('%Pagamento de Boleto%',))
    
    DadosPagBoleto = SQL.fetchall()

    for row in leituraPagBoleto:
        if str(row[5]) == str(data_atual_postgres):
            conteudo_sucesso += f"Data & hora do Log: {hora_log}\n\n"
            print("Pagamento de boleto muito possivelmente funcional !")
            for boleto in DadosPagBoleto:
                if boleto[0] == row[0]: 
                    conteudo_sucesso += f"\n\nID: {boleto[0]}, Nome: {boleto[1]}, CPF: {boleto[2]}, Descrição: {boleto[3]}, Valor: {boleto[4]}, Data: {boleto[5]}, Valor Fatura: {boleto[6]}\n\n"
        else:
            conteudo_erro += f"Data & hora do Log: {hora_log}\n\n"
            print("Pagamento de boleto muito possivelmente com erro !")
            for boleto in DadosPagBoleto:
                if boleto[0] == row[0]:
                    conteudo_erro += f"\n\nID: {boleto[0]}, Nome: {boleto[1]}, CPF: {boleto[2]}, Descrição: {boleto[3]}, Valor: {boleto[4]}, Data: {boleto[5]}, Valor Fatura: {boleto[6]}\n\n"

    if conteudo_erro:
        salvar_arquivo_Log_Erro_Boleto(conteudo= conteudo_erro)
    
    if conteudo_sucesso:
        salvar_arquivo_Log_Sucesso_Boleto(conteudo=conteudo_sucesso)

    if conteudo_sucesso:
        renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso" ,
                pasta_destino= rf"C:\LogsAutomatizacao\LogsSucesso\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Sucesso_Pagamento_boleto_",
                novo_nome_base= f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}"
                )
    if conteudo_erro:
        renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsErro" ,
                pasta_destino= rf"C:\LogsAutomatizacao\LogsErro\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Erro_Pagamento_boleto_",
                novo_nome_base= f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}"
                )

#Onboarding
def salvar_arquivo_Log_Sucesso_Onboarding(conteudo, nome_arquivo=f"Log_Sucesso_Onboarding_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_sucesso = rf"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_sucesso, nome_arquivo)

        # Abre o arquivo para escrita (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Escreve o conteúdo no arquivo
            #Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n"))
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Aplica a função de correção
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def salvar_arquivo_Log_Erro_Onboarding(conteudo, nome_arquivo=f"Log_Erro_Onboarding_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_erro = rf"C:\Automatização_Script\Script-MCC\Logs\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_erro, nome_arquivo)

        # Abre o arquivo para escrita (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Escreve o conteúdo no arquivo
             #Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n"))
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def MonitoraOnboarding():
    # Variáveis para armazenar os logs de sucesso e erro
    hora_log = datetime.now()
    conteudo_sucesso = ""
    conteudo_erro = ""
   
   #Lança Query para puxar do Postgre os resultados de clientes parados no Onboarding ordenados por erro.
    SQL.execute("""select 
    case o.type
    when 0 then 'Completo'
    end "Tipo",
    COALESCE(pu.description,pl.description) "Convênio",
    o.Document "Cpf",
    u.Name "Nome",
    u.margin_card,
    o.created_at "Iniciado Em",
    etapaAtual.discriminator AS "Etapa Atual",
    etapaAtual.created_at "Etapa Em",
    u.phone_number "Telefone",
    ( select value from hangfire.job j
    inner join hangfire.jobparameter jp on j.id = jp.jobid and name = 'message' and statename = 'Succeeded'
    where arguments::text like concat('%', o.id ,'%') and invocationdata::text not like '%Complete%'  order by j.id desc limit 1
    ) as "Erro",
    o.id "ID Onboarding",
    etapaAtual.id "ID Etapa Atual"
 
    From public.onboarding o
    inner join public.user u on o.document = u.document
    left join public.public_agency pu on u.public_agency_id = pu.id
    left join public.lead l on l.document = u.document
    left join public.public_agency pl on l.public_agency_id = pl.id
    left join lateral
    (
    select os.* from public.onboarding_evolutions oe 
    inner join  public.onboarding_steps os on oe.step_for_internal_id = os.id
    where oe.onboarding_id = o.Id and os.discriminator <> 'start' order by oe.created_at desc limit 1
    ) as etapaAtual on o.id = etapaAtual.onboarding_id 
    Where etapaAtual.is_background = true
    and (etapaAtual.created_at + interval '5 minutes') < (timezone('utc', now()) - interval '3 hours')
    Order By "Erro"
    LIMIT 10;
    """)

    leituraOnboarding = SQL.fetchall()
    
    #Procura por erro o resultado da query 
    for row in leituraOnboarding:
        if str(row[9]) == str("None"):
            conteudo_sucesso += f"Data & hora do Log: {hora_log}\n\n"
            print("Sem erros encontrados")
            conteudo_sucesso+= f"\nTipo: {row[0]}, Convênio: {row[1]}, CPF: {row[2]}, Nome: {row[3]}, Margem de cartão: {row[4]}, Iniciado em: {row[5]}, Etapa atual: {row[6]}, Etapa em: {row[7]}, Telefone: {row[8]}, Erro: {row[9]}\n\n"
        else:
            conteudo_erro += f"Data & hora do Log: {hora_log}\n\n"
            print("Onboarding com erros")
            conteudo_erro += f"\nTipo: {row[0]}, Convênio: {row[1]}, CPF: {row[2]}, Nome: {row[3]}, Margem de cartão: {row[4]}, Iniciado em: {row[5]}, Etapa atual: {row[6]}, Etapa em: {row[7]}, Telefone: {row[8]}, Erro: {row[9]}\n\n"
                    
    if conteudo_sucesso:
        salvar_arquivo_Log_Sucesso_Onboarding(conteudo= conteudo_sucesso, nome_arquivo=f"Log_Sucesso_onboarding_{data_Pasta_Arquivo}.txt")
    
    if conteudo_erro:
            salvar_arquivo_Log_Erro_Onboarding(conteudo=conteudo_erro, nome_arquivo= f"Log_Erro_onboarding_{data_Pasta_Arquivo}.txt")

    if conteudo_erro:
        renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsErro",
                pasta_destino= rf"C:\LogsAutomatizacao\LogsErro\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Erro_onboarding_",
                novo_nome_base= f"Log_Erro_Onboarding_{data_Pasta_Arquivo}"
                )
    
    if conteudo_sucesso:
         renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso" ,
                pasta_destino= rf"C:\LogsAutomatizacao\LogsSucesso\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Sucesso_Onboarding_",
                novo_nome_base= f"Log_Sucesso_Onboarding_{data_Pasta_Arquivo}"
         )
        
    print("Log da leitura do Onboarding foi enviado para a pasta de Logs")

#Ativação de Cartão
def salvar_arquivo_Log_Sucesso_Cartao(conteudo, nome_arquivo=f"Log_Sucesso_Cartão_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_sucesso = rf"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_sucesso, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:  # Alterado para "a" (append)
            # Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def salvar_arquivo_Log_Erro_Cartao(conteudo, nome_arquivo=f"Log_Erro_Ativa_cartao_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de erro
        diretorio_erro = rf"C:\Automatização_Script\Script-MCC\Logs\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_erro, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Cabeçalho
            file.write("\nId | Nome | Cpf | Descrição | Valor | Data & hora | Valor da fatura\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"\n{conteudo}\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def MonitoraAtivaCartao():
    # Variáveis para armazenar os logs de sucesso e erro
    hora_log = datetime.now()
    conteudo_sucesso = ""
    conteudo_erro = ""

    SQL.execute("""
    SELECT a.id, c.id, u.name, u.document, a.limit, c.person_id, c.card_id, c.number, c.discriminador, c.proposal_number, DATE(c.approved_at) AS approved_at, c.refused_at, c.canceled_at, c.blocked_at, u.margin_card
    FROM public.card as c
    INNER JOIN public.account as a on c.account_id = a.id
    INNER JOIN public.user as u on a.user_id = u.id
    WHERE approved_at IS NOT Null
    ORDER  BY approved_at DESC
    LIMIT 5;
    """)
    
    LeituraAtivaCartao = SQL.fetchall()

    SQL.execute( """
    SELECT a.id, c.id, u.name, u.document, a.limit, c.person_id, c.card_id, c.number, c.discriminador, c.proposal_number, c.approved_at, c.refused_at, c.canceled_at, c.blocked_at, u.margin_card
    FROM public.card as c
    INNER JOIN public.account as a on c.account_id = a.id
    INNER JOIN public.user as u on a.user_id = u.id
    --WHERE u.document = '51704145449'
    WHERE approved_at IS NOT Null
    ORDER  BY approved_at DESC
    LIMIT 5;
    """)

    DadosAtivaCartao = SQL.fetchall()
    for row in LeituraAtivaCartao:
        if str(row[10]) != str(data_atual_postgres):
            conteudo_erro += f"Data & hora do Log: {hora_log}\n\n"
            print("Criação de cartão provavelmente com erro")
            for row in DadosAtivaCartao:
                conteudo_erro += f"\nID da conta: {row[0]}, ID do usuário: {row[1]}, Nome: {row[2]}, CPF: {row[3]}, Limite: {row[4]}, ID_Dock: {row[5]}, ID do Cartão: {row[6]}, Número do Cartão: {row[7]}, Discriminador: {row[8]}, Número da proposta: {row[9]}, Aprovado em: {row[10]}, Recusado em: {row[11]}, Cancelado em: {row[12]}, Bloqueado em: {row[13]}, Margem Cartão: {row[14]}\n"
        else:
            conteudo_sucesso += f"Data & hora do Log: {hora_log}\n\n"
            print("Criação de Cartão provavelmente funcional")
            for row in DadosAtivaCartao:
                conteudo_sucesso += f"\nID da conta: {row[0]}, ID do usuário: {row[1]}, Nome: {row[2]}, CPF: {row[3]}, Limite: {row[4]}, ID_Dock: {row[5]}, ID do Cartão: {row[6]}, Número do Cartão: {row[7]}, Discriminador: {row[8]}, Número da proposta: {row[9]}, Aprovado em: {row[10]}, Recusado em: {row[11]}, Cancelado em: {row[12]}, Bloqueado em: {row[13]}, Margem Cartão: {row[14]}\n"
    
    if conteudo_sucesso:
        salvar_arquivo_Log_Sucesso_Cartao(conteudo= conteudo_sucesso, nome_arquivo=f"Log_Sucesso_Ativa_Cartão_{data_Pasta_Arquivo}.txt")
    
    if conteudo_erro:
            salvar_arquivo_Log_Erro_Cartao(conteudo=conteudo_erro, nome_arquivo= f"Log_Erro_Ativa_Cartão_{data_Pasta_Arquivo}.txt")

    if conteudo_erro:
        renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsErro",
                pasta_destino= rf"C:\LogsAutomatizacao\LogsErro\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Erro_Ativa_Cartão_",
                novo_nome_base= f"Log_Erro_Ativa_Cartão_{data_Pasta_Arquivo}"
                )
    
    if conteudo_sucesso:
         renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso" ,
                pasta_destino= rf"C:\LogsAutomatizacao\LogsSucesso\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Sucesso_Ativa_Cartão_",
                novo_nome_base= f"Log_Sucesso_Ativa_Cartão_{data_Pasta_Arquivo}"
         )

#Compras com cartão
def salvar_arquivo_Log_Erro_Compra(conteudo, nome_arquivo=f"Log_Erro_compra_cartao_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de erro
        diretorio_erro = rf"C:\Automatização_Script\Script-MCC\Logs\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_erro, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Cabeçalho
            file.write("\nId | Nome | Cpf | Descrição | Valor | Data & hora | Valor da fatura\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"\n{conteudo}\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def salvar_arquivo_Log_Sucesso_Compra(conteudo, nome_arquivo=f"Log_Sucesso_Compra_Cartao_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_sucesso = rf"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_sucesso, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:  # Alterado para "a" (append)
            # Data e hora da execução
            file.write(f"Data e hora que o script rodou: {Data_e_HoraLOG}\n\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_arquivo)
            file.truncate()
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def MonitoraCompraCartao():
    hora_log = datetime.now()
    conteudo_sucesso=""
    conteudo_erro=""

    #Query pra ler os dados da compra com cartão
    SQL.execute("""
    SELECT t.id, u.name, u.document, t.description, t.value, DATE(t.created_at) AS created_at, 
    i.situation, i.total_value, i.due_date,t.invoice_id, a."limit", t.pay_load
    FROM public.transaction as t 
    INNER JOIN public.invoice as i on t.invoice_id = i.id
    INNER JOIN public.account as a on t.account_id = a.id
    INNER JOIN public.user as u on a.user_id = u.id
    ORDER  BY t.created_at DESC
    LIMIT 10;
    """)

    LeituraCompra = SQL.fetchall()

    SQL.execute("""
        --Consulta transações
        SELECT t.id, u.name, u.document, t.description, t.value, t.accumulated_value, t.created_at
        , i.situation, i.total_value, i.due_date,t.invoice_id, a."limit", t.pay_load
        FROM public.transaction as t 
        INNER JOIN public.invoice as i on t.invoice_id = i.id
        INNER JOIN public.account as a on t.account_id = a.id
        INNER JOIN public.user as u on a.user_id = u.id
        ORDER  BY t.created_at DESC
        LIMIT 10;
        """)

    DadosCompra = SQL.fetchall()

    for row in LeituraCompra:
        if str (row[6]) == str(data_atual_postgres):
            conteudo_sucesso += f"{hora_log}\n\n"
            print(f"Última compra feita: {row[6]}")
            for row in DadosCompra:
                 if compraId [0] == row[0]:
                    conteudo_sucesso += f"\nID: {row[0]}, Nome: {row[1]}, CPF: {row[2]}, Estabelecimento da compra: {row[3]}, Valor {row[4]}, Data: {row[6]}"
        else:
            conteudo_sucesso += f"{hora_log}\n\n"
            print(f"Última compra: {row[6]}")
            for compraId in DadosCompra:
                conteudo_erro += f"\nID: {row[0]}, Nome: {row[1]}, CPF: {row[2]}, Estabelecimento da compra: {row[3]}, Valor {row[4]}, Data: {row[6]}"
    
    if conteudo_sucesso:
        salvar_arquivo_Log_Sucesso_Compra(conteudo= conteudo_sucesso, nome_arquivo=f"Log_Sucesso_Compra_Cartao_{data_Pasta_Arquivo}.txt")
    
    if conteudo_erro:
        salvar_arquivo_Log_Erro_Compra(conteudo=conteudo_erro, nome_arquivo= f"Log_Erro_Compra_Cartao_{data_Pasta_Arquivo}.txt")

    if conteudo_erro:
        renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsErro",
                pasta_destino= rf"C:\LogsAutomatizacao\LogsErro\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Erro_Compra_Cartao_",
                novo_nome_base= f"Log_Erro_Compra_Cartao_{data_Pasta_Arquivo}"
                )
    
    if conteudo_sucesso:
         renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso" ,
                pasta_destino= rf"C:\LogsAutomatizacao\LogsSucesso\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Sucesso_Compra_Cartao_",
                novo_nome_base= f"Log_Sucesso_Compra_Cartao_{data_Pasta_Arquivo}"
         )


#Agenda o run das funções
agenda = BlockingScheduler()
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=10, minute=10)
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=11, minute=00)   
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=12, minute=00)  
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=13, minute=00)
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=14, minute=00)
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=15, minute=00)
agenda.add_job(MonitoraPagamentoBoleto, 'cron', hour=16, minute=00)

agenda.add_job(MonitoraOnboarding, 'cron', hour=10, minute=30)
agenda.add_job(MonitoraOnboarding, 'cron', hour=11, minute=30)
agenda.add_job(MonitoraOnboarding, 'cron', hour=12, minute=30)
agenda.add_job(MonitoraOnboarding, 'cron', hour=13, minute=30)
agenda.add_job(MonitoraOnboarding, 'cron', hour=14, minute=30)
agenda.add_job(MonitoraOnboarding, 'cron', hour=15, minute=30)
agenda.add_job(MonitoraOnboarding, 'cron', hour=16, minute=00)
agenda.add_job(MonitoraOnboarding, 'cron', hour=17, minute=30)

agenda.add_job(MonitoraAtivaCartao, 'cron', hour=10, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=11, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=12, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=13, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=14, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=15, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=16, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=17, minute=00)
agenda.add_job(MonitoraAtivaCartao, 'cron', hour=18, minute=00)

agenda.add_job(MonitoraCompraCartao, 'cron', hour=9, minute=20)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=10, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=10, minute=30)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=11, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=11, minute=30)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=12, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=12, minute=30)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=13, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=14, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=15, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=16, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=17, minute=00)
agenda.add_job(MonitoraCompraCartao, 'cron', hour=18, minute=00)

# Iniciar o agendador
agenda.start()

"""
MonitoraAtivaCartao()
MonitoraCompraCartao()
MonitoraOnboarding()
MonitoraPagamentoBoleto()
"""