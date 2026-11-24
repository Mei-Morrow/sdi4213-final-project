import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from psycopg.rows import dict_row
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = logging.getLogger("uvicorn.error")


def connect_db():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        dbname=os.getenv("POSTGRES_DB", "tasktracker"),
        user=os.getenv("POSTGRES_USER", "tasktracker"),
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=3,
        options="-c statement_timeout=3000",
        row_factory=dict_row,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect_db() as connection:
        # Serialize schema setup when multiple app replicas start together.
        connection.execute("SELECT pg_advisory_xact_lock(4213)")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE
            )
            """
        )
    logger.info("Database schema is ready.")
    yield


app = FastAPI(
    title="DevOps Task Tracker",
    version="0.1.0",
    lifespan=lifespan,
)


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        pattern=r"\S",
    )


class Task(BaseModel):
    id: int
    title: str
    completed: bool


@app.exception_handler(psycopg.Error)
async def database_error_handler(request: Request, exc: psycopg.Error):
    logger.error("Database request failed: %s", type(exc).__name__)
    return JSONResponse(
        status_code=503,
        content={"detail": "Database temporarily unavailable"},
    )


@app.get("/")
def index():
    return {
        "application": "DevOps Task Tracker",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/healthz")
def healthz():
    return {"status": "alive"}


@app.get("/ready")
def ready():
    try:
        with connect_db() as connection:
            connection.execute("SELECT 1")
    except psycopg.Error:
        return JSONResponse(
            status_code=503,
            content={"status": "not ready"},
        )
    return {"status": "ready"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    with connect_db() as connection:
        row = connection.execute(
            """
            INSERT INTO tasks (title)
            VALUES (%s)
            RETURNING id, title, completed
            """,
            (task.title.strip(),),
        ).fetchone()
    return row


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id"
        ).fetchall()
    return rows