from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, VWAP
from surmount.data import ohlcv
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA"]
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        # We use '5min' intervals for more granularity in day trading
        return "5min"
    
    def run(self, data):
        tsla_data = data["ohlcv"]
        
        # Ensure we have enough data points to calculate our indicators
        if len(tsla_data) < 20:  # Arbitrarily chosen 20 periods
            return TargetAllocation({})
        
        sma_short = SMA("TSLA", tsla_data, length=5)  # Short-term SMA
        sma_long = SMA("TSLA", tsla_data, length=20)  # Long-term SMA
        vwap = VWAP("TSLA", tsla_data, length=20)  # VWAP for the day
        
        # The current and previous price data
        current_price = tsla_data[-1]["TSLA"]['close']
        previous_price = tsla_data[-2]["TSLA"]['close']
        
        # The latest values for our indicators
        latest_sma_short = sma_short[-1]
        latest_sma_long = sma_long[-1]
        latest_vwap = vwap[-1]
        
        # Determine buy signals based on SMA crossover and VWAP confirmation
        if latest_sma_short > latest_sma_long and current_price > latest_vwap and previous_price <= latest_vwap:
            log("Buy signal based on SMA crossover and VWAP confirmation")
            tsla_stake = 1  # Max out position in TSLA based on strategy
        else:
            # No clear signal, avoid taking a new position
            tsla_stake = 0
            
        return TargetAllocation({"TSLA": tsla_stake})