# calculate performance (starting cash, final value, total return, max drawdown)
import pandas as pd

def add_metrics_col(results: pd.DataFrame,) -> pd.DataFrame:

    # add times series performance metrics to the daily results

    # do not change the og dataframe
    results = results.copy()

    # return from one row to the next
    results["daily_return"] = (results["portfolio_value"].pct_change())

    # total return since the start of the backtest
    results["cumulative_return"] = (results["portfolio_value"] / results["portfolio_value"].iloc[0]) - 1

    # highest portfolio value reached up to each row 
    results["running_max"] = (results["portfolio_value"].cummax())

    # current decline from the previous portfolio peak
    results["drawdown"] = (results["portfolio_value"] / results["running_max"] - 1)

    return results

def results_summary(results: pd.DataFrame, trades: pd.DataFrame,) -> dict:
    # return one overall summary of the backtest

    start_val = results["portfolio_value"].iloc[0]
    end_val = results["portfolio_value"].iloc[-1]

    total_return = end_val / start_val - 1
    maximum_drawdown = results["drawdown"].min()

    return {
        "starting_value": float(start_val),
        "ending_value": float(end_val),
        "total_return": float(total_return),
        "maximum_drawdown": float(maximum_drawdown),
        "number_of_trades": int(len(trades)),
    }
