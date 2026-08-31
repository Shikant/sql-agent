from app.agent import generate_and_run, is_valid
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
    return {'status': 'ok'}


@app.post('/ask', response_model=AskResponse)
def ask(req: AskRequest):
    result = generate_and_run(req.question)

    if 'error' in result:
        return AskResponse(
            sql=result['sql'],
            rows=[[result['error']]]
        )

    return AskResponse(
        sql=result['sql'],
        rows=result['rows']
    )
