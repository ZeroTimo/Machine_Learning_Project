import subprocess

def run_script(script_name, args):
    print(f"Starte {script_name} mit Argumenten {args}...")
    result = subprocess.run(["python", script_name] + args, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    print(f"{script_name} abgeschlossen!\n")

if __name__ == "__main__":
    ticker = input("Bitte den Ticker eingeben (z.B. AAPL, TSLA, GOOG): ")
    start_date = input("Bitte das Startdatum eingeben (z.B. 2023-01-01): ")
    end_date = input("Bitte das Enddatum eingeben (z.B. 2023-12-31): ")

    scripts = [
        "src/data_collection.py",
        "src/feature_engineering.py",
        "src/train_model.py",
        "src/evaluate.py"
    ]
    
    for script in scripts:
        run_script(script, [ticker, start_date, end_date])
    
    print(f"✅ Kompletter Workflow für {ticker} abgeschlossen!")
