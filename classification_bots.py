from pandas import DataFrame
import numpy as np


class ClassificationBots:
    __coor_col: str = 'x_y_unix'
    __straight_line_threshold: int = 100

    def trajectory_analyze(self, df: DataFrame) -> DataFrame:
        df['Bot'] = np.zeros(len(df), dtype='int8')
        for index, cell_value in enumerate(df[self.__coor_col]):
            try:
                coord_list = cell_value.split(';')
            except AttributeError:
                print('Not str: ', index, cell_value)
                continue

            if coord_list[-1].endswith(','):
                coord_list = coord_list[:-1]

            if len(coord_list) < 3:
                print('coord_list < 3: ', index, cell_value)
                continue

            is_no_data = False
            for k in range(len(coord_list)):
                if len(coord_list[k].split(',')) < 3:
                    print('coord_value < 3: ', index, cell_value)
                    is_no_data = True
                    break
            if is_no_data:
                continue

            x_coords = [int(coord.split(',')[0]) for coord in coord_list]
            y_coords = [int(coord.split(',')[1]) for coord in coord_list]

            straight_line_detected = False
            for i in range(2, len(coord_list)):
                if abs((y_coords[i] - y_coords[i-2]) * (x_coords[i - 1] - x_coords[i-2]) -
                       (x_coords[i] - x_coords[i-2]) * (y_coords[i - 1] - y_coords[i-2]))\
                        < self.__straight_line_threshold:
                    straight_line_detected = True
                    break

            if not straight_line_detected:
                df.loc[index, 'Bot'] = 1

        return df

    def execute(self, df: DataFrame) -> DataFrame:
        df = self.trajectory_analyze(df)

        return df


if __name__ == '__main__':
    pass
