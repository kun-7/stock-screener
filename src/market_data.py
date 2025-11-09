import streamlit as st
import pandas as pd

@st.cache_data
def get_all_tickers_df():
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    
    try:
        df = pd.read_excel(url, header=0, dtype={
            "33業種コード": str,
            "17業種コード": str,
            "規模コード": str,
        })
        
        return df
    
    except Exception as e:
        st.error(f"銘柄リスト(Excel)の取得に失敗しました。理由: {e}")
        return pd.DataFrame()

def get_tickers_by_market(market: str) -> list:
    df = get_all_tickers_df()
    if df.empty:
        return []

    try:
        if market == "プライム（内国株式）":
            market_df = df[df["市場・商品区分"] == "プライム（内国株式）"]
        elif market == "スタンダード（内国株式）":
            market_df = df[df["市場・商品区分"] == "スタンダード（内国株式）"]
        elif market == "グロース（内国株式）":
            market_df = df[df["市場・商品区分"] == "グロース（内国株式）"]
        else:
            return [] 

        tickers = [f"{code}.T" for code in market_df["コード"]]
        return tickers
    
    except KeyError as e:
        st.error(f"Excelの列名が見つかりません (列名: {e})。東証のファイル形式が変更された可能性があります。")
        return []