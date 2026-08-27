# Retail Mini ETL

A beginner-friendly example that creates a tiny retail orders dataset, cleans it
with pandas, writes `data/processed/orders_clean.csv`, and loads SQLite at
`db/orders.db`.

## Run the project

From the repository root, run these commands in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.etl
pytest
```

The ETL script prints three KPIs and creates the processed CSV and SQLite table.
