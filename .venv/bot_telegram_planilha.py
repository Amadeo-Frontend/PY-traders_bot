import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient, events
import pandas as pd

# Carrega variáveis de ambiente
load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

# Configuração do cliente do Telegram
client = TelegramClient('session_name', API_ID, API_HASH)

# Caminho da planilha (ajuste o nome do arquivo)
PLANILHA_PATH = 'dados_traders.xlsx'

# Função para processar mensagens
def parse_mensagem(texto):
    padrao = r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|'
    matches = re.findall(padrao, texto, re.DOTALL)
    if not matches:
        return None
    dados = [item.strip() for item in matches[0]]
    return {
        'Name': dados[0],
        'Plataforma': dados[1],
        'OP': dados[2],
        'Horários': dados[3],
        'Exp': dados[4],
        'Gales': dados[5],
        'Loss': dados[6]
    }

# Evento: quando uma nova mensagem é recebida
@client.on(events.NewMessage)
async def handler(event):
    texto = event.message.text
    if '|' in texto and 'Plataforma' in texto:  # Verifica se é uma tabela
        dados = parse_mensagem(texto)
        if dados:
            df = pd.DataFrame([dados])
            
            # Salva na planilha
            if not os.path.exists(PLANILHA_PATH):
                df.to_excel(PLANILHA_PATH, index=False)
            else:
                df_existente = pd.read_excel(PLANILHA_PATH)
                df_final = pd.concat([df_existente, df], ignore_index=True)
                df_final.to_excel(PLANILHA_PATH, index=False)
            print('Dados atualizados na planilha!')

# Inicia o cliente
async def main():
    await client.start(PHONE)
    print("Bot iniciado. Monitorando mensagens...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())