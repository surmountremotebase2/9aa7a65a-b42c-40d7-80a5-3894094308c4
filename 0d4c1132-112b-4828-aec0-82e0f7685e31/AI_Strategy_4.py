from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA", "AAPL", "AMZN"]
        self.lookback_days = 20  # Lookback period for the high price to check the breakout
        self.exit_lookback_days = 10  # Lookback period for the low price to exit the trade

    @property
    def interval(self):
        # We're using daily data for our analysis
        return "1day"

    @property
    def assets(self):
        # The assets we're trading
        return self.tickers

    @property
    def data(self):
        # No additional data needed beyond the default OHLCV
        return []

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            ohlcv = data["ohlcv"]
            
            if len(ohlcv) < self.lookback_days:
                log(f"Not enough data for {ticker}")
                allocation_dict[ticker] = 0  # Not trading if we don't have enough lookback data
                continue
            
            # Calculate the 20-day high and 10-day low
            high_20_day = max(ohlcv[i][ticker]["high"] for i in range(-self.lookback_days, 0))
            low_10_day = min(ohlcv[i][ticker]["low"] for i in range(-self.exit_lookback_days, 0))

            # Current price to decide the action
            current_close = ohlcv[-1][ticker]["close"]
            
            # Strategy logic for breakout entry and exit
            if current_close > high_20_day:
                log(f"Breakout detected in {ticker}, going long.")
                allocation_dict[ticker] = 1.0 / len(self.tickers)  # Allocate equally among the tickers
            elif current_close < low_10_day:
                log(f"Exiting position for {ticker} due to break below 10-day low.")
                allocation_dict[ticker] = 0  # Exit position
            else:
                allocation_dict[ticker] = 0  # Default allocation if no condition met
            
        return TargetAllocation(allocation_dict)