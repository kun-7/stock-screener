import streamlit as st
import pandas as pd
from src.runner import run

st.title("📊 日本株スクリーナー")

# --- UI設定 ---
st.sidebar.header("スクリーニング条件")
screener_options = ["出来高・価格", "ゴールデンクロス"]
screener_name = st.sidebar.radio("スクリーナーを選択", screener_options)

tickers_input = st.text_area(
    "ティッカーをカンマ区切りで入力 (例: 7203.T, 9984.T)",
    "7203.T, 6758.T, 9432.T, 9984.T, 8058.T, 4755.T, 6501.T, 7974.T"
)

# --- スクリーニング実行 ---
if st.button("スクリーニング実行"):
    with st.spinner('データ取得・分析中...'):
        tickers = [t.strip() for t in tickers_input.split(",")]
        results = run(tickers, screener_name)

        st.subheader(f"📈 結果: {screener_name}")

        if results:
            df_results = pd.DataFrame(results)
            # 表示するカラムを整形
            display_cols = ["Ticker", "Close", "Volume", "Open", "High", "Low"]
            st.dataframe(df_results[display_cols].set_index("Ticker"))
        else:
            st.write("条件に一致する銘柄はありませんでした。")
