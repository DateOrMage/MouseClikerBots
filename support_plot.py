from pandas import DataFrame


def get_x_y_cooor_and_label(df: DataFrame, row_idx: int) -> tuple:

    coord_list = df['x_y_unix'][row_idx].split(';')

    x_coords = [int(coord.split(',')[0]) for coord in coord_list]
    y_coords = [int(coord.split(',')[1]) for coord in coord_list]

    if df['Bot'][row_idx] == 0:
        label = f"User {df['ACCOUNT_ID'][row_idx]} - Не бот"
    else:
        label = f"User {df['ACCOUNT_ID'][row_idx]} - Бот"

    return x_coords, y_coords, label

