import redis
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
import time
import threading

class RedisStockCache:
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialize Redis connection and cache settings"""
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        self.cache_duration = 24 * 60 * 60  # 24 hours
        self._lock = threading.Lock()
        
        # Default stocks to track
        self.default_stocks = {
            'AAPL': 'Apple Inc',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc',
            'AMZN': 'Amazon.com Inc',
            'META': 'Meta Platforms Inc',
            'NVDA': 'NVIDIA Corporation',
            'TSLA': 'Tesla Inc',
            'JPM': 'JPMorgan Chase & Co',
            'V': 'Visa Inc',
            'WMT': 'Walmart Inc',
            'PG': 'Procter & Gamble Co',
            'MA': 'Mastercard Inc',
            'HD': 'Home Depot Inc',
            'BAC': 'Bank of America Corp',
            'XOM': 'Exxon Mobil Corporation'
        }

        # Popular tech stocks for suggestions
        self.stock_suggestions = {
            'Technology': [
                'AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'CRM', 'ADBE', 'ORCL'
            ],
            'Finance': [
                'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'V', 'MA', 'AXP', 'BLK'
            ],
            'Healthcare': [
                'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'ABT', 'TMO', 'LLY', 'BMY', 'AMGN'
            ],
            'Consumer': [
                'AMZN', 'WMT', 'PG', 'KO', 'PEP', 'MCD', 'NKE', 'SBUX', 'TGT', 'COST'
            ]
        }

    def _get_key(self, ticker: str) -> str:
        """Generate Redis key for stock data"""
        return f"stock:{ticker}"

    def store_stock_data(self, ticker: str, data: Dict) -> bool:
        """Store stock data in Redis"""
        try:
            with self._lock:
                self.redis_client.setex(
                    self._get_key(ticker),
                    self.cache_duration,
                    json.dumps({
                        'data': data,
                        'timestamp': time.time()
                    })
                )
                return True
        except Exception as e:
            print(f"Error storing data for {ticker}: {str(e)}")
            return False

    def get_stock_data(self, ticker: str) -> Optional[Dict]:
        """Retrieve stock data from Redis"""
        try:
            data = self.redis_client.get(self._get_key(ticker))
            if data:
                return json.loads(data)['data']
            return None
        except Exception as e:
            print(f"Error retrieving data for {ticker}: {str(e)}")
            return None

    def is_data_valid(self, ticker: str) -> bool:
        """Check if cached data is still valid"""
        try:
            data = self.redis_client.get(self._get_key(ticker))
            if not data:
                return False
            
            stored_data = json.loads(data)
            return (time.time() - stored_data['timestamp']) < self.cache_duration
        except:
            return False

    def calculate_metrics(self, data: Dict) -> Dict:
        """Calculate key metrics from stock data"""
        try:
            hist_data = data['stock_price_data']['historical_prices']
            df = pd.DataFrame(hist_data['data'])
            if df.empty:
                return {}
                
            latest_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2] if len(df) > 1 else latest_price
            price_change = latest_price - prev_price
            price_change_percent = (price_change / prev_price * 100) if prev_price != 0 else 0
            
            return {
                'current_price': latest_price,
                'price_change': price_change,
                'price_change_percent': price_change_percent,
                'volume': df['Volume'].iloc[-1] if 'Volume' in df else 0,
                'avg_volume': df['Volume'].mean() if 'Volume' in df else 0,
                'high': df['High'].max() if 'High' in df else latest_price,
                'low': df['Low'].min() if 'Low' in df else latest_price
            }
        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            return {}

    def preload_default_stocks(self, fetch_func) -> None:
        """Preload data for default stocks"""
        def preload_ticker(ticker: str):
            try:
                if not self.is_data_valid(ticker):
                    data = fetch_func(ticker)
                    if data:
                        self.store_stock_data(ticker, data)
            except Exception as e:
                print(f"Error preloading {ticker}: {str(e)}")

        threads = []
        for ticker in self.default_stocks.keys():
            thread = threading.Thread(target=preload_ticker, args=(ticker,))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def get_cached_stocks_data(self) -> Dict[str, Dict]:
        """Get data for all cached stocks"""
        result = {}
        try:
            for ticker in self.default_stocks.keys():
                data = self.get_stock_data(ticker)
                if data:
                    metrics = self.calculate_metrics(data)
                    result[ticker] = {
                        'name': self.default_stocks[ticker],
                        'metrics': metrics
                    }
        except Exception as e:
            print(f"Error getting cached stocks data: {str(e)}")
        return result

    def get_stock_suggestions(self, category: Optional[str] = None) -> List[str]:
        """Get stock suggestions by category"""
        if category and category in self.stock_suggestions:
            return self.stock_suggestions[category]
        return [stock for stocks in self.stock_suggestions.values() for stock in stocks]
