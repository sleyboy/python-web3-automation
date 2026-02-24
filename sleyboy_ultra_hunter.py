import os
import requests
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from groq import Groq

# --- CONFIGURAÇÕES SEGURAS ---
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MY_WALLET = "0x67A77D70d45bb43C94a35172d87290a402b8f43a"

client = Groq(api_key=GROQ_KEY)

# --- TRUQUE PARA O RENDER NÃO DESLIGAR (SERVIDOR FANTASMA) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Sleyboy Bot is Alive")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"[*] Health check server on port {port}")
    server.serve_forever()

# --- LÓGICA DO ROBÔ CAÇADOR ---
def send_tg(msg):
    url = f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try: requests.get(url)
    except: pass

def hunt():
    queries = ["label:bounty automation", "label:bounty scraper", "XSS bounty", "RAG pipeline"]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    for q in queries:
        url = f"https://api.github.com{q}+is:open&sort=created&order=desc"
        try:
            items = requests.get(url, headers=headers).json().get('items', [])
            for issue in items:
                if issue.get('comments', 0) < 5:
                    # Envia para o Telegram apenas o que interessa
                    msg = f"💰 BOUNTY: {issue['title']}\nLink: {issue['html_url']}"
                    send_tg(msg)
                    time.sleep(30)
        except: continue

if __name__ == "__main__":
    # 1. Inicia o servidor fantasma numa linha separada (Thread)
    threading.Thread(target=run_health_check_server, daemon=True).start()
    
    # 2. Inicia o Bot
    send_tg("🚀 Sleyboy Hunter 3.0 ONLINE! A caça começou.")
    while True:
        hunt()
        time.sleep(600) # Procura a cada 10 minutos
