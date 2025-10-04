import pandas as pd

class Screener:
    def filter(self, df: pd.DataFrame) -> bool:
        """
        各スクリーナーは DataFrame を受け取り
        True/False を返す
        """
        raise NotImplementedError
