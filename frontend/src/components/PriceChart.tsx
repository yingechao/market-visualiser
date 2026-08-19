import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

import type { BacktestResult, Trade } from "../types";
import { treemapPayloadSearcher } from "recharts/types/chart/Treemap";

interface PriceChartProps {
  results: BacktestResult[];
  trades: Trade[];
}

function TradeMarker(props: any) {
  const { cx, cy, payload } = props;

  if (payload.tradeAction === "buy") {
    return (
      <circle
        cx={cx}
        cy={cy}
        r={6}
        fill="green"
      />
    );
  }

  if (payload.tradeAction === "sell") {
    return (
      <circle
        cx={cx}
        cy={cy}
        r={6}
        fill="red"
      />
    );
  }

  return <></>;
}

function PriceChart({ results, trades }: PriceChartProps) {

    const tradeMap = new Map(
    trades.map((trade) => [trade.date, trade])
  );

  const chartData = results.map((result) => {
    const trade = tradeMap.get(result.date);
    return{
      ...result, 
      tradeAction: trade?.action ?? null,
    };
  });

  return (
    <div style={{ width: "100%", height: 400 }}>

      <h2>Price Value</h2>

      <ResponsiveContainer>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="date"
            minTickGap={50}
          />

          <YAxis
            tickFormatter={(value) => `$${value.toLocaleString()}`}
          />

          <Tooltip
            formatter={(value) => [
              `$${Number(value).toLocaleString()}`,
              "Asset Value"
            ]}
          />

          <Line
            type="monotone"
            dataKey="close"
            dot={<TradeMarker/>}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PriceChart;