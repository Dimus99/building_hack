import pandas as pd

dataset_path = "./data/test.xlsx"
attr_path = "./data/attr_v2.csv"

# Read the dataset and attribute files
dataset = pd.read_excel(dataset_path)
attr = pd.read_csv(attr_path, delimiter=";", on_bad_lines="skip")
print(dataset.head())
print(attr.head)
dataset['date_report'] = pd.to_datetime(dataset['date_report'])
attr['date_report'] = pd.to_datetime(attr['date_report'])


merged_dataframe = pd.merge_asof(dataset, attr, on="date_report", by="obj_key")
print(merged_dataframe.head())
merged_dataframe.to_csv('joined.csv', index=False)


