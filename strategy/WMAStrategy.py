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

    # def _calculate_wma(self, series, period=20):
    #     weights = pd.Series(range(1, period + 1))
    #     return series.rolling(window=period).apply(
    #         lambda x: (x * weights).sum() / weights.sum()
    #     )

    def _calculate_wma(self, series, period=20):
        """Calculate Weighted Moving Average using simple range multiplication"""
        return series.rolling(window=period).apply(
            lambda x: (x * range(1, period + 1)).sum() / sum(range(1, period + 1)),
            raw=True
        )

    def apply_strategy(self, data=None):
        data = self.data.copy()  # Create a copy to avoid modifying original data

        
        # Calculate 20-period WMA
        data['WMA20'] = self._calculate_wma(data['Close'], 20)
        
        # Generate buy/sell signals
        data['Signal'] = 0

        print(data)

        print("***************")
        
        # Create conditions for buy/sell signals
        buy_condition = (data['Close'] > data['WMA20']) & (data['Close'].shift(1) <= data['WMA20'].shift(1))
        sell_condition = (data['Close'] < data['WMA20']) & (data['Close'].shift(1) >= data['WMA20'].shift(1))
        
        # Apply signals
        data.loc[buy_condition, 'Signal'] = 1
        data.loc[sell_condition, 'Signal'] = -1

        print(data)
        # Initialize tracking variables
        position = 0
        buy_price = 0
        total_profit = []
        returns = []

        print

        # Loop through the data to implement trading logic
        for i in range(1, len(data)):
            current_price = data['Close'].iloc[i]
            
            # Buy signal
            if data['Signal'].iloc[i] == 1 and position == 0:
                position = 1
                buy_price = current_price
                print(f"Bought at price: {buy_price}")

            # Manage position
            if position == 1:
                # Set stop loss and target
                stop_loss = buy_price * 0.98
                target_price = buy_price * 1.05

                # Check for exit conditions
                if (current_price <= stop_loss or 
                    current_price >= target_price or 
                    data['Signal'].iloc[i] == -1):
                    
                    profit = current_price - buy_price
                    returns_pct = (profit / buy_price) * 100
                    
                    total_profit.append(profit)
                    returns.append(returns_pct)
                    
                    print(f"Sold at price: {current_price}")
                    print(f"Trade return: {returns_pct:.2f}%")
                    
                    position = 0
                    buy_price = 0

        if returns:
            avg_return = sum(returns) / len(returns)
            print(f"Total Profit/Loss: {sum(total_profit):.2f}")
            print(f"Average Return per Trade: {avg_return:.2f}%")
            return avg_return
        return 0