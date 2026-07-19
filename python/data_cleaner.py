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

    # check high and low boundaries and ensure that low is never greater than high
    df["high"] = df[["open", "high", "close"]].max(axis=1)
    # Low must be <= open and close
    df["low"] = df[["open", "low", "close"]].min(axis=1)
    
    # Drop rows with impossible negative prices or volumes
    df = df[(df[numeric_columns] >= 0).all(axis=1)]

    # set date as the index
    df = df.set_index("date")

    return df