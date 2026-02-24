import os
import requests
import time
from groq import Groq
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- CONFIGURAÇÕES ---
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
MY_WALLET = "0x67A77D70d45bb43C94a35172d87290a402b8f43a"

client = Groq(api_key=GROQ_KEY)

# --- TRUQUE PARA O RENDER NÃO DESLIGAR ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Alive")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# --- LÓGICA DO ROBÔ ---
def send_tg(msg):
    url = f"https://api.telegram.org{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    requests.get(url)

def search_and_conquer():
    queries = ["label:bounty automation", "label:bounty scraper", "XSS bounty"]
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    for q in queries:
        url = f"https://api.github.com{q}+is:open&sort=created&order=desc"
        try:
            items = requests.get(url, headers=headers).json().get('items', [])
            for issue in items:
                if issue.get('comments', 0) < 5:
                    send_tg(f"💰 ACHADO: {issue['title']}\nLink: {issue['html_url']}")
                    time.sleep(60)
        except: continue

if __name__ == "__main__":
    # Inicia o servidor falso em segundo plano
    threading.Thread(target=run_health_check, daemon=True).start()
    
    send_tg("🚀 Sleyboy Hunter 3.0 ONLINE! A caça começou.")
    while True:
        search_and_conquer()
        time.sleep(600)
