from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, engine, Base
from repository import (
    get_all_tasks,
    get_task,
    create_task,
    update_task,
    delete_task
)


app = FastAPI(
    title="Task API",
    description="A CRUD Task API using PostgreSQL",
    version="3.0"
)


# Create tables
Base.metadata.create_all(bind=engine)



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
        "version": "3.0",
        "database": "PostgreSQL"
    }



@app.get("/health")
def health():

    return {
        "status": "ok"
    }



# GET ALL TASKS

@app.get("/tasks")
def read_tasks(
    db: Session = Depends(get_db)
):

    return get_all_tasks(db)



# GET ONE TASK

@app.get("/tasks/{task_id}")
def read_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = get_task(
        db,
        task_id
    )

    if task is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )

    return task



# CREATE TASK

@app.post("/tasks", status_code=201)
def add_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    if not task.title.strip():

        raise HTTPException(
            status_code=400,
            detail={
                "error": "Title cannot be empty"
            }
        )


    return create_task(
        db,
        task.title
    )



# UPDATE TASK

@app.put("/tasks/{task_id}")
def edit_task(
    task_id: int,
    update: TaskUpdate,
    db: Session = Depends(get_db)
):

    if (
        update.title is not None
        and not update.title.strip()
    ):

        raise HTTPException(
            status_code=400,
            detail={
                "error": "Title cannot be empty"
            }
        )


    task = update_task(
        db,
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



# DELETE TASK

@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    success = delete_task(
        db,
        task_id
    )


    if not success:

        raise HTTPException(
            status_code=404,
            detail={
                "error": "Task not found"
            }
        )


    return


        
