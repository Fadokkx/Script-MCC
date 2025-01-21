import os
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import psycopg2
import locale
import shutil
from datetime import date, timedelta, datetime

#Define valores datetime
data_atual = date.today()
data_atual_postgres = data_atual.strftime('%Y-%m-%d')
data_Pasta_Arquivo = data_atual.strftime('%d-%m-%Y')
Data_e_HoraLOG = datetime.now()

#Função para melhor formatação do TXT LOG de saida
def Corrige_espacamento(texto):
    texto = texto.replace("'), " , """

""")
    return texto

def salvar_arquivo_Log_Erro_Boleto(conteudo, nome_arquivo=f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de erro
        diretorio_erro = r"C:\Automatização_Script\Script-MCC\Logs\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_erro, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:  # Alterado para "a" (append)
            # Data e hora da execução
            file.write(f"{Data_e_HoraLOG}\n\n")
            # Cabeçalho
            file.write("\nId | Nome | Cpf | Descrição | Valor | Data & hora | Valor da fatura\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"\n{conteudo}\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Aplica a função de correção
            conteudo_corrigido = Corrige_espacamento(conteudo_arquivo)
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_corrigido)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

# Função para salvar os resultados de sucesso em um arquivo .txt
def salvar_arquivo_Log_Sucesso_Boleto(conteudo, nome_arquivo=f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_sucesso = r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_sucesso, nome_arquivo)

        # Abre o arquivo para adicionar conteúdo (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:  # Alterado para "a" (append)
            # Data e hora da execução
            file.write(f"{Data_e_HoraLOG}\n")
            # Cabeçalho
            file.write("Id | Nome | Cpf | Descrição | Valor | Data & hora | Valor da fatura\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n\n"))
        
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Aplica a função de correção
            conteudo_corrigido = Corrige_espacamento(conteudo_arquivo)
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_corrigido)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def salvar_arquivo_Log_Sucesso_Onboarding(conteudo, nome_arquivo=f"Log_Sucesso_Onboarding_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_sucesso = r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_sucesso, nome_arquivo)

        # Abre o arquivo para escrita (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Escreve o conteúdo no arquivo
            #Data e hora da execução
            file.write(f"{Data_e_HoraLOG}\n")
            # Cabeçalho
            file.write("Tipo | Convênio | CPF | Nome | Valor_margem | Iniciado em | Etapa atual | Telefone | Erro | ID Onboarding | ID Etapa atual|\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n"))
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Aplica a função de correção
            conteudo_corrigido = Corrige_espacamento(conteudo_arquivo)
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_corrigido)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

def salvar_arquivo_Log_Erro_Onboarding(conteudo, nome_arquivo=f"Log_Erro_Onboarding_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_erro = r"C:\Automatização_Script\Script-MCC\Logs\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_erro, nome_arquivo)

        # Abre o arquivo para escrita (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "a", encoding="utf-8") as file:
            # Escreve o conteúdo no arquivo
             #Data e hora da execução
            file.write(f"{Data_e_HoraLOG}\n")
            # Cabeçalho
            file.write("Tipo | Convênio | CPF | Nome | Valor_margem | Iniciado em | Etapa atual | Telefone | Erro | ID Onboarding | ID Etapa atual|\n")
            # Escreve o conteúdo no arquivo
            file.write(str(f"{conteudo}\n"))
        with open(caminho_arquivo, "r+", encoding="utf-8") as file:
            # Lê todo o conteúdo do arquivo
            conteudo_arquivo = file.read()
            # Aplica a função de correção
            conteudo_corrigido = Corrige_espacamento(conteudo_arquivo)
            # Volta para o início do arquivo para sobrescrever o conteúdo
            file.seek(0)
            file.write(conteudo_corrigido)
            file.truncate()  #
        print(f"Conteúdo salvo com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar o conteúdo no arquivo: {e}")

#Função para mover os arquivos editados
def renomear_e_mover_arquivos(pasta_origem, pasta_destino, parametro_nome, novo_nome_base):
    """
    Renomeia e move arquivos que contenham um parâmetro no nome para uma pasta de destino.
    Sempre adiciona um sufixo _1, _2, ... ao novo nome, independentemente de duplicação.

    :param pasta_origem: Caminho da pasta onde os arquivos estão localizados.
    :param pasta_destino: Caminho da pasta para onde os arquivos serão movidos.
    :param parametro_nome: Texto que deve estar no nome dos arquivos.
    :param novo_nome_base: Base do novo nome para os arquivos renomeados.
    """
    try:
        # Criar a pasta de destino, se não existir
        os.makedirs(pasta_destino, exist_ok=True)

        # Listar arquivos na pasta de origem
        arquivos = os.listdir(pasta_origem)
        contador = 1

        for arquivo in arquivos:
            caminho_origem = os.path.join(pasta_origem, arquivo)

            # Ignorar pastas
            if os.path.isdir(caminho_origem):
                continue

            # Verificar se o parâmetro está no nome do arquivo
            if parametro_nome in arquivo:
                # Criar o novo nome do arquivo
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

#Define Locale
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# Pega as variaveis no ambiente de sistema e tenta conexão com a database e criar conexão
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

#Cria função Para verificação de dados no ambiente do sistema
def TesteVariaveis():
    print(db_host)
    print(db_name)
    print(db_user)
    print(db_password)
    print(data_atual_postgres)

# Monitoramento das saidas do Banco de dados
def MonitoraPostgres():
    # Variáveis para armazenar o conteúdo acumulado de sucesso e erro
    conteudo_sucesso = ""
    conteudo_erro = ""

     #Lança a Query para o Psycopg puxar do postgre os pagamentos de boletos (10:00; 12:00; 14;00; 16;00)
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
    # Verificar o valor de row[5] (Data de Transação)
        if str(row[5]) != str(data_atual_postgres):
        # Se for um erro, acumula no conteúdo de erro
            conteudo_erro += f"\n{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]}\n\n"
        else:
        # Se for sucesso, acumula no conteúdo de sucesso
            conteudo_sucesso += f"\n{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]}\n\n"

    # Depois que o loop terminou, você salva os arquivos com todos os dados
    if conteudo_erro:
        salvar_arquivo_Log_Erro_Boleto(conteudo=conteudo_erro)
    if conteudo_sucesso:
        salvar_arquivo_Log_Sucesso_Boleto(conteudo=conteudo_sucesso)
    
    # Renomeia e move os arquivos gerados (se necessário)
    if conteudo_erro:
        renomear_e_mover_arquivos(
            pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsErro",
            pasta_destino= rf"C:\LogsAutomatizacao\LogsErro\{data_Pasta_Arquivo}",
            parametro_nome= "Log_Erro_Pagamento_boleto_",
            novo_nome_base= f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}"
        )
    if conteudo_sucesso:
        renomear_e_mover_arquivos(
            pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso",
            pasta_destino= rf"C:\LogsAutomatizacao\LogsSucesso\{data_Pasta_Arquivo}",
            parametro_nome= "Log_Sucesso_Pagamento_boleto_",
            novo_nome_base= f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}"
        )

    print("Log da leitura do Pagamento de Boleto foi enviado para a pasta de Logs")
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
            print("Sem erros encontrados")
            salvar_arquivo_Log_Sucesso_Onboarding(conteudo= f"\n{leituraOnboarding}\n", nome_arquivo=f"Log_Sucesso_onboarding_{data_Pasta_Arquivo}.txt")
            
            time.sleep(2)
            
            #Renomeia e move arquivo da pasta vscode para a pasta de logs
            renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsSucesso" ,
                pasta_destino= rf"C:\LogsAutomatizacao\LogsSucesso\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Sucesso_Onboarding_",
                novo_nome_base= f"Log_Sucesso_Onboarding_{data_Pasta_Arquivo}"
                )
   
        else:
            print("Onboarding com erros")
            salvar_arquivo_Log_Erro_Onboarding(conteudo= f"\n{leituraOnboarding}\n", nome_arquivo=f"Log_Erro_onboarding_{data_Pasta_Arquivo}.txt")
            
            #Renomeia e move arquivo da pasta vscode para a pasta de logs
            time.sleep(2)
            renomear_e_mover_arquivos(
                pasta_origem= r"C:\Automatização_Script\Script-MCC\Logs\LogsErro",
                pasta_destino= rf"C:\LogsAutomatizacao\LogsErro\{data_Pasta_Arquivo}",
                parametro_nome= "Log_Erro_onboarding_",
                novo_nome_base= f"Log_Erro_Onboarding_{data_Pasta_Arquivo}"
                )
        
    print("Log da leitura do Onboarding foi enviado para a pasta de Logs")
"""
#Agenda o run da função de monitoria do postgres
agenda = BlockingScheduler()

agenda.add_job(MonitoraPostgres, 'cron', hour=11, minute=00)   
agenda.add_job(MonitoraPostgres, 'cron', hour=13, minute=15)  
agenda.add_job(MonitoraPostgres, 'cron', hour=15, minute=00)
agenda.add_job(MonitoraPostgres, 'cron', hour=17, minute=00)

# Iniciar o agendador
agenda.start()
"""
MonitoraPostgres()

#Chamar função caso tenham erros recorrentes
#TesteVariaveis()