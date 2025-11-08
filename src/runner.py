# (インポートは変更なし)
from .data_fetcher import get_stock_data
from .screeners.volume_price import VolumePriceScreener
from .screeners.ma_screener import MAScreener

# 修正1: 引数名を screener_name から screener_key に変えると分かりやすい
def run(tickers, screener_key: str):
    
    screeners = []
    # 修正2: 比較対象を日本語の文字列から1バイト文字のキーに変更
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
    # (以下のスクリーニング実行ロジックは変更なし)
    for t in tickers:
        df = get_stock_data(t)
        if df.empty:
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
    # 修正3: 直接実行のテスト時もキー("all_and")で呼び出す
    passed = run(tickers, "all_and")
    
    print("スクリーニング通過:", passed)