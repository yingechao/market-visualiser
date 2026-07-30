# run everything and write JSON for React
# use signal series, available cash, execution price, and current number of shares to simulate trades

from data_cleaner import clean_price_data
from strategy import strategy
from backtester import create_sim
from metrics import add_metrics_col, results_summary

def run_pipeline(
        filepath: str, 
        initial_cash: float = 10000, 

):
    # 1. read and clean the raw market data
    data = clean_price_data("../data/AAPL.csv")

    # 2. pass the cleaned dataframe into the strategy
    signals = strategy(data)

    # 3. pass both the prices and signals into the backtester 
    results, trades = create_sim(data = data, signals = signals, init_cash=10000,)

    results = add_metrics_col(results)

    summary = results_summary(
        results=results,
        trades=trades,
    )

    return data, signals, results, trades, summary 



if __name__ == "__main__":
    data, signals, results, trades, summary = run_pipeline(
        filepath="../data/AAPL.csv",
        initial_cash=10_000,
    )

    print(results.tail())
    print(trades)
    print(summary)