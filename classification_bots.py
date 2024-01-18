import time

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
    def get_session_time(unix_time: list) -> float:

        return (max(unix_time) - min(unix_time)) / 1000.0

    @staticmethod
    def get_length_list(x_coords: list, y_coords: list, unix_time: list) -> list:
        length_list = []
        for i in range(1, len(unix_time)):
            distance = np.sqrt((x_coords[i] - x_coords[i - 1]) ** 2 + (y_coords[i] - y_coords[i - 1]) ** 2)
            length_list.append(distance)
        return length_list

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

    @staticmethod
    def get_duplicate_return_points(x_coords: list, y_coords: list) -> int:
        coords_str = [",".join([str(x), str(y)]) for x, y in zip(x_coords, y_coords)]
        n_duplicates = 0
        for i in range(1, len(coords_str)-1):
            if coords_str[i] == coords_str[i - 1]:
                continue
            if coords_str[i-1] == coords_str[i+1]:
                x1, y1 = coords_str[i-1].split(',')
                x2, y2 = coords_str[i].split(',')
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                return_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if return_length > 30:
                    n_duplicates += 1

        return n_duplicates

    @staticmethod
    def get_no_cross(x_coords, y_coords):
        x_sign_list = np.unique(np.sign(np.diff(x_coords)))
        y_sign_list = np.unique(np.sign(np.diff(y_coords)))
        x_sign_list = x_sign_list[x_sign_list != 0]
        y_sign_list = y_sign_list[y_sign_list != 0]
        if len(x_sign_list) > 1 and len(y_sign_list) > 1:
            return 0
        else:
            return 1

    @staticmethod
    def get_line_coef(x1: int, x2: int, y1: int, y2: int) -> tuple:
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return k, b

    @staticmethod
    def get_line_length(line: list) -> float:
        return np.sqrt((line[0][0] - line[-1][0])**2 + (line[0][1] - line[-1][1])**2)

    def get_length_straight_line(self, x_coords: list, y_coords: list) -> float:
        current_straight_line = []
        max_straight_line_length = 0
        # n_straight_lines = 0
        i = 0
        while i < len(x_coords) - 2:
            # x1 != x2, y1 != y2
            if x_coords[i] != x_coords[i + 1]:
                k, b = self.get_line_coef(x_coords[i], x_coords[i + 1], y_coords[i], y_coords[i + 1])
                current_straight_line.append((x_coords[i], y_coords[i]))
                current_straight_line.append((x_coords[i + 1], y_coords[i + 1]))
                i += 2
                while i < len(x_coords) - 2:
                    if x_coords[i] == x_coords[i - 1]:
                        i += 1
                        continue
                    if k * x_coords[i] + b == y_coords[i]:
                        current_straight_line.append((x_coords[i], y_coords[i]))
                        i += 1
                    else:
                        if len(current_straight_line) > 3:
                            # n_straight_lines += 1
                            line_length = self.get_line_length(current_straight_line)
                            if max_straight_line_length < line_length:
                                max_straight_line_length = line_length
                        current_straight_line = []
                        break

            # x1 = x2, y1 != y2
            elif x_coords[i] == x_coords[i + 1] and y_coords[i] != y_coords[i + 1]:
                x_const = x_coords[i]
                current_straight_line.append((x_coords[i], y_coords[i]))
                current_straight_line.append((x_coords[i + 1], y_coords[i + 1]))
                i += 2
                while i < len(x_coords) - 2:
                    if y_coords[i] == y_coords[i - 1]:
                        i += 1
                        continue
                    if x_coords[i] == x_const:
                        current_straight_line.append((x_coords[i], y_coords[i]))
                        i += 1
                    else:
                        if len(current_straight_line) > 3:
                            # n_straight_lines += 1
                            line_length = self.get_line_length(current_straight_line)
                            if max_straight_line_length < line_length:
                                max_straight_line_length = line_length
                        current_straight_line = []
                        break
            else:
                i += 1

        return max_straight_line_length  # , n_straight_lines

    def data_analyze(self, df: DataFrame) -> DataFrame:

        df['Session time'] = np.nan
        df['Avg length'] = np.nan
        df['Std length'] = np.nan
        # df['Min speed'] = np.nan
        # df['Max speed'] = np.nan
        # df['Avg speed'] = np.nan
        df['Std speed'] = np.nan
        # df['Min acceleration'] = np.nan
        # df['Max acceleration'] = np.nan
        # df['Avg acceleration'] = np.nan
        # df['Std acceleration'] = np.nan

        df['No cross'] = np.nan
        df['Straight length'] = np.nan
        # df['Straight line number'] = np.nan
        # df['Straight line frequency'] = np.nan

        df['Duplicate points'] = np.nan
        # df['Duplicate points max'] = np.nan
        # df['Min acceleration'] = np.nan
        df['Bot'] = ''

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
            session_time = self.get_session_time(unix_time)
            if session_time < 30:
                continue
            df.loc[index, 'Session time'] = session_time

            length_list = self.get_length_list(x_coords, y_coords, unix_time)
            speed_list = self.get_speed_list(x_coords, y_coords, unix_time)
            acceleration_list = self.get_acceleration_list(speed_list, unix_time)

            df.loc[index, 'Avg length'] = np.mean(length_list)
            df.loc[index, 'Std length'] = np.std(length_list)

            df.loc[index, 'Std speed'] = np.std(speed_list)

            df.loc[index, 'No cross'] = self.get_no_cross(x_coords, y_coords)
            df.loc[index, 'Straight length'] = self.get_length_straight_line(x_coords, y_coords)
            df.loc[index, 'Duplicate points'] = self.get_duplicate_return_points(x_coords, y_coords)

            bot_class_list = []
            if df.loc[index, 'Avg length'] > 100:
                bot_class_list.append('1')
            if df.loc[index, 'Std length'] > 100:
                bot_class_list.append('2')
            if df.loc[index, 'Std speed'] < 250:
                bot_class_list.append('3')
            if df.loc[index, 'No cross'] == 1:
                bot_class_list.append('4')
            if df.loc[index, 'Straight length'] > 100:
                bot_class_list.append('5')
            if df.loc[index, 'Duplicate points'] > 0:
                bot_class_list.append('6')

            if len(bot_class_list) == 0:
                bot_class_list.append('0')
            bot_value = ';'.join(bot_class_list)
            df.loc[index, 'Bot'] = bot_value



        return df

    def execute(self, df: DataFrame) -> DataFrame:
        df = self.data_analyze(df)
        if df.isnull().sum().sum() > 0:
            df = df.dropna().reset_index(drop=True)

        return df


if __name__ == '__main__':
    pass
