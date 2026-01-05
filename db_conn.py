import redis
import uuid
import json
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('REDIS_HOST')
PORT = int(os.getenv('REDIS_PORT'))

class DBConnector:
    def __init__(self):
        self.redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True)

    def add_task(self, data: str) -> str:
        task_id = str(uuid.uuid4())
        payload = json.dumps({'task_id': task_id, 'data': data})
        self.redis_client.lpush('active_tasks',payload)
        return task_id

    def get_task(self, task_id: str) -> str|None:
        data = self.redis_client.hget('done_tasks', task_id)
        return data