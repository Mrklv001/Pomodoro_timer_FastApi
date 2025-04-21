from fastapi import APIRouter, status
from database.database import get_db_session
from schema.task import Task

router = APIRouter(prefix="/task", tags=["ping"])


# GET________________________
@router.get(
    "/all",
    response_model=list[Task]
)
async def get_tasks():
    result: list[Task] = []
    cursor = get_db_session().cursor()
    tasks = cursor.execute("SELECT * FROM Tasks").fetchall()
    for task in tasks:
        result.append(Task(
            id=task[0],
            name=task[1],
            pomodoro_count=task[2],
            category_id=task[3]
        ))

    return result


# POST________________________
@router.post(
    "/",
    response_model=Task
)
async def create_task(task: Task):
    connection = get_db_session()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Tasks (name, pomodoro_count, category_id) VALUES (?, ?, ?)",
                   (task.name, task.pomodoro_count, task.category_id))
    connection.commit()
    connection.close()
    return task


# PATCH________________________
@router.patch(
    "/{task_id}",
    response_model=Task
)
async def patch_task(task_id: int, name: str):
    connection = get_db_session()
    cursor = connection.cursor()
    cursor.execute("UPDATE Tasks SET name =? WHERE id=?", (name, task_id))
    connection.commit()
    task = cursor.execute("SELECT * FROM Tasks WHERE id=?", f"{task_id}").fetchall()[0]
    connection.close()
    return Task(
        id=task[0],
        name=task[1],
        pomodoro_count=task[2],
        category_id=task[3]
    )


# DELETE________________________
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    connection = get_db_session()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id=?", (task_id,))
    connection.commit()
    connection.close()

    return {"message": "task deleted successfully"}
