import os
import time
import psycopg2
import locale
import shutil
import tkinter as tk
from tkinter import scrolledtext
from datetime import date, timedelta, datetime

#Define valores datetime
data_atual_postgres = date.today()
data_atual = date.today()
data_Pasta_Arquivo = data_atual.strftime('%d-%m-%Y')
Data_e_HoraLOG = datetime.now()

def Corrige_espacamento(texto):
    texto = texto.replace("'), " , """

""")
    return texto

# Função para salvar os resultados de erro em um arquivo .txt
def salvar_arquivo_Log_Erro(conteudo, nome_arquivo=f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de erro
        diretorio_formatacao = r"C:\Automatização_Script\Script-MCC\Scripts\Scripts_Postgres\LogsRetorno"
        diretorio_erro = r"C:\LogsAutomatizacao\LogsErro"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_erro, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_formatacao, nome_arquivo)

        # Abre o arquivo para escrita (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "w", encoding="utf-8") as file:
            #Data e hora da execução
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
def salvar_arquivo_Log_Sucesso(conteudo, nome_arquivo=f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}.txt"):
    try:
        # Define o caminho do diretório de sucesso
        diretorio_formatacao = r"C:\Automatização_Script\Script-MCC\Scripts\Scripts_Postgres\LogsRetorno"
        diretorio_sucesso = r"C:\LogsAutomatizacao\LogsSucesso"
        
        # Garante que o diretório exista
        os.makedirs(diretorio_sucesso, exist_ok=True)

        # Define o caminho completo do arquivo
        caminho_arquivo = os.path.join(diretorio_formatacao, nome_arquivo)

        # Abre o arquivo para escrita (irá criar o arquivo se não existir)
        with open(caminho_arquivo, "w", encoding="utf-8") as file:
            # Escreve o conteúdo no arquivo
             #Data e hora da execução
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



pasta_vscode = r"C:\Automatização_Script\Script-MCC\Scripts\Scripts_Postgres\LogsRetorno"
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

#Define Locale
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

# Pega as variaveis no ambiente de sistema e tenta conexão com a database e criar conexão
try:
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("User_Postgres")
    db_password = os.getenv("Senha_Postgres")

    # Make sure all variables are defined.
    if not all([db_host, db_name, db_user, db_password]):
        raise ValueError("Insira valores do banco de dados nas variaveis de ambiente")
    
    # Connect into Database set
    conexao = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        options="-c client_encoding=UTF8"
    )
    # CREATE A CURSOR
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

#Monitoramento Banco de dados
def MonitoraPostgres():
    
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
    
    for row in leituraPagBoleto:

        if row[5] in leituraPagBoleto != data_atual_postgres or str == "":
                print("Pagamento de boleto possivelmente com erro")
                # Verifica e salva no arquivo, se necessário
                salvar_arquivo_Log_Erro(conteudo= f"{Data_e_HoraLOG}\n \n{leituraPagBoleto}\n", nome_arquivo=f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}.txt")
                
                #Renomeia e move arquivo das files vscode
                renomear_e_mover_arquivos(
                pasta_origem= pasta_vscode,
                pasta_destino= r"C:\LogsAutomatizacao\LogsErro",
                parametro_nome= "Log_Erro_Pagamento_boleto_",
                novo_nome_base= f"Log_Erro_Pagamento_boleto_{data_Pasta_Arquivo}"
                )

        else:
            print("Pagamento de boleto possivelmente funcional")
            salvar_arquivo_Log_Sucesso(conteudo= f"\n{leituraPagBoleto}\n", nome_arquivo=f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}.txt")
            #Renomeia e move arquivo das files vscode
            renomear_e_mover_arquivos(
                pasta_origem= pasta_vscode,
                pasta_destino= r"C:\LogsAutomatizacao\LogsSucesso",
                parametro_nome= "Log_Sucesso_Pagamento_boleto_",
                novo_nome_base= f"Log_Sucesso_Pagamento_boleto_{data_Pasta_Arquivo}"
                )

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
Order By etapaAtual.created_at desc
LIMIT 5;
""")
    
    leituraOnboarding = SQL.fetchall()
    for row in leituraOnboarding:
        if row[9] in leituraOnboarding != "":
            print("SQL")
        
    print(f"{row [0]} | {row [1]} | {row [2]} | {row [3]} | {row [4]} | {row [5]} | {row [6]} | {row [7]} | {row [8]} | {row [9]} | {row [10]} | {row [11]}")


# Chama a execução das funções -------------------------------------------------------------------------------------------

#Chamar função caso tenham erros recorrentes
#TesteVariaveis()

#Chama a função de monitoria do Postgres e suas Querys
MonitoraPostgres()

