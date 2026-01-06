import redis
from worker import Worker
import json
import os
from dotenv import load_dotenv
from multiprocessing import Process

load_dotenv()
HOST = os.getenv('REDIS_HOST')
PORT = int(os.getenv('REDIS_PORT'))


def worker():
    redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True)

    while True:
        _, payload = redis_client.brpop('active_tasks')
        task = json.loads(payload)
        task_id = task['task_id']
        data = task['data']

        res = Worker.execute(data)
        redis_client.hset('done_tasks', task_id, res)

if __name__ == '__main__':
    for _ in range(4):
        Process(target=worker).start()

