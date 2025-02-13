import sys
import pandas as pd
import os

def calculate_indicators(df):
    """Berechnet technische Indikatoren für die Aktienkursdaten."""
    df = df.copy()
    
    # Gleitende Durchschnitte
    df['SMA_10'] = df['Close'].rolling(window=10, min_periods=1).mean()
    df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
    
    # Relative Strength Index (RSI)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # MACD
    short_ema = df['Close'].ewm(span=12, adjust=False).mean()
    long_ema = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20, min_periods=1).mean()
    df['BB_Upper'] = df['BB_Middle'] + 2 * df['Close'].rolling(window=20, min_periods=1).std()
    df['BB_Lower'] = df['BB_Middle'] - 2 * df['Close'].rolling(window=20, min_periods=1).std()
    
    # Zielvariable für Regression: Preis in einem Tag
    df['Target_Close_5d'] = df['Close'].shift(-1)
    
    # Entferne verbleibende NaN-Werte
    df.dropna(inplace=True)
    
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Fehler: Kein Ticker angegeben. Beispielaufruf: python feature_engineering.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1]

    os.makedirs("data", exist_ok=True)
    input_file = f"data/{ticker}_historical_data.csv"
    output_file = f"data/{ticker}_with_indicators.csv"

    try:
        data = pd.read_csv(input_file)
        data = calculate_indicators(data)
        data.to_csv(output_file, index=False)
        print(f"✅ Feature Engineering abgeschlossen. Daten gespeichert in {output_file}")
    except FileNotFoundError:
        print(f"❌ Fehler: Datei {input_file} nicht gefunden. Bitte stelle sicher, dass die Daten vorhanden sind.")