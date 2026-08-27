"""Create, transform, and load a tiny retail orders dataset."""

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "orders.csv"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "orders_clean.csv"
DATABASE_FILE = PROJECT_ROOT / "db" / "orders.db"
ORDER_COLUMNS = ["order_id", "order_date", "product", "quantity", "unit_price"]


def create_raw_orders(raw_file: Path = RAW_FILE) -> None:
    """Create deterministic synthetic orders when the raw file is missing."""
    if raw_file.exists():
        return

    raw_file.parent.mkdir(parents=True, exist_ok=True)
    products = ["Notebook", "Pen", "Backpack", "Desk Lamp", "Mug"]
    orders = []
    for order_number in range(1, 31):
        orders.append(
            {
                "order_id": order_number,
                "order_date": f"2026-01-{(order_number % 28) + 1:02d}",
                "product": products[(order_number - 1) % len(products)],
                "quantity": "" if order_number in {7, 18, 26} else (order_number % 4) + 1,
                "unit_price": [4.50, 1.25, 24.99, 18.75, 8.00][(order_number - 1) % 5],
            }
        )
    pd.DataFrame(orders, columns=ORDER_COLUMNS).to_csv(raw_file, index=False)


def transform_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Clean order values and calculate revenue for each order."""
    cleaned = orders.copy()
    cleaned["quantity"] = cleaned["quantity"].fillna(1).astype(int)
    cleaned["unit_price"] = cleaned["unit_price"].astype(float)
    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]
    return cleaned


def run_etl(
    raw_file: Path = RAW_FILE,
    processed_file: Path = PROCESSED_FILE,
    database_file: Path = DATABASE_FILE,
) -> pd.DataFrame:
    """Run the orders ETL and return the cleaned data."""
    create_raw_orders(raw_file)
    cleaned_orders = transform_orders(pd.read_csv(raw_file))

    processed_file.parent.mkdir(parents=True, exist_ok=True)
    cleaned_orders.to_csv(processed_file, index=False)

    database_file.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_file) as connection:
        cleaned_orders.to_sql("orders_clean", connection, if_exists="replace", index=False)

    revenue_by_product = cleaned_orders.groupby("product")["revenue"].sum()
    top_product = revenue_by_product.idxmax()
    print(f"total_orders: {len(cleaned_orders)}")
    print(f"total_revenue: {cleaned_orders['revenue'].sum():.2f}")
    print(f"top_product_by_revenue: {top_product}")
    return cleaned_orders


if __name__ == "__main__":
    run_etl()