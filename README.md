# Aktienkurs-Prognose-Projekt

Dieses Repository enthält ein Machine-Learning-Projekt, das historische Aktienkurse verwendet, um zukünftige Preise vorherzusagen. Der Workflow umfasst Datenabruf, Feature-Engineering, Modelltraining und Evaluierung. Die Ergebnisse werden visuell aufbereitet, um die Modellleistung verständlich darzustellen.

## Projektübersicht

### Datenabruf:
- Historische Aktienkurse werden über die Yahoo Finance API abgerufen.
- Der Zeitraum und der Ticker können flexibel gewählt werden.

### Feature-Engineering:
- Technische Indikatoren (z. B. gleitende Durchschnitte, RSI, Bollinger-Bänder) werden berechnet.
- Die Zielvariable ist der Schlusskurs des nächsten Handelstags.

### Modelltraining:
- Ein XGBoost-Modell wird verwendet, um zukünftige Preise vorherzusagen.
- Das Modell wird mit verschiedenen Hyperparametern optimiert (Grid Search).

### Evaluierung:
- Das Modell wird mit MAE, MSE und RMSE bewertet.
- Ergebnisse und Visualisierungen (echte vs. vorhergesagte Preise, Fehlermetriken) werden gespeichert.

## Installation

### Repository klonen:
git clone https://github.com/ZeroTimo/Machine_Learning_Project.git

### Abhängigkeiten installieren:
pip install -r requirements.txt

## Projektstruktur:

Machine_Learning_Project/
├── data/                # Enthält historische Daten und verarbeitete Daten mit Indikatoren
├── models/              # Gespeicherte Modelle
├── results/             # Evaluierungsergebnisse und Visualisierungen
├── src/                 # Enthält die Hauptskripte
│   ├── data_collection.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   └── evaluate.py
└── main.py              # Führt den gesamten Workflow aus

## Nutzung

### Workflow ausführen:
python main.py
Folge den Eingabeaufforderungen, um einen Ticker sowie einen Zeitraum anzugeben.

### Ergebnisse ansehen:
- Evaluierungsmesswerte: results/{TICKER}_evaluation_metrics.csv
- Visualisierungen: results/{TICKER}_price_comparison.png, results/{TICKER}_metrics.png
Hinweise

- Das Projekt ist flexibel für verschiedene Ticker und Zeiträume einsetzbar.
- Die Visualisierungen und Fehlermetriken helfen, die Modellleistung besser zu verstehen.
