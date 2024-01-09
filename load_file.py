from pandas import read_excel, DataFrame


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
            df = df[['ID', 'ACCOUNT_ID', 'CREATED', 'Кол-во координат',
                     'Координаты с отпечатком времени в unix формате (кол-во миллисекунд с 01.01.1970)']]
            df = df.rename(columns={'Координаты с отпечатком времени в unix формате (кол-во миллисекунд с 01.01.1970)':
                                    'x_y_unix'})
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

        return df, self.output_text, self.flag


if __name__ == '__main__':
    lf = LoadFile("C:\\Users\\Пользователь\\Downloads\\Координаты движения мыши Unix mini.xlsx")
    data, text, flag = lf.execute()
    print(data)
    import time
    from classification_bots import ClassificationBots
    start = time.time()
    cb = ClassificationBots()
    data = cb.execute(data)
    stop = time.time()
    print(f'Data analyze time is {round(stop-start)} sec.')
