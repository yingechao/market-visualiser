# simulate cash, position, trades, and portfolio value
# turn signals into positions/returns/equity

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

print("pandas:", pd.__version__)
print("numpy:", np.__version__)
print("Install works!")

def create_sim(
    data: pd.DataFrame, 
    signals: pd.Series,
    init_cash: float = 10000.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    # ensure that every signal lines up with the same dates as the price data
    if not data.index.equals(signals.index):
        raise ValueError(
            "The price data and signals must have matching indexes."
        )

    cash = init_cash
    shares = 0

    daily_records =[] 
    trade_records = []

    # process the market data one row at a time.
    for i in range(len(data)):
        # get date
        date = data.index[i]
        # get current row 
        current_row = data.iloc[i]

        # get open and close prices
        open_price = current_row["open"]
        close_price = current_row["close"]

        # initialise action, trade qty, and trade price
        action = "hold"
        trade_quantity = 0
        trade_price = None

        # use the signal produced from yesterday's close price and today's opening price to simulate the trade
        if i > 0:
            desired_pos_signal = signals.iloc[i-1]

            # if the signal says to own the stock but we dont own any now, buy
            if (desired_pos_signal == 1 and shares == 0):

                # calculate the number of shares to buy
                shares_to_buy = int(cash // open_price)

                if shares_to_buy > 0:
                    cost = shares_to_buy * open_price
                    cash -= cost
                    shares += shares_to_buy

                    action = "buy"
                    trade_quantity = shares_to_buy
                    trade_price = open_price
            # if the signal says hold cash, but we already own shares
            elif (desired_pos_signal == 0 and shares > 0):

                # calculate the number of shares to sell
                shares_to_sell = shares
                proceeds = shares_to_sell * open_price

                cash += proceeds
                shares = 0

                action = "sell"
                trade_quantity = shares_to_sell
                trade_price = open_price

        # value the shares (stock value and portfolio value) using today's closing price
        stock_value = shares * close_price
        portfolio_value = cash + stock_value

        # save one record for every market data row 
        daily_records.append({
            "date": date,
            "open" : open_price,
            "close": close_price,
            "signal": signals.iloc[i],
            "action": action,
            "trade_quality": trade_quantity,
            "shares": shares,
            "cash":cash,
            "stock_value" : stock_value,
            "portfolio_value" : portfolio_value,
        })

        # save a separate record only for when a trade occurred 
        if action != "hold":
            trade_records.append({
                "date": date,
                "action": action, 
                "quantity": trade_quantity,
                "price": trade_price, 
                "cash_after_trade": cash,
                "shares_after_trade": shares,
            })

        results = pd.DataFrame(daily_records).set_index("date")
        trades = pd.DataFrame(trade_records)

    return results, trades