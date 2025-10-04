from .base import Screener

class VolumePriceScreener(Screener):
    def filter(self, df):
        """
        出来高10万以上 & 終値500円以上 の銘柄を通す
        """
        latest = df.iloc[-1]
        return (latest["Volume"] > 100000) and (latest["Close"] > 500)
