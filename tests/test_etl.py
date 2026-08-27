from src.etl import build_sales_data, run_etl


def test_run_etl_calculates_revenue(tmp_path):
    output_file = tmp_path / "sales.csv"

    processed_sales = run_etl(output_file)

    assert processed_sales["revenue"].tolist() == [9.0, 6.25, 4.5]
    assert output_file.exists()
    assert len(build_sales_data()) == 3