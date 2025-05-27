import yfinance as yf
from strategy.Backtesting import Backtester
from strategy.MovingAverage import MovingAverageCrossover

def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

if __name__ == "__main__":
    # Fetch stock data
    stock = "KFINTECH.NS"
    start_date = "2024-05-01"
    end_date = "2025-05-26"
    data = fetch_stock_data(stock, start_date, end_date)

    # Initialize algorithms
    algorithms = [
        MovingAverageCrossover(),
    ]

    # Run backtesting
    backtester = Backtester(data, algorithms)
    results = backtester.run()

    # Find the best algorithm
    best_algo = max(results, key=results.get)
    print(f"Best Algorithm for {stock}: {best_algo} with return {results[best_algo]}")