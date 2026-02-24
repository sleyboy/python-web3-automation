import os
import requests
import time
from groq import Groq

# --- CONFIGURAÇÕES SEGURAS (Lidas do Servidor Render) ---
# O GitHub não vai bloquear este código porque as chaves não estão visíveis aqui
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MY_WALLET = "0x67A77D70d45bb43C94a35172d87290a402b8f43a"

# Inicializa o Cérebro IA (Groq)
client = Groq(api_key=GROQ_KEY)

def send_tg(msg):
    """Envia alertas em tempo real para o teu Telegram"""
    url = f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try:
        requests.get(url)
    except:
        pass

def search_and_conquer():
    """Vaqueiro Digital: Varre o GitHub e Algora por Bounties de Python/Go/Security"""
    # Procura por termos técnicos que pagam bem (mesmo sem a palavra Python)
    queries = ["label:bounty automation", "label:bounty scraper", "label:bounty api", "XSS bounty", "RAG pipeline"]
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    for q in queries:
        url = f"https://api.github.com{q}+is:open&sort=created&order=desc"
        
        try:
            resp = requests.get(url, headers=headers).json()
            items = resp.get('items', [])
            
            for issue in items:
                # Se houver pouca concorrência (< 5 comentários), nós atacamos!
                if issue.get('comments', 0) < 5:
                    title = issue['title']
                    link = issue['html_url']
                    body = issue.get('body', '')

                    # 1. BRAIN: Groq analisa o problema e cria a solução técnica
                    prompt = f"Solve this tech issue professionally: {title}\nDescription: {body}\nOutput ONLY the code solution. Mention payment in USDC Polygon to {MY_WALLET}."
                    completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama3-70b-8192"
                    )
                    solution = completion.choices.message.content

                    # 2. ACTION: O Bot comenta no GitHub para garantir o teu lugar na fila
                    comment_url = issue['comments_url']
                    comment_body = f"Hi! I can solve this. I've already drafted a high-performance solution. I accept payment in USDC (Polygon) at {MY_WALLET}. Ready to submit PR! /attempt #{issue['number']}"
                    requests.post(comment_url, headers=headers, json={"body": comment_body})

                    # 3. NOTIFY: Alerta imediato no teu Telegram com o link e a solução
                    send_tg(f"💰 TRABALHO ENCONTRADO: {title}\n\nLink: {link}\n\nSolução da Groq gerada! Abre o GitHub e finaliza os dólares.")
                    time.sleep(60) # Evita ser banido por spam
        except Exception as e:
            print(f"Erro no loop: {e}")
            continue

if __name__ == "__main__":
    # Mensagem de ativação
    send_tg("🚀 Sleyboy Hunter 2.0 Ativo! O teu exército digital está a minerar agora.")
    while True:
        search_and_conquer()
        # Descansa 10 minutos entre varreduras para não ser bloqueado
        time.sleep(600) 
