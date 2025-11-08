import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period="3mo", interval="1d") -> pd.DataFrame:
    """
    日本株のティッカーは 例: 7203.T (トヨタ)
    """
    tk = yf.Ticker(ticker)
    df = tk.history(period=period, interval=interval)
    return df
