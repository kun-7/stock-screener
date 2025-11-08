# 修正済みの相対インポート
from .data_fetcher import get_stock_data
from .screeners.volume_price import VolumePriceScreener
from .screeners.ma_screener import MAScreener

# run 関数の定義（引数2つ）はそのまま
def run(tickers, screener_name: str):
    
    # 実行するスクリーナーの選択ロジックもそのまま
    screeners = []
    if screener_name == "出来高＆価格":
        screeners = [VolumePriceScreener()]
    elif screener_name == "移動平均線":
        screeners = [MAScreener(period=25)]
    elif screener_name == "すべて(AND)":
        screeners = [
            VolumePriceScreener(),
            MAScreener(period=25)
        ]
    
    # 変更点 1: このリストに「辞書」を入れていく
    results = []
    
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
            # 変更点 2: 銘柄(t)をそのまま追加するのではなく、
            #            最新の行データを取得する
            latest = df.iloc[-1]
            
            # 変更点 3: UIで必要なデータを辞書として作成
            data_row = {
                "Ticker": t,
                "Close": latest["Close"],
                "Volume": latest["Volume"],
                "Open": latest["Open"],
                "High": latest["High"],
                "Low": latest["Low"]
                # (もしMAスクリーンで計算した 'SMA' も表示したいなら)
                # "SMA_25": latest.get("SMA") 
            }
            # 変更点 4: 辞書を results リストに追加
            results.append(data_row)
            
    # 変更点 5: results は ['7203.T'] ではなく、
    #  [ {'Ticker': '7203.T', 'Close': 3650, ...}, ... ] という
    #  「辞書のリスト」として返される
    return results

if __name__ == "__main__":
    tickers = ["7203.T", "6758.T", "9432.T"]
    passed = run(tickers, "すべて(AND)")
    
    # 出力が変わる（辞書のリストが表示される）
    print("スクリーニング通過:", passed)