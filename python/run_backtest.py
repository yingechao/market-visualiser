# run everything and write JSON for React
# use signal series, available cash, execution price, and current number of shares to simulate trades

from data_cleaner import clean_price_data
from strategy import strategy
from backtester import create_sim
from metrics import add_metrics_col, results_summary
from pathlib import Path
import pandas as pd

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "AAPL.csv"

def run_pipeline(
        filepath: str | Path = DEFAULT_DATA_PATH,
        initial_cash: float = 10000, 
        transaction_cost_rate: float = 0.0,

):
    # 1. read and clean the raw market data
    data = clean_price_data(filepath)

    # 2. pass the cleaned dataframe into the strategy
    signals = strategy(data)

    # 3. pass both the prices and signals into the backtester 
    results, trades = create_sim(data, signals, init_cash=initial_cash, transaction_cost_rate=transaction_cost_rate)

    # Buy at the second session's open, matching the strategy's earliest execution.
    benchmark_signals = pd.Series(1, index=data.index)
    benchmark, _ = create_sim(data, benchmark_signals, init_cash=initial_cash, transaction_cost_rate=transaction_cost_rate)
    results["benchmark_value"] = benchmark["portfolio_value"]

    results = add_metrics_col(results)

    summary = results_summary(
        results=results,
        trades=trades,
    )
    summary["benchmark_ending_value"] = float(benchmark["portfolio_value"].iloc[-1])
    summary["benchmark_total_return"] = summary["benchmark_ending_value"] / initial_cash - 1

    return data, signals, results, trades, summary 



if __name__ == "__main__":
    data, signals, results, trades, summary = run_pipeline(
        filepath=DEFAULT_DATA_PATH,
        initial_cash=10_000,
    )

    print(results.tail())
    print(trades)
    print(summary)
