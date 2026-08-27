# Retail Mini ETL

A beginner-friendly example that creates a tiny retail dataset, transforms it
with pandas, and writes the processed data to `data/processed/sales.csv`.

## Run the project

From the repository root, run these commands in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.etl
pytest
```

The ETL script prints the total revenue and creates the processed CSV file.
