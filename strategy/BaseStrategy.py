import pandas as pd

class TradingAlgorithm:
    def __init__(self, name):
        self.name = name

    def apply_strategy(self, data):
        """
        Apply the trading strategy to the data.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    # def evaluate(self, data):
    #     # Apply the strategy to calculate returns
    #     data = self.apply_strategy(data)

    #     # Initialize variables for tracking positions and returns
    #     position = 0  # 1 for holding the stock, 0 for no position
    #     initial_balance = 100  # Assume starting with $100
    #     balance = initial_balance

    #     for i in range(1, len(data)):
    #         if data['Signal'].iloc[i] == 1 and position == 0:  # Buy signal
    #             position = data['Close'].iloc[i]  # Buy at the current close price
    #         elif data['Signal'].iloc[i] == -1 and position > 0:  # Sell signal
    #             balance += (data['Close'].iloc[i] - position) / position * balance
    #             position = 0  # Reset position after selling

    #     # If still holding a position at the end, sell it
    #     if position > 0:
    #         balance += (data['Close'].iloc[-1] - position) / position * balance

    #     # Calculate net percentage return
    #     net_percentage_return = ((balance - initial_balance) / initial_balance) * 100
    #     return net_percentage_return