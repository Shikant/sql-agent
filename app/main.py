from fastapi import FastAPI
from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str
class AskResponse(BaseModel):
    sql: str
    rows: list
app = FastAPI()
@app.get('/health')
def health():
    return {'status':'ok'}