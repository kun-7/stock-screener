import streamlit as st
import pandas as pd
from src.runner import run
from src.market_data import get_tickers_by_market # 追記

st.title("📊 日本株スクリーナー")

# --- UI設定 ---
st.sidebar.header("スクリーニング条件")

# (スクリーナー選択の部分は変更なし)
screener_options = {
    "volume_price": "出来高＆価格",
    "ma_screener": "移動平均線",
    "all_and": "すべて(AND)"
}
selected_key = st.sidebar.radio(
    "スクリーナーを選択",
    options=screener_options.keys(),
    format_func=lambda key: screener_options.get(key)
)

st.sidebar.header("スクリーニング対象") # 追記

# 修正: text_area を selectbox に変更
market_options = ["プライム（内国株式）", "スタンダード（内国株式）", "グロース（内国株式）"]
selected_market = st.sidebar.selectbox(
    "市場を選択",
    market_options
)

# (↓ 元の text_area はコメントアウト または 削除)
# tickers_input = st.text_area(
#     "ティッカーをカンマ区切りで入力 (例: 7203.T, 9984.T)",
#     "7203.T, 6758.T, 9432.T, 9984.T, 8058.T, 4755.T, 6501.T, 7974.T"
# )

# --- スクリーニング実行 ---
if st.button("スクリーニング実行"):
    with st.spinner(f'【{selected_market}】市場の銘柄データを取得・分析中...'):
        
        # 修正: 選択された市場からティッカーリストを取得
        tickers = get_tickers_by_market(selected_market)
        
        # (↓ 元の text_area から読み込むコードは削除)
        # tickers = [t.strip() for t in tickers_input.split(",")]
        
        if not tickers:
            st.error("銘柄リストが取得できませんでした。")
            st.stop()
            
        st.write(f"（対象銘柄数: {len(tickers)} 件）") # 取得件数を表示

        # ▼▼▼ 修正 ▼▼▼
        # 1. 「一括ダウンロード中」のスピナーを表示
        with st.spinner(f'全 {len(tickers)} 銘柄の株価データを一括取得中...（これには数十秒かかります）'):
            # 2. プログレスバーはまだ出さずに、run() を呼び出す
            #    (この内部で、まず get_batch_stock_data が実行される)
            progress_bar = st.progress(0, text="処理開始...")
            results = run(tickers, selected_key, progress_bar) 
        # ▲▲▲ 修正 ▲▲▲

        # 修正: 処理完了後、プログレスバーを消す
        progress_bar.empty()

        st.subheader(f"📈 結果: {screener_options.get(selected_key)}")

        if results:
            df_results = pd.DataFrame(results)
            
            # (↓ 表示カラムの順番と日本語化の部分は変更なし)
            display_cols_english = ["Ticker", "Open", "High", "Low", "Close", "Volume"]
            column_mapping = {
                "Ticker": "銘柄コード",
                "Close": "終値",
                "Volume": "出来高",
                "Open": "始値",
                "High": "高値",
                "Low": "安値"
            }
            df_display = df_results[display_cols_english]
            df_display = df_display.rename(columns=column_mapping)
            st.dataframe(df_display.set_index("銘柄コード"))
            
        else:
            st.write("条件に一致する銘柄はありませんでした。")