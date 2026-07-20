# this is the data being cleaned for the backtester and NOT the visualiser
import pandas as pd

def clean_price_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    df.columns = df.columns.str.strip().str.lower()

    required_columns = {
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )
    
    # try to convert the value and turn it into a missing value if conversion is impossible  
    df["date"] = pd.to_datetime(df["date"], errors="coerce",)

    #convert numeric columns to numbers if not already 
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # if anything is missing, remove that row
    df = df.dropna(subset=["date", *numeric_columns])

    # sort values by date
    df = df.sort_values("date")

    # if there are duplicate dates, keep the latest version
    df = df.drop_duplicates(subset="date", keep="last",)

    valid_ohlc = (
        # High must be at least as large as open and close.
        (df["high"] >= df[["open", "close"]].max(axis=1))

        # Low must be at most as small as open and close.
        & (df["low"] <= df[["open", "close"]].min(axis=1))

        # High cannot be below low.
        & (df["high"] >= df["low"])
    )

    df = df[valid_ohlc]
    
    # Drop rows with impossible negative prices 
    price_columns = ["open", "high", "low", "close"]
    # ensure rows only have valid values 
    valid_prices = (df[price_columns] > 0).all(axis=1)
    valid_volume = df["volume"] >= 0
    df = df[valid_prices & valid_volume]

    # set date as the index
    df = df.set_index("date")

    return df