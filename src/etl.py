"""Create and transform a tiny retail dataset."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "sales.csv"


def build_sales_data() -> pd.DataFrame:
    """Return a small sales dataset for the example pipeline."""
    return pd.DataFrame(
        {
            "product": ["Notebook", "Pen", "Notebook"],
            "quantity": [2, 5, 1],
            "unit_price": [4.50, 1.25, 4.50],
        }
    )


def run_etl(output_file: Path = PROCESSED_FILE) -> pd.DataFrame:
    """Calculate revenue per sale and save the processed data as CSV."""
    sales = build_sales_data()
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    sales.to_csv(output_file, index=False)
    return sales


if __name__ == "__main__":
    processed_sales = run_etl()
    print(f"Total revenue: ${processed_sales['revenue'].sum():.2f}")