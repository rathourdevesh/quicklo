from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings
import asyncio, signal, os


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

async def perform_shutdown_tasks():
    print(f"Performing cleanup tasks with PID : {os.getpid()}")
    # Add your logic here (e.g., closing DB connections, flushing logs, etc.)
    await asyncio.sleep(2)  # Simulate task duration
    print(f"Cleanup completed with PID : {os.getpid()}.")

async def handle_sigterm():
    print(f"SIGTERM signal received. Shutting down gracefully with PID : {os.getpid()}")
    await perform_shutdown_tasks()
    print(f"Application shut down gracefully. with PID : {os.getpid()}")

@app.on_event("shutdown")
async def shutdown_event():
    print(f"Worker with PID : {os.getpid()} {id(asyncio.current_task())} shutdown event triggered.")
    await perform_shutdown_tasks()

loop = asyncio.get_event_loop()
loop.add_signal_handler(
    signal.SIGTERM,
    lambda: asyncio.create_task(handle_sigterm())
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1)
