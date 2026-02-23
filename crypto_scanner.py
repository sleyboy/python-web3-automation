import ccxt
import time

"""
Crypto Arbitrage Scanner
Author: Your Name
Description: A high-performance script to monitor price discrepancies 
between major exchanges using CCXT for fast API integration.
"""

def scan_markets():
    # Initialize exchanges (Binance and Kraken are used as examples)
    binance = ccxt.binance()
    kraken = ccxt.kraken()
    
    symbol = 'BTC/USDT'
    
    print(f"--- Monitoring {symbol} Market Inefficiency ---")
    
    try:
        # Fetch real-time market data
        ticker_binance = binance.fetch_ticker(symbol)
        ticker_kraken = kraken.fetch_ticker(symbol)
        
        # We buy where it is cheaper and sell where it is more expensive
        buy_price = ticker_binance['ask'] # Lowest price to buy on Binance
        sell_price = ticker_kraken['bid'] # Highest price to sell on Kraken
        
        spread = sell_price - buy_price
        profit_margin = (spread / buy_price) * 100
        
        print(f"Binance Ask: ${buy_price} | Kraken Bid: ${sell_price}")
        
        if spread > 0:
            print(f"[!] PROFIT OPPORTUNITY FOUND: +${spread:.2f} ({profit_margin:.2f}%)")
        else:
            print(f"[...] Spread is negative (${spread:.2f}). Looking for inefficiencies...")
            
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    # Simulate a monitoring loop
    for _ in range(5):
        scan_markets()
        time.sleep(3) # Wait 3 seconds between scans
