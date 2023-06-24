import datetime
import io

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

from .core.config import settings
from .utils import predict

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

vars = {
    'obj_prg': "obj_prg",
    'obj_subprg': "obj_subprg",
    'obj_key': "obj_key",
    'task_code': "Кодзадачи",
    'task_name': "НазваниеЗадачи",
    'task_completion': "ПроцентЗавершенияЗадачи",
    'task_start_date': "ДатаНачалаЗадачи",
    'task_end_date': "ДатаОкончанияЗадачи",
    'bp_start_date': "ДатаначалаБП0",
    'bp_end_date': "ДатаокончанияБП0",
    'status_expertise': "Статуспоэкспертизе",
    'expertise': "Экспертиза",
    'date_report': "date_report"
}
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def predict_by_file(file: UploadFile = File(...)):
    """
    Принимает файл xls/xlsx или csv
    Возвращает список отклонений от дат завершения работ
    """
    content = await file.read()
    if file.filename.endswith('.csv'):
        try:
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        except Exception as e:
            return {"error": f"bad csv file: \n{e}"}
    elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        try:
            df = pd.read_excel(io.BytesIO(content))
        except Exception as e:
            return {"error": f"bad excel file: \n {e}"}
    else:
        return {"error": "Unsupported file format"}

    for column in vars.values():
        if column == "date_report":
            continue
        if column not in df:
            return {"error": f"Missed column {v}"}
    try:
        result = predict(df)
        print(df.head(), "ДатаОкончанияЗадачи" in df)
        for i, date in enumerate(df["ДатаОкончанияЗадачи"]):
            for format in ["%d/%m/%Y", "%d%m%Y", "%Y.%m.%d", "%Y-%m-%d"]:
                try:
                    result[i] = (datetime.datetime.strptime(date, format).date() + datetime.timedelta(
                        days=result[i])).strftime(format)
                except:
                    continue
                break
            else:
                return {"error": f"Unsupported date format: {date}"}
    except Exception as e:
        return {"error": f"can't predict: {e}"}
    return {"predict": result}


@app.post("/predict/")
async def predict_by_fields(data: dict = {}):
    """
    Принимает json c полями
    Возвращает отклонение от даты окончания
    """

    l = {}
    for k in vars:
        if k in data:
            l[vars[k]] = [data[k]] if data[k] is not None else np.nan

    df = pd.DataFrame.from_dict(l)

    try:
        result = predict(df)
    except Exception as e:
        return {"error": f"can't predict: {e}"}
    for format in ["%d/%m/%Y", "%d%m%Y", "%Y.%m.%d", "%Y-%m-%d", "%d/%m/%y"]:
        try:
            res = (datetime.datetime.strptime(df["ДатаОкончанияЗадачи"][0], format).date() + datetime.timedelta(
                days=result[0])).strftime(format)
        except:
            continue
        break
    else:
        return {"error": f"Unsupported date format: {df['ДатаОкончанияЗадачи'][0]}"}
    return {"predict": res}


@app.post("/update_attr/")
async def update_attr(file: UploadFile = File(...)):
    """
    Эндпоинт для обновления файла attr.csv, нужного для предсказания
    """
    content = await file.read()
    if file.filename.endswith('.csv'):
        try:
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        except Exception as e:
            return {"error": f"bad csv file: \n{e}"}
    elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        try:
            df = pd.read_excel(io.BytesIO(content))
        except Exception as e:
            return {"error": f"bad excel file: \n {e}"}
    else:
        return {"error": "Unsupported file format"}

    df.to_csv("./attr.csv")

    return {"result": "updated"}
