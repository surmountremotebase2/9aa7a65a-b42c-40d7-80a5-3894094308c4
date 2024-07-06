from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    """
    This strategy trades SPY based on the MACD crossover signal.
    It buys SPY when the MACD line crosses above the signal line,
    and sells (or stays out) when the MACD line crosses below the signal line.
    """

    @property
    def assets(self):
        """
        Define the asset(s) that this strategy will trade.
        """
        return ["SPY"]

    @property
    def interval(self):
        """
        Set the data interval for the strategy. 
        This strategy uses daily data points.
        """
        return "1day"

    def run(self, data):
        """
        The core logic of the strategy, deciding when to buy or sell based on MACD signal.
        """
        spy_macd = MACD("SPY", data["ohlcv"], fast=12, slow=26)
        macd_line = spy_macd["MACD"]
        signal_line = spy_macd["signal"]
        
        spy_stake = 0  # Default to no position
        
        if len(macd_line) > 0 and len(signal_line) > 0:
            # Check for a bullish crossover (MACD crosses above signal)
            if macd_line[-1] > signal_domain[-1] and macd_line[-2] < signal_line[-2]:
                log("Bullish MACD crossover detected. Buying SPY.")
                spy_stake = 1  # Take a full position in SPY
            # Check for a bearish crossover (MACD crosses below signal)
            elif macd_line[-1] < signal_domain[-1] and macd_line[-2] > signal_line[-2]:
                log("Bearish MACD crossover detected. Exiting SPY.")
                spy_stake = 0  # Exit any position in SPY
        
        return TargetAllocation({"SPY": spy_stake})