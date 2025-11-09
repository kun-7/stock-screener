# (インポートは変更なし)
from .data_fetcher import get_stock_data
from .screeners.volume_price import VolumePriceScreener
from .screeners.ma_screener import MAScreener

# 修正1: 第3引数として progress_bar を追加 (None をデフォルトにしておく)
def run(tickers, screener_key: str, progress_bar=None):
    
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
    total = len(tickers) # 全件数を取得

    # 修正2: enumerate を使って、ループのインデックス(i)も取得する
    for i, t in enumerate(tickers):
        
        # ▼▼▼ 追記 ▼▼▼
        # プログレスバーを更新
        if progress_bar:
            percent_complete = (i + 1) / total
            progress_bar.progress(percent_complete, text=f"処理中: {t} ({i + 1}/{total})")
        # ▲▲▲ 追記 ▲▲▲
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