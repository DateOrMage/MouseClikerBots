from pandas import DataFrame, NamedAgg
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import gc


class Clusterization:
    __n_clusters: int = 3
    __random_seed: int = 42

    def get_cluster_by_user(self, df: DataFrame) -> DataFrame:
        clustering_df = df.groupby('ACCOUNT_ID').agg(
            Number_of_Sessions=NamedAgg(column='ID', aggfunc='count'),
            Average_Max_Speed=NamedAgg(column='Max speed', aggfunc='mean'),
            Average_Max_Acceleration=NamedAgg(column='Max acceleration', aggfunc='mean'),
            Average_Min_Acceleration=NamedAgg(column='Min acceleration', aggfunc='mean'),
            Average_Session_Time=NamedAgg(column='Session time', aggfunc='mean'),
            Bot_frequency=NamedAgg(column='Bot', aggfunc='mean')
        ).reset_index()

        print('DF after session_cluster: \n', df)
        print('Cluster_df: \n', clustering_df)

        scaled_data = clustering_df.drop(['ACCOUNT_ID', 'Bot_frequency'], axis=1)
        scaled_data = np.where(np.abs(scaled_data) > 10000, 10000 * np.sign(scaled_data), scaled_data)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(scaled_data)

        kmeans = KMeans(n_clusters=self.__n_clusters, random_state=self.__random_seed, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_data)
        clustering_df['User_cluster'] = cluster_labels

        return clustering_df

    def get_cluster_by_session(self, df: DataFrame) -> DataFrame:
        original_data = df.copy()
        print(original_data)
        print(df)
        df = df.drop(['ID', 'ACCOUNT_ID', 'x_y_unix'], axis=1)
        print('DF after drop cols\n', df)
        df = np.where(np.abs(df) > 10000, 10000 * np.sign(df), df)
        scaler = StandardScaler()
        df = scaler.fit_transform(df)
        print('DF after scaler\n', df)
        kmeans = KMeans(n_clusters=self.__n_clusters, random_state=self.__random_seed, n_init=10)
        cluster_labels = kmeans.fit_predict(df)
        del df
        original_data['Session_cluster'] = cluster_labels
        gc.collect()

        return original_data



