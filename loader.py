import pandas as pd


df = pd.read_csv('/home/tik_home/repositories/stravanalytics/data_source/activities.csv')

print(df.describe())

print(df.mean())