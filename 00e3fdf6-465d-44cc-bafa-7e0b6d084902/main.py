from surmount.base_class import Strategy, TargetAllocation
from surmount.data import FinancialStatement, SocialSentiment
from surmount.technical_indicators import EMA, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Tracking only AAPL for this strategy
        self.tickers = ["AAPL"]
        
        # Adding SocialSentiment and FinancialStatement to data_list for AAPL
        self.data_list = [SocialSentiment("AAPL"), FinancialStatement("AAPL")]

    @property
    def interval(self):
        # Using daily data for the analysis
        return "1day"

    @property
    def assets(self):
        # Operates on AAPL
        return self.tickers

    @property
    def data(self):
        # Data required for the run method
        return self.data_list

    def run(self, data):
        # Default allocation to AAPL is 0, meaning not holding any position initially
        aapl_stake = 0

        ema_short = EMA("AAPL", data["ohlcv"], length=12)  # Short-term EMA
        ema_long = EMA("AAPL", data["ohlcv"], length=26)  # Long-term EMA
        rsi = RSI("AAPL", data["ohlcv"], length=14)  # Relative Strength Index
        social_sentiment = data[("social_sentiment", "AAPL")][-1]["twitterSentiment"] if ("social_sentiment", "AAPL") in data else None

        # Trading logic
        if social_sentiment and social_sentiment > 0.5:
            # Positive sentiment on Twitter: consider buying
            if ema_short[-1] > ema_long[-1] and rsi[-1] < 70:
                # If short-term EMA is above long-term EMA and RSI is below 70 (not overbought), allocate 100% to AAPL
                aapl_stake = 1.0
            elif ema_short[-1] < ema_long[-1] or rsi[-1] > 70:
                # If short-term EMA is below long-term EMA or RSI is above 70 (overbought), do not hold AAPL
                aapl_stake = 0
        else:
            # Neutral or negative sentiment: stay cautious
            if ema_short[-1] > ema_long[-1] and rsi[-1] < 30:
                # Consider buying only if strongly indicated by EMA and RSI (oversold condition)
                aapl_stake = 0.5
            else:
                # Otherwise, do not hold AAPL
                aapl_stake = 0

        # Logging the decision
        log(f"Allocating {aapl_stake * 100}% to AAPL based on EMA crossover, RSI, and social sentiment.")

        # Return the target allocation
        return TargetAllocation({"AAPL": aapl_stake})