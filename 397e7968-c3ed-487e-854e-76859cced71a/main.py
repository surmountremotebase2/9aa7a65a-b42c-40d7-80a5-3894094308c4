from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbols for the strategy.
        self.tickers = ["NVDA", "SOUN", "AMD", "TSLA", "GOOG", "AAPLE"]
        # Set the initial trailing stop percentage (e.g., 5% trailing stop).
        self.trailing_stop_percentage = 5
        # Initialize a dictionary to keep track of entry prices for the trailing stop calculation.
        self.entry_prices = {ticker: None for ticker in self.tickers}
        # Define a short and long window for moving average to identify momentum
        self.short_window = 20
        self.long_window = 50
        
    @property
    def interval(self):
        # Define the time interval for the strategy.
        return "1day"
        
    @property
    def assets(self):
        # Return the assets that the strategy will involve.
        return self.tickers
        
    def run(self, data):
        allocation = {}
        for ticker in self.tickers:
            d = data["ohlcv"][ticker]
            if len(d) >= self.long_window:
                # Compute short and long-term moving averages
                short_ma = SMA(ticker, data, self.short_window)
                long_ma = SMA(ticker, data, self.long_window)
                
                # Entry condition: if short-term MA crosses above long-term MA, indicating momentum.
                if short_ma[-1] > long_ma[-1] and short_ma[-2] < long_ma[-2]:
                    allocation[ticker] = 1.0 / len(self.tickers)  # Evenly distribute allocation.
                    self.entry_prices[ticker] = d[-1]["close"]  # Update entry price for trailing stop calculation.
                # Check if the current price is lower than the trailing stop price (if entry price is set).
                elif self.entry_prices[ticker] and d[-1]["close"] < self.entry_prices[ticker] * (1 - self.trailing_stop_percentage / 100.0):
                    allocation[ticker] = 0  # Exit the position.
                    self.entry_prices[ticker] = None  # Reset entry price.
                else:
                    allocation[ticker] = 0  # No action taken.
            else:
                allocation[ticker] = 0  # No action due to insufficient data.
                
        return TargetAllocation(allocation)