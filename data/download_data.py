import yfinance as yf

ticker = "AAPL"

# download price data for Apple from 1 Jan 2020 to 1 Jan 2024
df = yf.download(
    ticker,
    start="2020-01-01",
    end="2024-01-01",
    auto_adjust=False # do not automatically adjust OHLC prices for dividends and stock splits
    # more to learn about adjusted prices for backtesting later
)
# download is stored in df, which stands for dataframe (like a table)

# check whether the download failed
if df.empty:
    raise ValueError(f"No data downloaded for selected ticker {ticker}")

# Reset date index into a normal column
df = df.reset_index()

print(df.columns)
# Keep only the columns we want
df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

# Rename columns to lowercase for easier use later
df.columns = ["date", "open", "high", "low", "close", "volume"]

# Save to CSV
df.to_csv("AAPL.csv", index=False)
# index = False ensures the index is not saved as an extra col
