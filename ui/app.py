import streamlit as st
from src.runner import run

st.title("📊 日本株スクリーナー（デモ）")

tickers_input = st.text_area(
    "ティッカーをカンマ区切りで入力してください (例: 7203.T, 6758.T, 9432.T)",
    "7203.T, 6758.T, 9432.T"
)

if st.button("スクリーニング実行"):
    tickers = [t.strip() for t in tickers_input.split(",")]
    results = run(tickers)
    st.write("✅ 通過銘柄:", results if results else "なし")
