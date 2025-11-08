import pandas as pd
from .base import Screener

class MAScreener(Screener):
    def __init__(self, period=25):
        self.period = period

    def filter(self, df: pd.DataFrame) -> bool:
        """
        終値が指定した期間(period)の移動平均線を上回っているか判定
        """
        if len(df) < self.period:
            # データが移動平均を計算するのに足りない場合は除外
            return False
        
        # 移動平均を計算
        df['SMA'] = df['Close'].rolling(window=self.period).mean()
        
        # 最新（最後）のデータを取得
        latest = df.iloc[-1]
        
        # 終値 > 移動平均線 かつ 移動平均線が計算済み(NaNでない)か
        return latest['Close'] > latest['SMA'] and not pd.isna(latest['SMA'])