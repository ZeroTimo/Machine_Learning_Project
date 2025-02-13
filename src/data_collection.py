import sys
import yfinance as yf
import pandas as pd
import os

def fetch_stock_data(ticker, start_date, end_date):
    """Lädt historische Aktienkurse von Yahoo Finance."""
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)

    if data.empty:
        print(f"⚠️ Warnung: Keine Daten für {ticker} im angegebenen Zeitraum gefunden!")
        sys.exit(1)

    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # Relevante Spalten behalten

    return data

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("❌ Fehler: Nicht genug Argumente angegeben. Beispielaufruf: python data_collection.py AAPL 2023-01-01 2023-12-31")
        sys.exit(1)

    ticker = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    os.makedirs("data", exist_ok=True)
    data = fetch_stock_data(ticker, start_date, end_date)
    file_path = f"data/{ticker}_historical_data.csv"
    data.to_csv(file_path)

    print(f"✅ Daten für {ticker} erfolgreich gespeichert: {file_path}")

