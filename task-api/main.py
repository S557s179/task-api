from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Task API",
    description="A simple CRUD Task API built with FastAPI",
    version="1.0"
)


# In-memory database
tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Deploy Project",
        "done": True
    }
]


# Request models
class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


# Stage 1
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Stage 2
@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task {task_id} not found"
        }
    )


# Stage 3
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Title cannot be empty"
            }
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task


# Stage 4
@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):

    for task in tasks:

        if task["id"] == task_id:

            if update.title is not None:

                if not update.title.strip():
                    raise HTTPException(
                        status_code=400,
                        detail={
                            "error": "Title cannot be empty"
                        }
                    )

                task["title"] = update.title


            if update.done is not None:
                task["done"] = update.done


            return task


    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task {task_id} not found"
        }
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            return


    raise HTTPException(
        status_code=404,
        detail={
            "error": f"Task {task_id} not found"
        }
    )
