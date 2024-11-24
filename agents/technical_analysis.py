import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

class TechnicalAnalysisAgent:
    def __init__(self):
        pass

    def convert_to_dataframe(self, historical_prices):
        """Convert the historical prices data to a pandas DataFrame."""
        if isinstance(historical_prices, pd.DataFrame):
            return historical_prices
        
        if isinstance(historical_prices, dict):
            # Handle nested dictionary structure from DataConverter
            if 'data' in historical_prices:
                df = pd.DataFrame(historical_prices['data'])
                if 'index' in historical_prices:
                    df.index = historical_prices['index']
                return df
            
            # Handle flat dictionary structure
            return pd.DataFrame(historical_prices)
            
        return pd.DataFrame()

    def analyze_technical(self, financial_data):
    
        try:
            # Extract historical prices from the nested structure
            stock_price_data = financial_data.get('stock_price_data', {})
            historical_prices = stock_price_data.get('historical_prices')
            
            if historical_prices is None:
                raise ValueError("No historical prices data found")

            # Convert to DataFrame
            df = self.convert_to_dataframe(historical_prices)

            # Verify required columns exist
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Missing required columns. Required: {required_columns}. Found: {df.columns.tolist()}")

            # Calculate all technical indicators
            results = {
                "Moving Averages": self.calculate_moving_averages(df),
                "Oscillators": self.calculate_oscillators(df),
                "Trend Indicators": self.calculate_trend_indicators(df),
                "Volatility Indicators": self.calculate_volatility_indicators(df),
                "Volume Indicators": self.calculate_volume_indicators(df),
                "Support and Resistance": self.find_support_resistance(df)
            }

            # Convert numpy arrays and other non-serializable types to lists
            results = self.convert_to_serializable(results)
            return results
        except Exception as e:
            print(f"Error in technical analysis: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }
    def convert_to_serializable(self, data):
        """Convert all numpy arrays and other types to JSON-serializable format."""
        if isinstance(data, dict):
            return {k: self.convert_to_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_serializable(v) for v in data]
        elif isinstance(data, (np.ndarray, pd.Series)):
            return data.tolist()
        elif isinstance(data, (np.float32, np.float64)):
            return float(data)
        elif isinstance(data, (np.int32, np.int64)):
            return int(data)
        return data

    def calculate_moving_averages(self, prices):
        try:
            return {
                "SMA_50": self.calculate_sma(prices, 50),
                "SMA_200": self.calculate_sma(prices, 200),
                "EMA_12": self.calculate_ema(prices, 12),
                "EMA_26": self.calculate_ema(prices, 26)
            }
        except Exception as e:
            print(f"Error calculating moving averages: {str(e)}")
            return {}

    def calculate_oscillators(self, prices):
        try:
            return {
                "RSI": self.calculate_rsi(prices),
                "Stochastic": {
                    "K": self.calculate_stochastic_oscillator(prices)[0],
                    "D": self.calculate_stochastic_oscillator(prices)[1]
                },
                "MACD": {
                    "MACD_Line": self.calculate_macd(prices)[0],
                    "Signal_Line": self.calculate_macd(prices)[1]
                }
            }
        except Exception as e:
            print(f"Error calculating oscillators: {str(e)}")
            return {}

    def calculate_trend_indicators(self, prices):
        try:
            return {
                "ADX": self.calculate_adx(prices),
                "Parabolic_SAR": self.calculate_parabolic_sar(prices)
            }
        except Exception as e:
            print(f"Error calculating trend indicators: {str(e)}")
            return {}

    def calculate_volatility_indicators(self, prices):
        try:
            bb_upper, bb_lower = self.calculate_bollinger_bands(prices)
            return {
                "Bollinger_Bands": {
                    "Upper": bb_upper,
                    "Lower": bb_lower
                },
                "ATR": self.calculate_atr(prices)
            }
        except Exception as e:
            print(f"Error calculating volatility indicators: {str(e)}")
            return {}

    def calculate_volume_indicators(self, prices):
        try:
            return {
                "OBV": self.calculate_obv(prices),
                "CMF": self.calculate_cmf(prices)
            }
        except Exception as e:
            print(f"Error calculating volume indicators: {str(e)}")
            return {}

    # Rest of the calculation methods remain the same as in your original code
    # [Previous methods for calculate_sma, calculate_ema, calculate_rsi, etc.]
    
    def calculate_sma(self, prices, window):
        return prices['Close'].rolling(window=window).mean().dropna().tail(10).tolist()

    def calculate_ema(self, prices, window):
        return prices['Close'].ewm(span=window, adjust=False).mean().dropna().tail(10).tolist()

    def calculate_rsi(self, prices, window=14):
        delta = prices['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.dropna().tail(10).tolist()

    def calculate_stochastic_oscillator(self, prices, window=14):
        low_min = prices['Low'].rolling(window=window).min()
        high_max = prices['High'].rolling(window=window).max()
        k = 100 * (prices['Close'] - low_min) / (high_max - low_min)
        d = k.rolling(window=3).mean()
        return k.dropna().tail(10).tolist(), d.dropna().tail(10).tolist()

    def calculate_macd(self, prices, slow=26, fast=12, signal=9):
        ema_fast = prices['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = prices['Close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd.dropna().tail(10).tolist(), signal_line.dropna().tail(10).tolist()

    def calculate_adx(self, prices, window=14):
        tr1 = abs(prices['High'] - prices['Low'])
        tr2 = abs(prices['High'] - prices['Close'].shift(1))
        tr3 = abs(prices['Low'] - prices['Close'].shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=window).mean()
        
        up_move = prices['High'] - prices['High'].shift(1)
        down_move = prices['Low'].shift(1) - prices['Low']
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        plus_di = 100 * (pd.Series(plus_dm).rolling(window=window).mean() / atr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(window=window).mean() / atr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=window).mean()
        
        return adx.dropna().tail(10).tolist()

    def calculate_parabolic_sar(self, prices, step=0.02, max_step=0.2):
        high, low = prices['High'], prices['Low']
        sar = low.copy()
        af = pd.Series(step, index=prices.index)
        ep = high.copy()
        trend = pd.Series(1, index=prices.index)
        
        for i in range(1, len(prices)):
            sar[i] = sar[i-1] + af[i-1] * (ep[i-1] - sar[i-1])
            
            if trend[i-1] > 0:
                sar[i] = min(sar[i], low[i-1], low[i-2] if i > 1 else low[i-1])
                if high[i] > ep[i-1]:
                    ep[i] = high[i]
                    af[i] = min(af[i-1] + step, max_step)
                else:
                    ep[i] = ep[i-1]
                    af[i] = af[i-1]
                if low[i] < sar[i]:
                    trend[i] = -1
                    sar[i] = ep[i]
                    ep[i] = low[i]
                    af[i] = step
            else:
                sar[i] = max(sar[i], high[i-1], high[i-2] if i > 1 else high[i-1])
                if low[i] < ep[i-1]:
                    ep[i] = low[i]
                    af[i] = min(af[i-1] + step, max_step)
                else:
                    ep[i] = ep[i-1]
                    af[i] = af[i-1]
                if high[i] > sar[i]:
                    trend[i] = 1
                    sar[i] = ep[i]
                    ep[i] = high[i]
                    af[i] = step
            
        return sar.dropna().tail(10).tolist()

    def calculate_bollinger_bands(self, prices, window=20, num_std_dev=2):
        sma = prices['Close'].rolling(window=window).mean()
        rstd = prices['Close'].rolling(window=window).std()
        upper_band = (sma + rstd * num_std_dev).dropna().tail(10).tolist()
        lower_band = (sma - rstd * num_std_dev).dropna().tail(10).tolist()
        return upper_band, lower_band

    def calculate_atr(self, prices, window=14):
        high_low = prices['High'] - prices['Low']
        high_close = np.abs(prices['High'] - prices['Close'].shift())
        low_close = np.abs(prices['Low'] - prices['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(window=window).mean()
        return atr.dropna().tail(10).tolist()

    def calculate_obv(self, prices):
        obv = (np.sign(prices['Close'].diff()) * prices['Volume']).fillna(0).cumsum()
        return obv.dropna().tail(10).tolist()

    def calculate_cmf(self, prices, window=20):
        mfm = ((prices['Close'] - prices['Low']) - (prices['High'] - prices['Close'])) / (prices['High'] - prices['Low'])
        mfv = mfm * prices['Volume']
        cmf = mfv.rolling(window=window).sum() / prices['Volume'].rolling(window=window).sum()
        return cmf.dropna().tail(10).tolist()

    def find_support_resistance(self, prices, window=20):
        local_max = argrelextrema(prices['High'].values, np.greater_equal, order=window)[0]
        local_min = argrelextrema(prices['Low'].values, np.less_equal, order=window)[0]
        resistance = prices['High'].iloc[local_max].tail(5).tolist()
        support = prices['Low'].iloc[local_min].tail(5).tolist()
        return {"support": support, "resistance": resistance}