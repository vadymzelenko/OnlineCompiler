import os

import redis
import json
from celery import Celery
from compiles.pyCompile import run_py
from compiles.jsCompile import run_js
from compiles.cppCompile import run_cpp

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

celery_app = Celery("tasks", broker=f"{REDIS_URL}/0", backend=f"{REDIS_URL}/0")

# Redis Pub/Sub
redis_pub = redis.Redis.from_url(REDIS_URL, db=1)

@celery_app.task(bind=True)
def execute_task(self, request):
    language_id = request.get('language_id')
    result = {}

    if language_id == 71:
        result = run_py(request)
    elif language_id == 63:
        result = run_js(request)
    elif language_id == 54:
        result = run_cpp(request)
    else:
        result = {
            "output": "language not found",
            "status": "error",
        }

    redis_pub.publish(f"task:{self.request.id}", json.dumps(result))
    return result
