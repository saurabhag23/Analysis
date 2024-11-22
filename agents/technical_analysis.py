import numpy as np
import pandas as pd

class TechnicalAnalysisAgent:
    def __init__(self):
        pass

    def calculate_sma(self, prices, window=20):
        """Calculates Simple Moving Average (SMA) and converts it to a list."""
        return prices['Close'].rolling(window=window).mean().dropna().tail(10).tolist()

    def calculate_ema(self, prices, window=20):
        """Calculates Exponential Moving Average (EMA) and converts it to a list."""
        return prices['Close'].ewm(span=window, adjust=False).mean().dropna().tail(10).tolist()

    def find_support_resistance(self, prices, window=20):
        """Identifies potential support and resistance levels and converts them to lists."""
        rolling_max = prices['High'].rolling(window=window, min_periods=1).max().dropna().tail(10).tolist()
        rolling_min = prices['Low'].rolling(window=window, min_periods=1).min().dropna().tail(10).tolist()
        return rolling_min, rolling_max

    def calculate_macd(self, prices, slow=26, fast=12):
        """Calculates the Moving Average Convergence Divergence (MACD) and its signal line and converts them to lists."""
        ema_fast = prices['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = prices['Close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd.dropna().tail(10).tolist(), signal.dropna().tail(10).tolist()

    def calculate_bollinger_bands(self, prices, window=20, num_std_dev=2):
        """Calculates Bollinger Bands and converts them to lists."""
        sma = prices['Close'].rolling(window=window).mean()
        rstd = prices['Close'].rolling(window=window).std()
        upper_band = (sma + rstd * num_std_dev).dropna().tail(10).tolist()
        lower_band = (sma - rstd * num_std_dev).dropna().tail(10).tolist()
        return upper_band, lower_band

    def analyze_technical(self, historical_prices):
        """Perform technical analysis with historical price data and prepare for JSON serialization."""
        sma = self.calculate_sma(historical_prices)
        ema = self.calculate_ema(historical_prices)
        support, resistance = self.find_support_resistance(historical_prices)
        macd, macd_signal = self.calculate_macd(historical_prices)
        upper_band, lower_band = self.calculate_bollinger_bands(historical_prices)

        return {
            "SMA": sma,
            "EMA": ema,
            "Support": support,
            "Resistance": resistance,
            "MACD": macd,
            "MACD Signal": macd_signal,
            "Bollinger Upper Band": upper_band,
            "Bollinger Lower Band": lower_band
        }