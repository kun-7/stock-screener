import streamlit as st
import pandas as pd

@st.cache_data
def get_all_tickers_df():
    url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    
    try:
        # 修正1: pyarrowエラーを完全に回避するため、
        # ヘッダー情報にあった「-」が含まれそうな列をすべて「str」で読み込む
        df = pd.read_excel(url, header=0, dtype={
            "33業種コード": str,
            "17業種コード": str,
            "規模コード": str,
        })
        
        # デバッグコードは不要なので削除
        
        return df
    
    except Exception as e:
        st.error(f"銘柄リスト(Excel)の取得に失敗しました。理由: {e}")
        return pd.DataFrame()

def get_tickers_by_market(market: str) -> list:
    df = get_all_tickers_df()
    if df.empty:
        return []

    try:
        # 修正2: ユーザーが教えてくれた正しい列名「市場・商品区分」を使用する
        if market == "プライム（内国株式）":
            market_df = df[df["市場・商品区分"] == "プライム（内国株式）"]
        elif market == "スタンダード（内国株式）":
            market_df = df[df["市場・商品区分"] == "スタンダード（内国株式）"]
        elif market == "グロース（内国株式）":
            market_df = df[df["市場・商品区分"] == "グロース（内国株式）"]
        else:
            return [] 

        # 「コード」列はそのまま使える
        tickers = [f"{code}.T" for code in market_df["コード"]]
        return tickers
    
    except KeyError as e:
        # ここでエラーが出ることはもう無いはず
        st.error(f"Excelの列名が見つかりません (列名: {e})。東証のファイル形式が変更された可能性があります。")
        return []