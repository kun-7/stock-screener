from .data_fetcher import get_batch_stock_data
from .screeners.volume_price import VolumePriceScreener
from .screeners.ma_screener import MAScreener

def run(tickers, screener_key: str, progress_bar=None):
    
    screeners = []
    if screener_key == "volume_price":
        screeners = [VolumePriceScreener()]
    elif screener_key == "ma_screener":
        screeners = [MAScreener(period=25)]
    elif screener_key == "all_and":
        screeners = [
            VolumePriceScreener(),
            MAScreener(period=25)
        ]
    
    results = []
    all_data = get_batch_stock_data(tickers, progress_bar=progress_bar)
    
    total = len(tickers)
    for i, t in enumerate(tickers):

        if progress_bar:
            percent_complete = (i + 1) / total
            progress_bar.progress(percent_complete, text=f"[分析中] {t} ({i + 1}/{total})")
        
        try:
            df = all_data[t].copy()
            if df.empty or df['Close'].isnull().all():
                continue 
        except KeyError:
            print(f"警告: {t} のデータが all_data に見つかりません。スキップします。")
            continue
            
        passed_all = True
        for screener in screeners:
            if not screener.filter(df):
                passed_all = False
                break
        
        if passed_all:
            latest = df.iloc[-1]
            data_row = {
                "Ticker": t,
                "Close": latest["Close"],
                "Volume": latest["Volume"],
                "Open": latest["Open"],
                "High": latest["High"],
                "Low": latest["Low"]
            }
            results.append(data_row)
            
    return results

if __name__ == "__main__":
    tickers = ["7203.T", "6758.T", "9432.T"]
    passed = run(tickers, "all_and")
    
    print("スクリーニング通過:", passed)