import io

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
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
    try:
        result = predict(df)
        print(result)
    except Exception as e:
        return {"error": f"can't predict: {e}"}
    return {"predict": result}


@app.post("/predict/")
async def predict_by_fields(data):
    """
    Принимает json c полями
    Возвращает отклонение от даты окончания
    """
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
    l = {}
    for k in vars:
        l[vars[k]] = [data[k]]
    df = pd.DataFrame.from_dict(l)

    try:
        result = predict(df)
    except Exception as e:
        return {"error": f"can't predict: {e}"}

    return {"predict": result}


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
