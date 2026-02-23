import requests
import time

# Professional Crypto Price Alert Bot
# Built for LaborX / Gitcoin Portfolios
# Developer: sleyboy (GitHub)

class PriceAlertBot:
    def __init__(self, coin="bitcoin", currency="usd"):
        self.coin = coin
        self.currency = currency
        self.api_url = f"https://api.coingecko.com{coin}&vs_currencies={currency}"

    def get_market_price(self):
        """Fetches real-time price from CoinGecko API"""
        try:
            response = requests.get(self.api_url).json()
            price = response[self.coin][self.currency]
            return price
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None

    def start_monitoring(self, target_price, interval=60):
        """Monitors the price every X seconds and alerts if target is hit"""
        print(f"[*] Starting monitor for {self.coin.upper()} at target ${target_price}...")
        
        while True:
            current_price = self.get_market_price()
            if current_price:
                print(f"[LOG] Current {self.coin.upper()} Price: ${current_price}")
                
                if current_price >= target_price:
                    print(f"🚀 [ALERT] {self.coin.upper()} HIT TARGET: ${current_price}!")
                    # Here we would trigger the Telegram/Discord webhook
                    break
            
            time.sleep(interval)

if __name__ == "__main__":
    # Proof of Concept: Monitoring Bitcoin to hit $100k
    bot = PriceAlertBot(coin="bitcoin")
    bot.start_monitoring(target_price=100000)
