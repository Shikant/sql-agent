from app.agent import generate_sql, is_valid
from fastapi import FastAPI
from pydantic import BaseModel
from app.db import run_sql

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
    sql = generate_sql(req.question)

    if not is_valid(sql):
        return AskResponse(
            sql=sql,
            rows=[["INVALID SQL"]]
        )

    result = run_sql(sql)

    if not result['ok']:
        return AskResponse(
            sql=sql,
            rows=[[result['error']]]
        )

    return AskResponse(
        sql=sql,
        rows=result['rows']
    )

