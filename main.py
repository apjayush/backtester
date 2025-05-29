import yfinance as yf
from strategy.Backtesting import Backtester
from strategy.MovingAverage import MovingAverageCrossover
from strategy.WMAStrategy import WMACrossoverStrategy
import time

def fetch_stock_data(ticker, start_date, end_date, interval='1d'):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    data.index = data.index.tz_convert('Asia/Kolkata')
    return data

if __name__ == "__main__":
    # Fetch stock data
    stock = "KFINTECH.NS"
    start_date = "2025-05-01"
    end_date = "2025-05-29"
    timeframe = "15m"  # Can be 1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo

    # data = fetch_stock_data(stock, start_date, end_date, timeframe)
    # put some 100 stock name here

    stock_list = [
        "KFINTECH.NS", "TATAMOTORS.NS", "RELIANCE.NS", "HDFCBANK.NS", 
        "INFY.NS", "TCS.NS", "HINDUNILVR.NS", "ICICIBANK.NS", 
        "LT.NS", "HCLTECH.NS", "ASIANPAINT.NS", "MARUTI.NS",
        "BAJFINANCE.NS", "AXISBANK.NS", "ITC.NS", "SBIN.NS",
        "WIPRO.NS", "HDFC.NS", "TECHM.NS", "TATAPOWER.NS",
        "ONGC.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS", "JSWSTEEL.NS",
        "BHARTIARTL.NS", "POWERGRID.NS", "NTPC.NS", "CIPLA.NS",
        "SUNPHARMA.NS", "DRREDDY.NS", "DIVISLAB.NS", "GRASIM.NS",
    ]

    for stock in stock_list:

        # Initialize algorithms with timeframe
        algorithms = [
            MovingAverageCrossover(stock,timeframe="1h",start_date=start_date, end_date=end_date)
            # WMACrossoverStrategy(stock, start_date=start_date, end_date=end_date, timeframe=timeframe),
        ]

        # Run backtesting
        backtester = Backtester(algorithms)
        results = backtester.run()

        time.sleep(2)

        # Find the best algorithm
        best_algo = max(results, key=results.get)
        print(f"Best Algorithm for {stock}: {best_algo} with return {results[best_algo]}")