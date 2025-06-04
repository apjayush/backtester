from strategy.BaseStrategy import TradingAlgorithm
import yfinance as yf


class MovingAverageCrossover(TradingAlgorithm):
    def __init__(self, stock, start_date, end_date, timeframe='1d'):
        super().__init__("Moving Average Crossover")
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.data = self._fetch_stock_data()

    def _fetch_stock_data(self):
        data = yf.download(self.stock, start=self.start_date, end=self.end_date, interval=self.timeframe)
        data.index = data.index.tz_convert('Asia/Kolkata')
        return data

    def apply_strategy(self, data=None):
        data = self.data.copy()

        data = data.dropna()
        data = data.drop(columns=['Volume'])

        data = data.reset_index()
        # Calculate 9 EMA and 21 EMA
        data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
        data['EMA_21'] = data['Close'].ewm(span=21, adjust=False).mean()

        # Generate buy/sell signals
        data['Signal'] = 0  # Default to no signal
        data.loc[(data['EMA_9'] > data['EMA_21']) & (data['EMA_9'].shift(1) <= data['EMA_21'].shift(1)), 'Signal'] = 1  # Buy signal
        data.loc[(data['EMA_9'] < data['EMA_21']) & (data['EMA_9'].shift(1) >= data['EMA_21'].shift(1)), 'Signal'] = -1  # Sell signal

        ticker = data['Close'].columns[0]
        # print("Ticker:", ticker)

        print(data)
        # Initialize variables for tracking positions and returns
        position = 0  # Number of shares held
        buy_price = 0  # Price at which the stock was bought
        total_profit = []  # Total profit/loss\
        returns = []  # List to store returns for each trade


        for i in range(1, len(data)):

            # Check for buy signal
            if data['Signal'].iloc[i] == 1 and position == 0:
                position = 1  # Buy one share
                buy_price = data['Close'].iloc[i][ticker]  # Record the buy price
                print("Bought at price:", buy_price)

            # Check for sell conditions
            if position == 1:
                # Calculate stop loss and target prices
                stop_loss = buy_price * 0.96  # 4% below buy price
                target_price = buy_price * 1.12  # 12% above buy price

                # # # # Check if stop loss or target is hit
                if data['Close'].iloc[i][ticker] <= stop_loss or data['Close'].iloc[i][ticker] >= target_price:
                    print("Sold at price:", data['Close'].iloc[i][ticker])
                    profit = (data['Close'].iloc[i][ticker] - buy_price)  # Gain/loss from the trade
                    total_profit.append(profit)
                    returns.append((profit / buy_price)*100)  # Calculate return for this trade
                    position = 0  # Reset position after selling
                    buy_price = 0  # Reset buy price


                # # # Check if 9 EMA crosses below 21 EMA
                elif data['Signal'].iloc[i] == -1:
                    print("Sold at price:", data['Close'].iloc[i][ticker])
                    profit = (data['Close'].iloc[i][ticker] - buy_price)  # Gain/loss from the trade
                    total_profit.append(profit)
                    returns.append((profit / buy_price)*100) # Calculate return for this trade
                    position = 0  # Reset position after selling
                    buy_price = 0  # Reset buy price
                
                # else:
                #     total_profit = (data['Close'].iloc[i]['APOLLO.NS'] - buy_price)
                    # print(total_profit)
                
               
        print("Total Profit/Loss:", sum(total_profit))
        # print("Total Returns:", (returns))

        print("Average return per trade:", sum(total_profit)/len(returns) if returns else 0)
        # Return the total profit/loss as a percentage of the initial balance
        return (total_profit / data['Close'].iloc[0]) * 100