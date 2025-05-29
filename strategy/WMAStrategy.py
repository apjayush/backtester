from strategy.BaseStrategy import TradingAlgorithm
import yfinance as yf
import pandas as pd

class WMACrossoverStrategy(TradingAlgorithm):
    def __init__(self, stock, start_date, end_date, timeframe='1d'):
        super().__init__("WMA Crossover")
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.data = self._fetch_stock_data()

    def _fetch_stock_data(self):
        data = yf.download(self.stock, start=self.start_date, end=self.end_date, interval=self.timeframe)
        return data

        # data.index = data.index.tz_convert('Asia/Kolkata')
        # return data

    def apply_strategy(self, data=None):
        data = self.data.copy()

        data = data.dropna()
        # Reset index to ensure proper indexing after dropping rows
        data = data.reset_index()

        
        # Calculate WMA20
        data['WMA20'] = data['Close'].rolling(window=20).apply(
            lambda x: (x * range(1, 21)).sum() / sum(range(1, 21)),
            raw=True
        )

        data['Signal'] = 0

        # Create a new DataFrame with just Close and WMA20 columns to ensure alignment
        trading_data = pd.DataFrame()
        
        # Create aligned DataFrame with required columns
        trading_data['Open'] = data['Open']
        trading_data['High'] = data['High']
        trading_data['Low'] = data['Low']
        trading_data['Close'] = data['Close']
        trading_data['WMA20'] = data['WMA20']
        trading_data['Signal'] = 0

        # Generate buy/sell signals using trading_data
        trading_data.loc[(trading_data['Close'] > trading_data['WMA20']) & 
                        (trading_data['Close'].shift(1) <= trading_data['WMA20'].shift(1)), 'Signal'] = 1  # Buy signal
        trading_data.loc[(trading_data['Close'] < trading_data['WMA20']) & 
                        (trading_data['Close'].shift(1) >= trading_data['WMA20'].shift(1)), 'Signal'] = -1  # Sell signal



        # Initialize tracking variables
        position = 0
        buy_price = 0
        total_profit = []
        returns = []

            # Implement backtesting loop
        for i in range(1, len(trading_data)):
        # Buy Signal
            if trading_data['Signal'].iloc[i] == 1 and position == 0:
                position = 1
                buy_price = float(trading_data['Close'].iloc[i])
                print(f"\nBuy Signal at {trading_data.index[i]}")
                print(f"Buy Price: {buy_price:.2f}")
            
            # Check for exit conditions if in position
            elif position == 1:
                current_price = float(trading_data['Close'].iloc[i])
                
                # Calculate stop loss and target
                stop_loss = buy_price * 0.98
                target_price = buy_price * 1.05
                
                # Exit conditions
                if (current_price <= stop_loss or 
                    current_price >= target_price or 
                    trading_data['Signal'].iloc[i] == -1):
                    
                    profit = current_price - buy_price
                    returns_pct = (profit / buy_price) * 100
                    
                    total_profit.append(profit)
                    returns.append(returns_pct)
                    
                    print(f"\nSell Signal at {trading_data.index[i]}")
                    print(f"Sell Price: {current_price:.2f}")
                    print(f"Trade Return: {returns_pct:.2f}%")
                    
                    position = 0
                    buy_price = 0
        
        # Print backtest results
        if returns:
            avg_return = sum(returns) / len(returns)
            total_profit_sum = sum(total_profit)
            print(f"\nBacktesting Results for {self.stock}:")
            print(f"Number of Trades: {len(returns)}")
            print(f"Total Profit/Loss: {total_profit_sum:.2f}")
            print(f"Average Return per Trade: {avg_return:.2f}%")
            return trading_data, avg_return
        
        print(f"\nNo trades executed for {self.stock}")
        return trading_data, 0