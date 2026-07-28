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

@app.post('/ask', response_model=AskResponse)
def ask(req: AskRequest):
    return AskResponse(sql='SELECT 1', rows=[[1]])