from fastapi import FastAPI
from pydantic import BaseModel

from .classifier import LLMClient

app = FastAPI()
client = LLMClient()


class ProcessRequest(BaseModel):
    csv_path: str


@app.post("/process")
def process_csv(request: ProcessRequest):
    raise NotImplementedError
