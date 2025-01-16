import os
import time
import psycopg2
import locale
import shutil
import tkinter as tk
from tkinter import scrolledtext
from datetime import date, timedelta, datetime

#Define Locale
locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

#Define valores datetime
data_atual_postgres = date.today()

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
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        options="-c client_encoding=UTF8"
    )
    # CREATE A CURSOR
    cursor = conn.cursor()
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
    
    #Lança a Query para o Psycopg puxar do postgre
    cursor.execute("""
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
    
    leituraPagBoleto = cursor.fetchall()

    JanelaResultados = tk.Tk()
    JanelaResultados.title("Resultado da Query")
    
    # Criando a área de texto para exibir os resultados
    text_area = scrolledtext.ScrolledText(JanelaResultados, width=180, height=30, wrap=tk.WORD)
    
    # Usando pack para expandir o widget tanto vertical quanto horizontalmente
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Adicionando os resultados da consulta SQL na área de texto
    for row in leituraPagBoleto:
        text_area.insert(tk.END, "Id | Nome | Cpf | Descrição | Valor | Data & hora | Valor da fatura \n")
        text_area.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} \n")

        if row[5] != data_atual_postgres or len == 0:
            print("Pagamento de boleto possivelmente com erro")
        else:
            print("Teste concluído com sucesso")

    
    cursor.execute("""
                   

    """)
    UltimosPagBoletos = cursor.fetchall()

    # Tornar a janela interativa
    # text_area.config(state=tk.DISABLED)  # Desabilita a edição do texto
    JanelaResultados.mainloop()

# Chama a execução das funções -------------------------------------------------------------------------------------------

#Chamar função caso tenham erros recorrentes
#TesteVariaveis()

#Chama a função de monitoria do Postgres e suas Querys
MonitoraPostgres()

