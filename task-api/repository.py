from sqlalchemy.orm import Session

from models import Task


def get_all_tasks(db: Session):

    return db.query(Task).all()



def get_task(db: Session, task_id: int):

    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )



def create_task(
    db: Session,
    title: str
):

    task = Task(
        title=title,
        done=False
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task



def update_task(
    db: Session,
    task_id: int,
    title=None,
    done=None
):

    task = get_task(
        db,
        task_id
    )

    if task is None:
        return None


    if title is not None:
        task.title = title


    if done is not None:
        task.done = done


    db.commit()
    db.refresh(task)

    return task



def delete_task(
    db: Session,
    task_id: int
):

    task = get_task(
        db,
        task_id
    )

    if task is None:
        return False


    db.delete(task)
    db.commit()

    return True
