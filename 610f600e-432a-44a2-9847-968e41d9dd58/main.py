from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Targeted asset for day trading
        self.ticker = "SPY"

    @property
    def assets(self):
        # Specify the asset(s) this strategy will trade
        return [self.ticker]

    @property
    def interval(self):
        # Utilizing a 15-minute interval for day trading
        return "15min"

    def run(self, data):
        # Initialize allocation to be neutral at the start
        allocation = {self.ticker: 0}
        # Check if we have enough data points
        if len(data["ohlcv"]) < 21: # Need at least 21 data points for BB and RSI
            return TargetAllocation(allocation)
        
        # Fetch the latest Bollinger Bands and RSI values
        bbands = BB(self.ticker, data["ohlcv"], length=20)
        rsi = RSI(self.ticker, data["ohlcv"], length=14)
        
        # Get the closing price of the latest interval
        current_price = data["ohlcv"][-1][self.ticker]['close']
        
        if bbands and rsi:
            upper_band = bbands['upper'][-1]
            lower_band = bbands['lower'][-1]
            current_rsi = rsi[-1]
            
            # Conditions for entering a long position
            if current_price < lower_band and current_rsi < 30:
                # When the price is below the lower BB and RSI is below 30, it's considered oversold
                log(f"Buying signal at {current_price} with RSI {current_rsi}")
                allocation[self.ticker] = 1.0 # Full allocation to this asset
                
            # Conditions for taking profits or cutting losses
            elif current_price > upper_band or current_rsi > 70:
                # When the price is above the upper BB or RSI is above 70, it's either time to take profits or cut losses
                log(f"Selling signal at {current_price} with RSI {current_rsi}")
                allocation[self.ticker] = 0 # No allocation, i.e., sell

        return TargetAllocation(allocation)