// define shape of data that is expected by React

export type BacktestSummary = {
  starting_value: number;
  ending_value: number;
  total_return: number;
  maximum_drawdown: number;
  number_of_trades: number;
};

export type BacktestResult = {
  date: string;
  open: number;
  close: number;
  signal: number;
  action: string;
  shares: number;
  cash: number;
  portfolio_value: number;
  daily_return: number;
  cumulative_return: number;
  drawdown: number;
};

export type Trade = {
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