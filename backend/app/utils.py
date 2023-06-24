import pandas as pd


def merge_with_attr(dataset):
    attr_path = "./data/attr.csv"
    try:
        attr = pd.read_csv(attr_path, delimiter=";", on_bad_lines="skip")
        dataset['date_report'] = pd.to_datetime(
            dataset['date_report']) if "date_report" in dataset else pd.to_datetime("2023.06.05")
        attr['date_report'] = pd.to_datetime(attr['date_report'])

        return pd.merge_asof(dataset, attr, on="date_report", by="obj_key")
    except FileNotFoundError:
        raise ValueError("Need attr.csv file for predict")
    except Exception as e:
        raise ValueError(f"Error with merging: {e}")


def predict(df):
    pass
