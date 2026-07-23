# generate buy/sell/hold signals 
import pandas as pd
from data_cleaner import clean_price_data

data = clean_price_data("../data/AAPL.csv")
print(data.head())
print()
print(data.dtypes)
print()
print(data.index)
# data checking
assert not data.empty
assert data.index.is_monotonic_increasing
assert not data.isna().any().any()
assert not data.index.duplicated().any()

print("Data cleaning passed.")

def strategy(data: pd.DataFrame) -> pd.Series:
    # this is a moving average strategy 
    # signal 1 means to buy or hold a long position. signal 0 means to hold no position.
    # 1 = own the stock
    # 0 = do not own the stock 

    ma_20 = data["close"].rolling(20).mean()
    ma_50 = data["close"].rolling(50).mean()

    # create signal series to return at the end 

    signal = pd.Series(data = 0, index = data.index, dtype= int, name="signal")
    signal.loc[ma_20 > ma_50] = 1

    return signal

