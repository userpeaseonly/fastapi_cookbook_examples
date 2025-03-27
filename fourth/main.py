from fastapi import FastAPI, HTTPException
from operations import read_all_tasks, read_task, create_task, modify_task, remote_task
from typing import List
from models import Task, TaskWithID, UpdateTask

app = FastAPI()

@app.get('/tasks', response_model=List[TaskWithID])
async def get_tasks():
    return read_all_tasks()


@app.get('/tasks/{task_id}', response_model=TaskWithID)
async def get_task(task_id: int):
    task = read_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


@app.post('/task', response_model=TaskWithID)
async def add_task(task: Task):
    return create_task(task)


@app.put('/task/{task_id}', response_model=TaskWithID)
async def update_task(task_id: int, task: UpdateTask):
    modified_task = modify_task(task_id, task)
    if modified_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return modified_task

@app.delete('/task/{task_id}', response_model=TaskWithID)
async def delete_task(task_id: int):
    task = read_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    remote_task(task_id)
    return task