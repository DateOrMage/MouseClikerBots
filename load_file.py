from pandas import read_excel, DataFrame
import gc


class LoadFile:
    def __init__(self, input_folder: str) -> None:
        self.input_path: str = input_folder
        self.flag: bool = True
        self.output_text: str = 'Файл успешно загружен.'

    def load_excel(self):
        df = read_excel(self.input_path)

        return df

    def check_columns(self, df: DataFrame) -> DataFrame:
        try:
            for col_name in df.columns:
                if col_name.startswith('Координаты с отпечатком времени в unix'):
                    df = df.rename(columns={col_name: 'x_y_unix'})
                    break
            df = df[['ID', 'ACCOUNT_ID', 'CREATED', 'Кол-во координат', 'x_y_unix']]
        except KeyError:
            self.output_text = 'Error: Неверное название столбцов, см. руководство пользователя.'
            self.flag = False

        return df

    @staticmethod
    def check_nan(df: DataFrame) -> DataFrame:
        if df.isnull().sum().sum() > 0:
            df = df.dropna().reset_index(drop=True)

        return df

    def check_up(self, df: DataFrame) -> DataFrame:
        df = self.check_columns(df)
        if not self.flag:
            return df
        df = self.check_nan(df)

        return df

    def execute(self):
        df = self.load_excel()
        df = self.check_up(df)
        gc.collect()

        return df, self.output_text, self.flag


if __name__ == '__main__':
    lf = LoadFile("C:\\Users\\Пользователь\\Downloads\\Координаты движения мыши Unix mini.xlsx")
    data, text, flag = lf.execute()
    import time
    # from classification_bots import ClassificationBots
    # start = time.time()
    # cb = ClassificationBots()
    # data = cb.execute(data)
    # stop = time.time()
    # print(f'Data analyze time is {round(stop-start)} sec.')
    # # data.to_excel("C:\\Users\\Пользователь\\Downloads\\pp_unix_mini.xlsx")
    # from clusterization import Clusterization
    # data = Clusterization().get_cluster_by_session(data)
    # print(data)
    # stat_data = Clusterization().get_cluster_by_user(data)
