import pandas as pd
from pandas import DataFrame, NamedAgg
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class Clusterization:
    __n_clusters: int = 6
    __random_seed: int = 42

    def get_cluster_by_user(self, df: DataFrame) -> tuple:
        clustering_df = df.groupby('ACCOUNT_ID').agg(
            Number_of_Sessions=NamedAgg(column='ID', aggfunc='count'),
            Average_Avg_length=NamedAgg(column='Avg length', aggfunc='mean'),
            Average_Std_length=NamedAgg(column='Std length', aggfunc='mean'),
            # Average_Min_speed=NamedAgg(column='Min speed', aggfunc='mean'),
            # Average_Max_speed=NamedAgg(column='Max speed', aggfunc='mean'),
            # Average_Avg_speed=NamedAgg(column='Avg speed', aggfunc='mean'),
            Average_Std_speed=NamedAgg(column='Std speed', aggfunc='mean'),

            # Average_No_cross=NamedAgg(column='No cross', aggfunc='mean'),
            Average_Straight_length=NamedAgg(column='Straight length', aggfunc='mean'),
            # Average_Straight_line_number=NamedAgg(column='Straight line number', aggfunc='mean'),
            # Average_Straight_line_frequency=NamedAgg(column='Straight line frequency', aggfunc='mean'),

            Average_Duplicate_points=NamedAgg(column='Duplicate points', aggfunc='mean'),

            Average_Session_Time=NamedAgg(column='Session time', aggfunc='mean'),
            Duplicated_session=NamedAgg(column='Avg length', aggfunc=lambda x: x.duplicated().sum())  # if x.duplicated().sum() == 0 else x.duplicated().sum()+1)
            # Bot_frequency=NamedAgg(column='Bot', aggfunc='mode')
        ).reset_index()
        # print('after agg', clustering_df)

        # print('DF after session_cluster: \n', df)
        # print('Cluster_df: \n', clustering_df)
        # clustering_df['Duplicated_session'] = clustering_df['Duplicated_session'] / clustering_df['Number_of_Sessions']

        scaled_data = clustering_df.drop(['ACCOUNT_ID', 'Number_of_Sessions', 'Average_Session_Time'], axis=1)  # 'Bot_frequency'
        # print('cols for clustrization by users:', scaled_data.columns)
        # scaled_data = np.where(np.abs(scaled_data) > 10000, 10000 * np.sign(scaled_data), scaled_data)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(scaled_data)

        kmeans = KMeans(n_clusters=self.__n_clusters, random_state=self.__random_seed, n_init='auto')
        cluster_labels = kmeans.fit_predict(scaled_data)
        clustering_df['User_cluster'] = cluster_labels
        ###
        cluster_labels = {k: v for k, v in zip(np.argsort(clustering_df['User_cluster'].value_counts()).index,
                                               sorted(clustering_df['User_cluster'].unique()))}
        clustering_df['User_cluster'].replace(cluster_labels, inplace=True)
        ###

        return clustering_df, scaled_data

    # def get_cluster_by_session(self, df: DataFrame) -> DataFrame:
    #     original_data = df.copy()
    #     df = df.drop(['ID', 'ACCOUNT_ID', 'CREATED', 'Кол-во координат', 'x_y_unix', 'Bot', 'No cross', 'Session time'
    #                   ], axis=1)  # 'Duplicate return points'
    #
    #     scaler = StandardScaler()
    #     df = scaler.fit_transform(df)
    #     kmeans = KMeans(n_clusters=self.__n_clusters, random_state=self.__random_seed, n_init='auto')
    #     cluster_labels = kmeans.fit_predict(df)
    #     del df
    #     original_data['Session_cluster'] = cluster_labels
    #     ###
    #     cluster_labels = {k: v for k, v in zip(np.argsort(original_data['Session_cluster'].value_counts()).index,
    #                                            sorted(original_data['Session_cluster'].unique()))}
    #     original_data['Session_cluster'].replace(cluster_labels, inplace=True)
    #     ###
    #     gc.collect()
    #
    #     return original_data

    def execute(self, df: DataFrame) -> tuple:
        # original_data = self.get_cluster_by_session(df)
        clustering_df, scaled_data = self.get_cluster_by_user(df)
        return clustering_df, scaled_data  # original_data,


if __name__ == '__main__':
    pp_data = pd.read_excel('pp_mini_data.xlsx')
    cluster = Clusterization()
    cluster.execute(pp_data)


