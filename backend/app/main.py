import io

from fastapi import FastAPI, UploadFile, File
import pandas as pd

from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def predict_by_file(file: UploadFile = File(...)):
    """
    Принимает файл xls/xlsx или csv и возвращает предсказание
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

    # use ML

    return {"filename": file.filename, "dataframe": df.to_dict(orient='records')}


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

    df.to_csv("../attr.csv")

    return {"result": "updated"}
