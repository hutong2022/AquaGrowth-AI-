import pandas as pd
import numpy as np
from pathlib import Path


class DataManager:
    """数据管理器 - 负责数据的加载、清洗和预处理"""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.raw_data = None
        self.processed_data = None

    def load_from_csv(self, file_name: str) -> pd.DataFrame:
        """从CSV文件加载数据"""
        file_path = self.data_path / "raw" / file_name
        try:
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'])
            self.raw_data = df
            print(f"成功加载数据: {len(df)} 条记录")
            return df
        except Exception as e:
            print(f"数据加载失败: {e}")
            return pd.DataFrame()

    def validate_data(self, df: pd.DataFrame) -> bool:
        """数据验证"""
        required_columns = ['date', 'length', 'weight']
        if not all(col in df.columns for col in required_columns):
            print(f"缺少必要列，需要: {required_columns}")
            return False

        if df.isnull().any().any():
            print("数据中存在空值")
            return False

        return True

    def remove_outliers(self, df: pd.DataFrame, method: str = "iqr") -> pd.DataFrame:
        """去除异常值"""
        df_clean = df.copy()

        for column in ['length', 'weight']:
            if method == "iqr":
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                mask = (df[column] >= lower_bound) & (df[column] <= upper_bound)
                df_clean = df_clean[mask]

        removed_count = len(df) - len(df_clean)
        if removed_count > 0:
            print(f"移除了 {removed_count} 个异常值")

        return df_clean

    def create_rolling_dataset(self, df: pd.DataFrame, window_size: int = 30):
        """创建滚动窗口数据集"""
        dates = sorted(df['date'].unique())
        datasets = []

        for i in range(window_size, len(dates)):
            train_dates = dates[i - window_size:i]
            test_date = dates[i]

            train_data = df[df['date'].isin(train_dates)]
            test_data = df[df['date'] == test_date]

            if len(train_data) >= 10 and len(test_data) >= 1:
                datasets.append({
                    'train': train_data,
                    'test': test_data,
                    'train_end_date': train_dates[-1],
                    'test_date': test_date
                })

        return datasets