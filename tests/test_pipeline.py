import pandas as pd
import pytest

from backtester import create_sim
from metrics import add_metrics_col, results_summary
from run_backtest import run_pipeline


def test_pipeline_uses_custom_file_cash_and_benchmark(tmp_path):
    path = tmp_path / "custom.csv"
    path.write_text("date,open,high,low,close,volume\n"
                    "2026-01-01,10,11,9,10,100\n"
                    "2026-01-02,10,13,9,12,100\n"
                    "2026-01-03,12,15,11,14,100\n")
    data, _, results, _, summary = run_pipeline(path, initial_cash=25, transaction_cost_rate=0.1)
    assert len(data) == 3
    assert summary["starting_value"] == 25
    # Benchmark buys two shares for $22 including fees, leaving $3 cash.
    assert results["benchmark_value"].tolist() == pytest.approx([25, 27, 31])
    assert summary["benchmark_ending_value"] == pytest.approx(31)
    assert summary["benchmark_total_return"] == pytest.approx(0.24)


def test_transaction_costs_apply_to_both_sides_and_reduce_affordability():
    data = pd.DataFrame({"open": [10, 10, 20], "close": [10, 10, 20]})
    results, trades = create_sim(data, pd.Series([1, 0, 0]), init_cash=100, transaction_cost_rate=0.1)
    assert trades["quantity"].tolist() == [9, 9]
    assert trades["transaction_cost"].tolist() == pytest.approx([9, 18])
    assert results["cash"].tolist() == pytest.approx([100, 1, 163])
    assert results["portfolio_value"].tolist() == pytest.approx([100, 91, 163])


@pytest.mark.parametrize("cash", [0, -1, float('nan'), float('inf')])
def test_invalid_cash_is_rejected(cash):
    with pytest.raises(ValueError, match="Initial cash"):
        create_sim(pd.DataFrame({"open": [10], "close": [10]}), pd.Series([0]), init_cash=cash)


@pytest.mark.parametrize("rate", [-0.1, 1, float('nan')])
def test_invalid_cost_rate_is_rejected(rate):
    with pytest.raises(ValueError, match="Transaction cost"):
        create_sim(pd.DataFrame({"open": [10], "close": [10]}), pd.Series([0]), transaction_cost_rate=rate)


def test_empty_data_and_invalid_signals_are_rejected():
    with pytest.raises(ValueError, match="must not be empty"):
        create_sim(pd.DataFrame(), pd.Series(dtype=int))
    data = pd.DataFrame({"open": [10], "close": [10]})
    with pytest.raises(ValueError, match="Signals"):
        create_sim(data, pd.Series([2]))
    with pytest.raises(ValueError, match="must not be empty"):
        add_metrics_col(pd.DataFrame())
    with pytest.raises(ValueError, match="must not be empty"):
        results_summary(pd.DataFrame(), pd.DataFrame())
