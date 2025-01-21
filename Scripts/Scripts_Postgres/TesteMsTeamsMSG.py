import pymsteams
MensagemTeams = pymsteams("https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZGYxNjZmNGEtODEzOS00NjA4LThjZTAtOWVjODEzYjdlYzBj%40thread.v2/0?context=%7b%22Tid%22%3a%22db7cfec1-5723-4416-aeb0-614aad2cd4b4%22%2c%22Oid%22%3a%222532f655-dade-4d67-b0b0-f11ebc064389%22%7d")
MensagemTeams.text("this is my text")
MensagemTeams.send()


import requests
import json
from msal import ConfidentialClientApplication

# Configurações do aplicativo
CLIENT_ID = 'seu-client-id'
CLIENT_SECRET = 'seu-client-secret'
TENANT_ID = 'seu-tenant-id'
TEAM_ID = 'seu-team-id'
CHANNEL_ID = 'seu-channel-id'

# Endpoint para obter o token de acesso
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPES = ['https://graph.microsoft.com/.default']

# Função para obter token de acesso
def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPES)
    
    if "access_token" in result:
        return result['access_token']
    else:
        raise Exception("Não foi possível obter o token de acesso.")

# Função para enviar uma mensagem para o canal do Teams
def send_message_to_teams_channel(message):
    access_token = get_access_token()
    
    url = f'https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "body": {
            "content": message
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")
        print(response.text)

# Exemplo de uso
if __name__ == "__main__":
    message = "Esta é uma mensagem automática enviada pelo script!"
    send_message_to_teams_channel(message)
