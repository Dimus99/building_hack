import numpy as np
import pandas as pd
import xgboost
from sklearn.preprocessing import LabelEncoder


def merge_with_attr(dataset):
    attr_path = "./attr.csv"
    try:
        print(1)
        attr = pd.read_csv(attr_path, delimiter=";", on_bad_lines="skip")
        if "date_report" in dataset:
            print(2)
            dataset['date_report'] = pd.to_datetime(
                dataset['date_report'])
            print(3)
        else:
            print(4)
            dataset['date_report'] = pd.to_datetime("2023.06.05")
        attr['date_report'] = pd.to_datetime(attr['date_report'])
        print(5)

        return pd.merge_asof(dataset, attr, on="date_report", by="obj_key")
    except FileNotFoundError as e:
        raise ValueError(f"Need attr.csv file for predict: {e.__repr__()}")
    except Exception as e:
        raise ValueError(f"Error with merging: {e}")


def predict(df):
    df = merge_with_attr(df)
    date_cols = [
        'ДатаНачалаЗадачи',
        'ДатаОкончанияЗадачи',
        'ДатаначалаБП0',
        'ДатаокончанияБП0',
        'date_report'
    ]
    for date_col in date_cols:
        df[date_col] = pd.to_datetime(df[date_col])

    le_columns = [
        "obj_prg",
        "obj_subprg",
        "obj_key",
        "Кодзадачи",
        "НазваниеЗадачи",
        "ПроцентЗавершенияЗадачи",
        "Экспертиза",
        "состояние площадки",
    ]

    le = LabelEncoder()
    df["Кодзадачи"] = df["Кодзадачи"].astype("str")
    for col in le_columns:
        print(col)
        le.classes_ = np.load(f"building_hack/backend/app/data_files/{col}_calsses.npy", allow_pickle=True)
        df[col] = le.transform(df[col])

    df["month_start"] = df["ДатаНачалаЗадачи"].apply(lambda x: x.month)
    df["season_start"] = df["ДатаНачалаЗадачи"].apply(lambda x: get_season(x))

    df["bp_date_month_start"] = df["ДатаначалаБП0"].apply(lambda x: x.month)
    df["bp_date_season_start"] = df["ДатаначалаБП0"].apply(lambda x: get_season(x))

    df["bp_date_month_end"] = df["ДатаокончанияБП0"].apply(lambda x: x.month)
    df["bp_date_season_end"] = df["ДатаокончанияБП0"].apply(lambda x: get_season(x))

    model = xgboost.XGBRegressor()
    model.load_model("building_hack/backend/app/data_files/w.json")

    result = model.predict(df[model.feature_names_in_])

    return list(result)


def get_season(date):
    if date.month in [12, 1, 2]:
        return 0
    elif date.month in [3, 4, 5]:
        return 1
    elif date.month in [6, 7, 8]:
        return 2
    else:
        return 3
