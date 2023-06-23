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
    content = await file.read()
    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(io.BytesIO(content))
    else:
        return {"error": "Unsupported file format"}

    # use ML

    return {"filename": file.filename, "dataframe": df.to_dict(orient='records')}
