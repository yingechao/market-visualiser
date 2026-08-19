// define shape of data that is expected by React

export type BacktestSummary = {
  starting_value: number;
  ending_value: number;
  total_return: number;
  maximum_drawdown: number;
  number_of_trades: number;
};

export interface BacktestResult {
  date: string;
  open: number;
  close: number;

  signal: number;
  action: string;

  cash: number;
  shares: number;
  stock_value: number;
  portfolio_value: number;

  daily_return: number;
  cumulative_return: number;
  running_max: number;
  drawdown: number;

  trade_quality: number;
}

export interface Trade {
  date: string;
  action: string;
  quantity: number;
  price: number;
  cash_after_trade: number;
  shares_after_trade: number;
};

export type BacktestResponse = {
  summary: BacktestSummary;
  results: BacktestResult[];
  trades: Trade[];
};