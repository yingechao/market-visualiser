import streamlit as st

from run_backtest import run_pipeline


st.set_page_config(
    page_title="Market Backtester",
    layout="wide",
)

st.title("Market Strategy Backtester")

data, signals, results, trades, summary = run_pipeline(
    filepath="../data/AAPL.csv",
    initial_cash=10_000,
)


st.subheader("Performance summary")

column_1, column_2, column_3, column_4 = st.columns(4)

column_1.metric(
    "Starting value",
    f"${summary['starting_value']:,.2f}",
)

column_2.metric(
    "Ending value",
    f"${summary['ending_value']:,.2f}",
)

column_3.metric(
    "Total return",
    f"{summary['total_return']:.2%}",
)

column_4.metric(
    "Maximum drawdown",
    f"{summary['maximum_drawdown']:.2%}",
)

st.metric(
    "Number of trades",
    summary["number_of_trades"],
)


st.subheader("Market price")

st.line_chart(
    results["close"]
)


st.subheader("Portfolio value")

st.line_chart(
    results["portfolio_value"]
)


st.subheader("Drawdown")

st.line_chart(
    results["drawdown"]
)


st.subheader("Trades")

if trades.empty:
    st.info("The strategy did not generate any trades.")
else:
    st.dataframe(
        trades,
        use_container_width=True,
    )


with st.expander("Daily backtest results"):
    st.dataframe(
        results,
        use_container_width=True,
    )