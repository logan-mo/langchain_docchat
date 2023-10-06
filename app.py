from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
import os
import openai
import shutil
import json
from model import Model
import numpy as np

api_key = "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"
os.environ["OPENAI_API_KEY"] = api_key
openai.api_key = os.environ["OPENAI_API_KEY"]

model = Model(api_key)

# To run app, Use:
# uvicorn app:app --reload
app = FastAPI()
# with open('openai_api_key.txt', 'r') as f:
#    os.environ['OPENAI_API_KEY'] = f.read()


DOCUMENT_STORE_PATH = "documents"

if not os.path.exists(DOCUMENT_STORE_PATH):
    os.mkdir(DOCUMENT_STORE_PATH)


@app.get("/")
def home():
    return "API is live"


@app.post("/add_document")
async def add_source(
    file: Annotated[UploadFile, Form()], user_id: Annotated[str, Form()]
):
    if not os.path.exists(DOCUMENT_STORE_PATH):
        os.mkdir(DOCUMENT_STORE_PATH)
    if not os.path.exists(os.path.join(DOCUMENT_STORE_PATH, user_id)):
        os.mkdir(os.path.join(DOCUMENT_STORE_PATH, user_id))

    file_path = os.path.join(DOCUMENT_STORE_PATH, user_id, "data.csv")

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": "data.csv",
        "saved_path": file_path,
    }


@app.post("/ask_question")
def query(query: Annotated[str, Form()], user_id: Annotated[str, Form()]):
    response = model.generate(
        query,
        user_id=user_id,
    )

    return {"msg": response}
