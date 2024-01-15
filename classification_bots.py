from pandas import DataFrame
import numpy as np


class ClassificationBots:
    __coor_col: str = 'x_y_unix'
    __straight_line_threshold: int = 100

    def get_bot_value(self, x_coords: list, y_coords: list) -> int:
        straight_line_detected = False
        for i in range(2, len(x_coords)):
            if abs((y_coords[i] - y_coords[i - 2]) * (x_coords[i - 1] - x_coords[i - 2]) -
                   (x_coords[i] - x_coords[i - 2]) * (y_coords[i - 1] - y_coords[i - 2])) \
                    < self.__straight_line_threshold:
                straight_line_detected = True
                break
        if straight_line_detected:
            return 0
        else:
            return 1

    @staticmethod
    def get_session_time(unix_time: list) -> tuple:
        sess_time = (max(unix_time) - min(unix_time)) / 1000.0

        return sess_time, len(unix_time)/sess_time

    @staticmethod
    def get_speed_list(x_coords: list, y_coords: list, unix_time: list) -> list:
        speed_list = []
        for i in range(1, len(unix_time)):
            time_diff = (unix_time[i] - unix_time[i - 1]) / 1000.0  # Convert to seconds
            distance = np.sqrt((x_coords[i] - x_coords[i - 1]) ** 2 + (y_coords[i] - y_coords[i - 1]) ** 2)
            if time_diff == 0 and distance == 0:
                speed = 0
            elif time_diff == 0 and distance != 0:
                speed = distance
            else:
                speed = distance / time_diff
            speed_list.append(speed)
        return speed_list

    @staticmethod
    def get_acceleration_list(speed_list: list, unix_time: list) -> list:
        acceleration_list = []
        for i in range(1, len(unix_time) - 1):
            time_diff = (unix_time[i + 1] - unix_time[i - 1]) / 1000.0  # Convert to seconds
            speed_distance = speed_list[i] - speed_list[i - 1]
            if time_diff == 0 and speed_distance == 0:
                acceleration = 0
            elif time_diff == 0 and speed_distance != 0:
                acceleration = abs(speed_distance)
            else:
                acceleration = abs((speed_list[i] - speed_list[i - 1]) / time_diff)
            acceleration_list.append(acceleration)
        return acceleration_list

    def data_analyze(self, df: DataFrame) -> DataFrame:
        df['Bot'] = np.zeros(len(df), dtype='int8')
        df['Session time'] = np.nan
        df['APS'] = np.nan
        df['Max speed'] = np.nan
        df['Max acceleration'] = np.nan
        # df['Min acceleration'] = np.nan

        for index, cell_value in enumerate(df[self.__coor_col]):
            try:
                coord_list = cell_value.split(';')
            except AttributeError:
                continue

            if coord_list[-1].endswith(','):
                coord_list = coord_list[:-1]

            if len(coord_list[-1].split(',')) < 3:
                coord_list = coord_list[:-1]

            if len(coord_list[-1].split(',')[-1]) < 12:
                coord_list = coord_list[:-1]

            if len(coord_list) < 3:
                continue

            is_no_data = False
            for k in range(len(coord_list)):
                if len(coord_list[k].split(',')) < 3:
                    is_no_data = True
                    break
            if is_no_data:
                continue

            x_coords = [int(coord.split(',')[0]) for coord in coord_list]
            y_coords = [int(coord.split(',')[1]) for coord in coord_list]
            unix_time = [int(coord.split(',')[2]) for coord in coord_list]

            # df.loc[index, 'Bot'] = self.get_bot_value(x_coords, y_coords)
            df.loc[index, 'Session time'], df.loc[index, 'APS'] = self.get_session_time(unix_time)

            speed_list = self.get_speed_list(x_coords, y_coords, unix_time)
            acceleration_list = self.get_acceleration_list(speed_list, unix_time)

            df.loc[index, 'Max speed'] = np.max(speed_list)
            df.loc[index, 'Max acceleration'] = np.max(acceleration_list)
            # df.loc[index, 'Min acceleration'] = np.min(acceleration_list)

        bot_idx = df[df['APS'] > 3].index
        df.loc[bot_idx, 'Bot'] = 1
        return df

    def execute(self, df: DataFrame) -> DataFrame:
        df = self.data_analyze(df)
        if df.isnull().sum().sum() > 0:
            df = df.dropna().reset_index(drop=True)

        return df


if __name__ == '__main__':
    pass
