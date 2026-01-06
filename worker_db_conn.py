import redis
from worker import Worker
import json
import os
from dotenv import load_dotenv
from multiprocessing import Pool

load_dotenv()
HOST = os.getenv('REDIS_HOST')
PORT = int(os.getenv('REDIS_PORT'))

def worker(task):
    task_id = task['task_id']
    data = task['data']

    w_redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True)
    res = Worker.execute(data)
    w_redis_client.hset('done_tasks', task_id, res)


if __name__ == '__main__':
    redis_client = redis.Redis(host=HOST, port=PORT, decode_responses=True)

    with Pool(processes=4) as pool:

        while True:
            _, payload = redis_client.brpop('active_tasks')
            task = json.loads(payload)
            pool.apply_async(worker, args=(task,))