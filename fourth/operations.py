import csv
from typing import List, Dict, Any, Optional
from models import Task, TaskWithID

DATABASE_FILENAME = 'tasks.csv'

column_fields = ['id', 'title', 'description', 'status']


def read_all_tasks() -> List[TaskWithID]:
    with open(DATABASE_FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        return [TaskWithID(**row) for row in reader]


def read_task(task_id: int) -> Optional[TaskWithID]:
    with open(DATABASE_FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['id']) == task_id:
                return TaskWithID(**row)


def get_next_id():
    try:
        with open(DATABASE_FILENAME, 'r') as file:
            reader = csv.DictReader(file)
            ids = [int(row['id']) for row in reader]
            return max(ids) + 1 if ids else 1
    except (FileNotFoundError, ValueError):
        return 1


def write_task_into_csv(task: TaskWithID):
    with open(DATABASE_FILENAME, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        writer.writerow(task.model_dump())


def create_task(task: Task) -> TaskWithID:
    task_id = get_next_id()
    task_with_id = TaskWithID(id=task_id, **task.model_dump())
    write_task_into_csv(task_with_id)
    return task_with_id


def modify_task(task_id: int, task: Task) -> TaskWithID:
    with open(DATABASE_FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
    with open(DATABASE_FILENAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        writer.writeheader()
        for row in rows:
            if int(row['id']) == task_id:
                row.update(task.model_dump())
            writer.writerow(row)
    return TaskWithID(id=task_id, **task.model_dump())

def remote_task(task_id: int) -> Optional[TaskWithID]:
    with open(DATABASE_FILENAME, 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
    with open(DATABASE_FILENAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        writer.writeheader()
        for row in rows:
            if int(row['id']) == task_id:
                task = TaskWithID(**row)
                continue
            writer.writerow(row)
    return task