import pandas as pd

from src.etl import run_etl, transform_orders


def test_revenue_column_exists_and_non_negative(tmp_path):
    processed_orders = run_etl(
        raw_file=tmp_path / "raw" / "orders.csv",
        processed_file=tmp_path / "processed" / "orders_clean.csv",
        database_file=tmp_path / "db" / "orders.db",
    )

    assert "revenue" in processed_orders.columns
    assert (processed_orders["revenue"] >= 0).all()


def test_missing_quantity_filled_with_one():
    orders = pd.DataFrame(
        {
            "order_id": [1],
            "order_date": ["2026-01-01"],
            "product": ["Pen"],
            "quantity": [None],
            "unit_price": [1.25],
        }
    )

    cleaned_orders = transform_orders(orders)

    assert cleaned_orders.loc[0, "quantity"] == 1