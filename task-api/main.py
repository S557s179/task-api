from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import (
    initialize_database,
    get_all_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)

app = FastAPI(
    title="Task API",
    description="A simple CRUD Task API built with FastAPI",
    version="2.0"
)

# Create database/table on startup
initialize_database()


# Request Models
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


# Root
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# GET all tasks
@app.get("/tasks")
def get_tasks():
    return get_all_tasks()


# GET one task
@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):

    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    return task


# CREATE
@app.post("/tasks", status_code=201)
def add_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Title cannot be empty"
            }
        )

    return create_task(task.title)


# UPDATE
@app.put("/tasks/{task_id}")
def edit_task(task_id: int, update: TaskUpdate):

    if update.title is not None and not update.title.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Title cannot be empty"
            }
        )

    task = update_task(
        task_id,
        update.title,
        update.done
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    return task


# DELETE
@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):

    success = delete_task(task_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    return
        
