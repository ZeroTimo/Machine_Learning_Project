import sys
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Fehler: Kein Ticker angegeben. Beispielaufruf: python evaluate.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1]

    # Pfade anpassen
    model_file = f"models/{ticker}_best_xgboost_model.pkl"
    input_file = f"data/{ticker}_with_indicators.csv"

    try:
        # Modell laden
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"Kein gespeichertes Modell gefunden: {model_file}. Bitte trainiere das Modell zuerst mit train_model.py")

        best_model = joblib.load(model_file)
        print(f"✅ Modell geladen: {model_file}")

        # Daten laden
        data = pd.read_csv(input_file)
        X_test = data.drop(columns=["Target_Close_5d", "Date"], errors='ignore').iloc[int(len(data) * 0.8):]
        y_test = data["Target_Close_5d"].iloc[int(len(data) * 0.8):]

        # Vorhersagen treffen
        y_pred = best_model.predict(X_test)

        # Evaluierung des Modells
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        # Ergebnisse speichern
        os.makedirs("results", exist_ok=True)
        eval_results = pd.DataFrame({
            "MAE": [mae],
            "MSE": [mse],
            "RMSE": [rmse]
        })
        results_file = f"results/{ticker}_evaluation_metrics.csv"
        eval_results.to_csv(results_file, index=False)

        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}")
        print(f"✅ Ergebnisse gespeichert in {results_file}")

        # Visualisierung: Echte vs. vorhergesagte Preise
        plt.figure(figsize=(10, 6))
        plt.plot(y_test.values, label="Echter Preis", color="blue")
        plt.plot(y_pred, label="Vorhergesagter Preis", color="red")
        plt.xlabel("Zeit")
        plt.ylabel("Preis")
        plt.title("Echter vs. vorhergesagter Preis")
        plt.legend()
        plt.savefig(f"results/{ticker}_price_comparison.png")
        print(f"✅ Visualisierung 'Echter vs. vorhergesagter Preis' gespeichert in results/{ticker}_price_comparison.png")

    except FileNotFoundError as e:
        print(f"❌ Fehler: {str(e)}")

