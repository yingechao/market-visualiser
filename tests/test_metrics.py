import pandas as pd
import pytest

from metrics import add_metrics_col, results_summary


def test_returns_and_drawdown_follow_peaks_and_recovery_without_mutating_input():
    original = pd.DataFrame({"portfolio_value": [100, 120, 90, 108, 150]})
    before = original.copy(deep=True)

    results = add_metrics_col(original)

    assert results["daily_return"].tolist() == pytest.approx([0, 0.2, -0.25, 0.2, 150 / 108 - 1])
    assert results["cumulative_return"].tolist() == pytest.approx([0, 0.2, -0.1, 0.08, 0.5])
    assert results["running_max"].tolist() == pytest.approx([100, 120, 120, 120, 150])
    assert results["drawdown"].tolist() == pytest.approx([0, 0, -0.25, -0.1, 0])
    pd.testing.assert_frame_equal(original, before)


def test_summary_uses_worst_drawdown_even_after_recovery():
    results = add_metrics_col(pd.DataFrame({"portfolio_value": [100, 120, 90, 150]}))
    trades = pd.DataFrame({"action": ["buy", "sell"]})

    assert results_summary(results, trades) == pytest.approx({
        "starting_value": 100,
        "ending_value": 150,
        "total_return": 0.5,
        "maximum_drawdown": -0.25,
        "number_of_trades": 2,
    })


def test_single_day_without_trades_has_zero_return_and_drawdown():
    results = add_metrics_col(pd.DataFrame({"portfolio_value": [73]}))

    assert results.iloc[0]["daily_return"] == 0
    assert results_summary(results, pd.DataFrame()) == {
        "starting_value": 73,
        "ending_value": 73,
        "total_return": 0,
        "maximum_drawdown": 0,
        "number_of_trades": 0,
    }
