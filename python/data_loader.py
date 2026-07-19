# this is data being cleaned for the visualiser and NOT the backtester
# load CSVs into pandas

import pandas as pd

def load_price_data() -> pd.DataFrame:
    # load csv, standardise column names, check required columns exist, sort by date, remove duplicates, convert prices to numbers, drop broken rows, return clean df

    # read csv and convert date string to datetime object
    df = pd.read_csv("../data/AAPL.csv", parse_dates=["date"])
    df = df.sort_values("date")
    df = df.set_index("date")
    # reindex time gaps (weekends and holidays) to fill in missing days 
    # REMOVE this fill when cleaning data for a backtester
    full_idx = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(full_idx)
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low','close']].ffill()

    # if volume is missing on a specific day, set it to zero to prevent errors in indicators such as vol weighted avg price
    df['volume'] = df['volume'].fillna(0)

    # 5. Remove any remaining unexpected missing data
    df.dropna(inplace=True)
    return df