import asyncio
import json
import logging
import os
import redis.asyncio as aioredis
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult
from celery_worker import execute_task
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.post("/execute")
async def execute_code(request: dict, background_tasks: BackgroundTasks):
    """Accepts code, sends to Celery"""
    logging.info("Execute request: language_id=%s", request.get("language_id"))
    task = execute_task.delay(request)
    return {"task_id": task.id}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == "PENDING":
        return {"status": "processing"}

    if task_result.state == "FAILURE":
        return JSONResponse(
            status_code=500,
            content={"status": "error", "output": str(task_result.result)}
        )

    if task_result.state == "SUCCESS":
        return task_result.result

    return {"status": task_result.state.lower()}


@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """WebSocket for Redis Pub/Sub"""
    await websocket.accept()

    client = aioredis.from_url(REDIS_URL, db=1)
    pubsub = client.pubsub()
    await pubsub.subscribe(f"task:{task_id}")

    try:
        for _ in range(20):  # wait up to ~10 seconds
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.5)
            if message:
                await websocket.send_json(json.loads(message["data"]))
                break
            await asyncio.sleep(0.5)
    except Exception as e:
        await websocket.send_json({"status": "error", "output": f"WebSocket error: {e}"})
    finally:
        await pubsub.unsubscribe(f"task:{task_id}")
        await pubsub.aclose()
        await client.aclose()
        await websocket.close()
