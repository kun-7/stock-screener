import streamlit as st
import pandas as pd
from src.runner import run

st.title("📊 日本株スクリーナー")

# --- UI設定 ---
st.sidebar.header("スクリーニング条件")

# 修正1: キー(1バイト文字)と表示名(日本語)の「辞書」を定義
screener_options = {
    "volume_price": "出来高＆価格",
    "ma_screener": "移動平均線",
    "all_and": "すべて(AND)"
}

# 修正2: radioボタンのキーと表示名を分離
# options にはキーのリスト (["volume_price", "ma_screener", ...]) を渡す
# format_func で、キーを受け取って辞書から日本語の「表示名」を返すように指定
selected_key = st.sidebar.radio(
    "スクリーナーを選択",
    options=screener_options.keys(),
    format_func=lambda key: screener_options.get(key)
)

tickers_input = st.text_area(
    "ティッカーをカンマ区切りで入力 (例: 7203.T, 9984.T)",
    "7203.T, 6758.T, 9432.T, 9984.T, 8058.T, 4755.T, 6501.T, 7974.T"
)

# --- スクリーニング実行 ---
if st.button("スクリーニング実行"):
    with st.spinner('データ取得・分析中...'):
        tickers = [t.strip() for t in tickers_input.split(",")]
        
        # 修正3: run 関数には日本語の表示名ではなく、
        #        選択された1バイト文字のキー(例: "volume_price")を渡す
        results = run(tickers, selected_key) 

        # 修正4: 結果ヘッダーも辞書から日本語の表示名を取得して表示
        st.subheader(f"📈 結果: {screener_options.get(selected_key)}")

        if results:
            df_results = pd.DataFrame(results)
            
            # 1. 表示したいカラムの「英語キー」を定義（この順番を入れ替える）
            display_cols_english = ["Ticker", "Open", "High", "Low", "Close","Volume"]
            
            # 2. 英語キーと日本語表示名の「辞書」(ここは変更不要)
            column_mapping = {
                "Ticker": "銘柄コード",
                "Close": "終値",
                "Volume": "出来高",
                "Open": "始値",
                "High": "高値",
                "Low": "安値"
            }
            
            # 3. まず英語キーでDataFrameを絞り込み
            df_display = df_results[display_cols_english]
            
            # 4. 絞り込んだDataFrameのカラム名を、辞書を使って日本語に「リネーム」
            df_display = df_display.rename(columns=column_mapping)
            
            # 5. 日本語名になった "銘柄コード" をインデックスに指定して表示
            st.dataframe(df_display.set_index("銘柄コード"))
            
        else:
            st.write("条件に一致する銘柄はありませんでした。")