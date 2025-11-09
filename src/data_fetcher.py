import yfinance as yf
import pandas as pd
import time
from tenacity import retry, stop_after_attempt, wait_exponential


def get_stock_data(ticker: str, period="3mo", interval="1d") -> pd.DataFrame:
    tk = yf.Ticker(ticker)
    df = tk.history(period=period, interval=interval)
    return df

# ▼▼▼ この関数を丸ごと差し替え ▼▼▼
def get_batch_stock_data(tickers: list, period="3mo", interval="1d", progress_bar=None): # 修正1: progress_bar を引数で受け取る
    
    chunk_size = 100 
    all_data_frames = []
    
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10) 
    )
    def download_chunk_with_retry(chunk, current_chunk_num, total_chunks):
        print(f"  > [チャンク {current_chunk_num} / {total_chunks}] ( {len(chunk)} 件) をダウンロード試行中...")
        
        data = yf.download(
            tickers=chunk,
            period=period,
            interval=interval,
            group_by='tickers',
            auto_adjust=True,
            threads=True 
        )
        
        failed_tickers = [t for t in chunk if t not in data.columns.get_level_values(0) and data.empty]
        if not data.empty and any(data[t]['Close'].isnull().all() for t in chunk if t in data.columns):
             failed_tickers.extend([t for t in chunk if t in data.columns and data[t]['Close'].isnull().all()])

        if len(failed_tickers) > 0:
            print(f"  > !!! [チャンク {current_chunk_num} / {total_chunks}] が失敗したため、リトライします... (失敗: {failed_tickers})")
            raise Exception(f"チャンクダウンロード失敗: {failed_tickers}")
            
        return data

    print(f"yfinance: {len(tickers)} 件のデータを {chunk_size} 件ずつのチャンクでダウンロード開始")
    total_chunks = -(-len(tickers) // chunk_size)

    for i in range(0, len(tickers), chunk_size):
        chunk = tickers[i : i + chunk_size]
        current_chunk_num = (i // chunk_size) + 1
        
        # ▼▼▼ 追記 ▼▼▼
        # 修正2: ダウンロード「前」に、UIのプログレスバーを更新
        if progress_bar:
            # 進捗は「今何件目か / 総件数」で計算 (例: 0/1616, 100/1616, ...)
            percent_complete = i / len(tickers)
            progress_bar.progress(percent_complete, text=f"[ダウンロード {current_chunk_num} / {total_chunks}] 実行中...")
        # ▲▲▲ 追記 ▲▲▲

        try:
            data = download_chunk_with_retry(chunk, current_chunk_num, total_chunks)
            all_data_frames.append(data)
            
        except Exception as e:
            print(f"  > !!! [チャンク {current_chunk_num} / {total_chunks}] が3回のリトライ後も失敗しました: {e}")
            
        time.sleep(0.5) 

    # ▼▼▼ 追記 ▼▼▼
    # 修正3: ダウンロード完了をUIに通知
    if progress_bar:
        progress_bar.progress(1.0, text="[ダウンロード完了] 分析処理に移行...")
    # ▲▲▲ 追記 ▲▲▲

    print("yfinance: 全チャンクのダウンロード完了")
    
    combined_data = pd.concat([df for df in all_data_frames if df is not None], axis=1)
    
    return combined_data