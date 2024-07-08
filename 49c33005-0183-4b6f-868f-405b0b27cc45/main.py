from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker we're interested in
        self.ticker = "NVDA"
        # Set buy and sell margins
        self.buy_margin = 0.15  # 15% within the support level
        self.sell_margin = 0.18  # 18% within the resistance level

    @property
    def assets(self):
        # Specify the asset(s) your strategy deals with
        return [self.ticker]

    @property
    def interval(self):
        # Frequency of data updates (this can be adjusted as needed)
        return "1day"
    
    def calculate_support(self, data):
        # Simple moving average for 50 days period could act as support
        return SMA(self.ticker, data, 50)[-1]

    def calculate_resistance(self, data):
        # Simple moving average for 200 days period could act as resistance
        return SMA(self.ticker, data, 200)[-1]

    def run(self, data):
        ohlcv = data["ohlcv"]
        current_price = ohlcv[-1][self.ticker]["close"]
        
        support_level = self.calculate_support(ohlcv)
        resistance_level = self.calculate_resistance(ohlcv)
        
        allocation = {}
        
        # Ensure we have the necessary data for our calculation
        if support_level and resistance_level and current_price:
            # Determine our buy/sell strategy
            if current_price <= support_level * (1 + self.buy_margin):
                # Within 15% of the support level, consider buying
                allocation[self.ticker] = 1.0
            elif current_price >= resistance_level * (1 - self.sell_margin):
                # Within 18% of the resistance level, consider selling
                allocation[self.ticker] = 0  # Sell signal represented by 0 allocation
            else:
                # No action, hold the stock if already owned
                log(f"Holding {self.ticker}. No action.")
        else:
            log("Insufficient data for decision.")

        return TargetAllocation(allocation)

# Note: This strategy assumes you have the capability to go long (buy) and exit (sell) positions.
# It does not directly execute sell orders but suggests when to sell by setting the allocation to 0.