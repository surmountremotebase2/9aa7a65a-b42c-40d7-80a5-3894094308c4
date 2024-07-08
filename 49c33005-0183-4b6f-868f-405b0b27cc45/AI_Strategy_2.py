from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["NVDA"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Access historical OHLCV data for NVDA
        nvda_data = data["ohlcv"]["NVDA"]
        # Calculating Bollinger Bands for NVDA
        nvda_bbands = BB("NVDA", nvda_data, 20, 2)  # Using 20 periods and 2 std deviations
        
        if not nvda_bbands:
            # If for some reason Bollinger Bands calculation fails, do nothing.
            return TargetAllocation({"NVDA": 0})

        # Fetch the last close price
        last_close_price = nvda_data[-1]['close']
        lower_band = nvda_bbands['lower'][-1]
        upper_band = nvda_bbands['upper'][-1]

        # Calculate the acceptable buy and sell thresholds
        buy_threshold = lower_band * 1.20  # Within 20% of the support level
        sell_threshold = upper_band * 0.92  # Within 8% of the resistance level

        # Default action is to hold the current position
        nvda_stake = data["holdings"].get("NVDA", 0)

        # Determine if we should buy
        if last_close_price <= buy_threshold:
            log("Buying NVDA - price within 20% of support level.")
            nvda_stake = 1  # Assuming full allocation for simplicity
            
        # Determine if we should sell
        elif last_close_price >= sell_threshold:
            log("Selling NVDA - price within 8% of resistance level.")
            nvda_stake = 0  # Sell all holdings
        
        # Return the target allocation
        return TargetAllocation({"NVDA": nvda_stake})