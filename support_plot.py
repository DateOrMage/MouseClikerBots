from pandas import DataFrame


def get_x_y_cooor_and_label(df: DataFrame, col_name: str, cell_value: any) -> tuple:

    df_row = df[df[col_name] == cell_value]
    coord_list = df_row['x_y_unix'].iloc[0].split(';')

    x_coords = [int(coord.split(',')[0]) for coord in coord_list]
    y_coords = [int(coord.split(',')[1]) for coord in coord_list]

    if df_row['Bot'].iloc[0] == 0:
        label = f"User {df_row['ID'].iloc[0]} - Не бот"
    else:
        label = f"User {df_row['ID'].iloc[0]} - Бот"

    return x_coords, y_coords, label


if __name__ =='__main__':
    import pandas as pd
    data = pd.read_excel("C:\\Users\\Пользователь\\Downloads\\pp_unix_mini.xlsx")
    # data = data.rename(columns={'Координаты с отпечатком времени в unix формате (кол-во миллисекунд с 01.01.1970)':
                                # 'x_y_unix'})

    x, y, lab = get_x_y_cooor_and_label(data, col_name='ID', cell_value=102193)
