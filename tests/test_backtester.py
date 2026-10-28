"""Small price paths with manually calculated executions and balances."""

import pandas as pd
import pytest

from backtester import create_sim


def prices(opens, closes):
    return pd.DataFrame(
        {"open": opens, "close": closes},
        index=pd.date_range("2026-01-01", periods=len(opens), name="date"),
    )


def test_round_trip_executes_previous_signal_at_open_and_values_at_close():
    data = prices([10, 12, 15, 14], [11, 13, 16, 100])
    signals = pd.Series([1, 1, 0, 1], index=data.index)

    results, trades = create_sim(data, signals, init_cash=100)

    # Buy eight shares for 96 on day two; sell for 112 on day four.
    assert results["action"].tolist() == ["hold", "buy", "hold", "sell"]
    assert results["cash"].tolist() == pytest.approx([100, 4, 4, 116])
    assert results["shares"].tolist() == [0, 8, 8, 0]
    assert results["stock_value"].tolist() == pytest.approx([0, 104, 128, 0])
    assert results["portfolio_value"].tolist() == pytest.approx([100, 108, 132, 116])
    assert trades["date"].tolist() == [data.index[1], data.index[3]]
    assert trades["action"].tolist() == ["buy", "sell"]
    assert trades["quantity"].tolist() == [8, 8]
    assert trades["price"].tolist() == pytest.approx([12, 14])
    assert trades["cash_after_trade"].tolist() == pytest.approx([4, 116])
    assert trades["shares_after_trade"].tolist() == [8, 0]


@pytest.mark.parametrize("signals", [[0, 0, 0], [0, 0, 1]])
def test_no_trade_without_an_executable_buy_signal(signals):
    data = prices([10, 20, 30], [15, 25, 35])
    results, trades = create_sim(data, pd.Series(signals, index=data.index), init_cash=73)

    # A buy signal on the final close has no next session in which to execute.
    assert trades.empty
    assert results["shares"].tolist() == [0, 0, 0]
    assert results["portfolio_value"].tolist() == pytest.approx([73, 73, 73])


@pytest.mark.parametrize("cash, expected_shares, expected_cash", [(9, 0, 9), (10, 1, 0), (25, 2, 5)])
def test_buys_only_affordable_whole_shares(cash, expected_shares, expected_cash):
    data = prices([10, 10], [10, 12])
    results, trades = create_sim(data, pd.Series([1, 1], index=data.index), init_cash=cash)

    assert results.iloc[-1]["shares"] == expected_shares
    assert results.iloc[-1]["cash"] == pytest.approx(expected_cash)
    assert results.iloc[-1]["portfolio_value"] == pytest.approx(expected_cash + expected_shares * 12)
    assert len(trades) == (1 if expected_shares else 0)


def test_rejects_misaligned_signal_dates():
    data = prices([10, 12], [11, 13])
    signals = pd.Series([1, 0], index=data.index + pd.Timedelta(days=1))

    with pytest.raises(ValueError, match="matching indexes"):
        create_sim(data, signals)
