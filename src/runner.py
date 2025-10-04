from data_fetcher import get_stock_data
from screeners.volume_price import VolumePriceScreener

def run(tickers):
    screener = VolumePriceScreener()
    results = []
    for t in tickers:
        df = get_stock_data(t)
        if df.empty:
            continue
        if screener.filter(df):
            results.append(t)
    return results

if __name__ == "__main__":
    tickers = ["7203.T", "6758.T", "9432.T"]  # トヨタ, ソニー, NTT
    passed = run(tickers)
    print("スクリーニング通過:", passed)
