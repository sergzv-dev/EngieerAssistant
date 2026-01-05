from fastapi import FastAPI
from db_conn import DBConnector

app = FastAPI()
base_conn = DBConnector()

@app.post('/question')
def question(req_data: str) -> str:
    return base_conn.add_task(req_data)

@app.post('/answer')
def answer(task_id: str) -> str:
    return base_conn.get_task(task_id)
