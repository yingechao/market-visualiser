import pandas as pd
import pytest

from data_cleaner import clean_price_data


def test_normalises_columns_sorts_dates_and_keeps_last_duplicate(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text(
        " Date , Open , High , Low , Close , Volume \n"
        "2026-01-05,20,23,19,22,100\n"
        "2026-01-02,10,13,9,11,100\n"
        "2026-01-02,11,14,10,12,200\n"
    )

    result = clean_price_data(str(path))

    assert result.index.tolist() == list(pd.to_datetime(["2026-01-02", "2026-01-05"]))
    assert result["close"].tolist() == [12, 22]
    assert result["volume"].tolist() == [200, 100]
    # No synthetic weekend rows should enter the backtest.
    assert len(result) == 2


@pytest.mark.parametrize("bad_row", [
    "invalid-date,10,12,9,11,100",
    "2026-01-03,not-a-price,12,9,11,100",
    "2026-01-03,10,10,9,11,100",  # High below close.
    "2026-01-03,10,12,11,11,100",  # Low above open.
    "2026-01-03,0,12,0,11,100",  # Zero price.
    "2026-01-03,10,12,9,11,-1",  # Negative volume.
])
def test_drops_invalid_rows_but_preserves_valid_zero_volume_row(tmp_path, bad_row):
    path = tmp_path / "prices.csv"
    path.write_text(
        "date,open,high,low,close,volume\n"
        "2026-01-02,10,12,9,11,0\n" + bad_row + "\n"
    )

    result = clean_price_data(str(path))

    assert result.index.tolist() == [pd.Timestamp("2026-01-02")]
    assert result.iloc[0]["volume"] == 0


def test_rejects_missing_required_columns(tmp_path):
    path = tmp_path / "prices.csv"
    path.write_text("date,close\n2026-01-02,10\n")

    with pytest.raises(ValueError, match="Missing required columns"):
        clean_price_data(str(path))
