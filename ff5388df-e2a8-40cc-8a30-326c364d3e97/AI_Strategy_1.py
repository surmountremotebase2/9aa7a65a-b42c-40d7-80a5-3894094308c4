from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.ticker = "NVDA"
        self.support_distance = 0.20  # 20% from support
        self.resistance_distance = 0.20  # 20% from resistance

    @property
    def assets(self):
        return [self.t.getAbsolutePath()]

    @property
    def interval(self):
        return "1day"
    
    def run(self, data):
        # Calculate simple moving averages as proxy for support and resistance
        support_sma = SMA(self.ticker, data["ohlcv"], 50)  # Shorter SMA for support
        resistance_sma = SMA(self.ticker, data["ohlcv"], 200)  # Longer SMA for resistance

        if not support_sma or not resistance_sma:
            return TargetAllocation({})
        
        current_price = data["ohlcv"][-1][self.ticker]["close"]
        support_level = support_sma[-1]
        resistance_level = resistance_sma[-1]
        
        allocation = 0
        within_support = current_price <= (support_level * (1 + self.support_distance))
        within_resistance = current_price >= (resistance_level * (1 - self.resistance_distance))

        if within_support:
            # Buy strategy
            log("NVDA within 15% of support level, buying signal triggered.")
            allocation = 1  # Here, 1 represents a 100% allocation, adjust according to your strategy
        elif within_resistance:
            # Sell strategy
            log("NVDA within 18% of resistance level, selling signal triggered.")
            allocation = -1  # Symbolize selling, actual implementation depends on framework handling
        
        return TargetAllocation({self.ticker: allocation})