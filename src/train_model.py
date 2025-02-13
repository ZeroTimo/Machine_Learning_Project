import sys
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import joblib
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Fehler: Kein Ticker angegeben. Beispielaufruf: python train_model.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1]

    # Pfade anpassen
    input_file = f"data/{ticker}_with_indicators.csv"
    model_file = f"models/{ticker}_best_xgboost_model.pkl"

    # Ordner für das Modell erstellen
    os.makedirs("models", exist_ok=True)

    try:
        # Daten laden
        data = pd.read_csv(input_file)
        X = data.drop(columns=["Target_Close_5d", "Date"], errors='ignore')
        y = data["Target_Close_5d"]

        # Zeitbasiertes Train-Test-Split (erste 80% Training, letzte 20% Test)
        split_index = int(len(data) * 0.8)
        X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
        y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

        # TimeSeriesSplit statt K-Fold für Grid Search
        tscv = TimeSeriesSplit(n_splits=3)

        # XGBoost Modell mit Grid Search für Hyperparameter-Tuning
        param_grid = {
            'n_estimators': [100, 200, 500],
            'learning_rate': [0.01, 0.1, 0.3],
            'max_depth': [3, 5, 7]
        }

        gb_model = xgb.XGBRegressor(objective='reg:squarederror')
        grid_search = GridSearchCV(gb_model, param_grid, scoring='neg_mean_absolute_error', cv=tscv, verbose=1)
        grid_search.fit(X_train, y_train)

        # Bestes Modell auswählen
        best_model = grid_search.best_estimator_
        print(f"Beste Hyperparameter: {grid_search.best_params_}")

        # Modell speichern
        joblib.dump(best_model, model_file)
        print(f"✅ Modell gespeichert: {model_file}")

    except FileNotFoundError:
        print(f"❌ Fehler: Datei {input_file} nicht gefunden. Bitte führe feature_engineering.py zuerst aus.")