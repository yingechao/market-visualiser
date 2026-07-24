# run everything and write JSON for React
# use signal series, available cash, execution price, and current number of shares to simulate trades

from data_cleaner import clean_price_data
from strategy import strategy
from backtester import create_sim

# 1. read and clean the raw market data
data = clean_price_data("../data/AAPL.csv")

# 2. pass the cleaned dataframe into the strategy
signals = strategy(data)

# 3. pass both the prices and signals into the backtester 
results, trades = create_sim(data = data, signals = signals, init_cash=10000,)

print("Trades: ")
print(trades)
print("\nFinal portfolio state: ")
print(results.tail())