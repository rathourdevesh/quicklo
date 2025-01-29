from fastapi import APIRouter, BackgroundTasks
from app.core.logger_config import logger
import asyncio, os

router = APIRouter()

async def bg(id_, req_id):
    import time
    logger.info(f"started bg with PID : {os.getpid()} asyncio id : {id(asyncio.current_task())} and request id {req_id} task id {id_}")
    time.sleep(10)
    logger.info(f"ending bg with PID : {os.getpid()} asyncio id : {id(asyncio.current_task())} and request id {req_id} task id {id_}")

@router.get("/health/{req_id}")
async def healthz(
    req_id: int,
    bg_task: BackgroundTasks
):
    """
    health check.
    """
    print(f"received PID : {os.getpid()} request id {req_id} with asyncio id:  {id(asyncio.current_task())} ")
    bg_task.add_task(bg, 1, req_id)
    bg_task.add_task(bg, 2, req_id)
    bg_task.add_task(bg, 3, req_id)
    bg_task.add_task(bg, 4, req_id)
    print(f"sending response PID : {os.getpid()} request id {req_id} with asyncio id:  {id(asyncio.current_task())} ")
    return {
        "success": True,
        "message": "server is up"
    }
