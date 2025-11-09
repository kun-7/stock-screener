import streamlit as st
import pandas as pd
from src.runner import run
from src.market_data import get_tickers_by_market

st.title("📊 日本株スクリーナー")

# --- UI設定 ---
st.sidebar.header("スクリーニング条件")

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

st.sidebar.header("スクリーニング対象")

market_options = ["プライム（内国株式）", "スタンダード（内国株式）", "グロース（内国株式）"]
selected_market = st.sidebar.selectbox(
    "市場を選択",
    market_options
)

# --- スクリーニング実行 ---
if st.button("スクリーニング実行"):
    with st.spinner(f'【{selected_market}】市場の銘柄データを取得・分析中...'):
        
        tickers = get_tickers_by_market(selected_market)
        
        if not tickers:
            st.error("銘柄リストが取得できませんでした。")
            st.stop()
            
        st.write(f"（対象銘柄数: {len(tickers)} 件）") # 取得件数を表示

        with st.spinner(f'全 {len(tickers)} 銘柄の株価データを一括取得中...（これには数十秒かかります）'):
            progress_bar = st.progress(0, text="処理開始...")
            results = run(tickers, selected_key, progress_bar) 
        progress_bar.empty()

        st.subheader(f"📈 結果: {screener_options.get(selected_key)}")

        if results:
            df_results = pd.DataFrame(results)
            
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