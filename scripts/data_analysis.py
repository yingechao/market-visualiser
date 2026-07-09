# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# load / read in csv and save into dataframe 
df = pd.read_csv("../data/AAPL.csv", parse_dates=["date"])

print(df.head())

df = df.sort_values("date")
df = df.set_index("date")

# calculate daily returns 
df["daily_return"] = df["close"].pct_change()

# create a cumulative return column #?
df["cumulative_return"] = (1 + df["daily_return"]).cumprod() - 1

# calculate a 20-day moving average column
df["ma_20"] = df["close"].rolling(window = 20).mean()
df["ma_50"] = df["close"].rolling(window = 50).mean()

# create a running maximum column
df["running_max"] = df["close"].cummax()

# create a drawdown column
df["drawdown"] = df["close"] / df["running_max"] -1

# print total return, volatility, and max drawdown
start_price = df["close"].iloc[0]
end_price = df["close"].iloc[-1]

total_return = end_price / start_price - 1
daily_volatility = df["daily_return"].std()
annualised_volatility = daily_volatility * np.sqrt(252)
max_drawdown = df["drawdown"].min()

best_day = df["daily_return"].max()
worst_day = df["daily_return"].min()

print("AAPL basic metrics")
print("------------------")
print(f"Rows: {len(df)}")
print(f"Start date: {df.index.min().date()}")
print(f"End date: {df.index.max().date()}")
print(f"Start close: ${start_price:.2f}")
print(f"End close: ${end_price:.2f}")
print(f"Total return: {total_return:.2%}")
print(f"Daily volatility: {daily_volatility:.2%}")
print(f"Annualised volatility: {annualised_volatility:.2%}")
print(f"Max drawdown: {max_drawdown:.2%}")
print(f"Best day: {best_day:.2%}")
print(f"Worst day: {worst_day:.2%}")

# plot close price and moving averages
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["close"], label="Close")
plt.plot(df.index, df["ma_20"], label="20-day MA")
plt.plot(df.index, df["ma_50"], label="50-day MA")

plt.title("AAPL close price")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)

plt.savefig("outputs/aapl_price.png")

# 10. Plot drawdown
plt.figure(figsize=(12, 4))
plt.plot(df.index, df["drawdown"])

plt.title("AAPL drawdown")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.grid(True)

plt.savefig("outputs/aapl_drawdown.png")