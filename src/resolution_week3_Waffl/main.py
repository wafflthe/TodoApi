from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json

app = FastAPI()

TASKS_FILE = "tasks.json"

# Each task will look like: {"id": 1, "task": "Buy milk", "done": False}

class TaskBody(BaseModel):
    task: str

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

@app.get("/tasks")
async def tasks(done: bool | None = None, search: str | None = None):
    tasks = load_tasks()

    if done is not None:
        tasks = [t for t in tasks if t["done"] == done]
    
    if search is not None:
        tasks = [t for t in tasks if search in t["task"]]

    return tasks
# get all tasks + option to search by completion + option to search by name (Case sensetive)

@app.post("/tasks")
async def new_task(task: str):
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = tasks[-1]["id"] + 1
    tasks.append({"id": new_id, "task": task, "done": False})
    save_tasks(tasks)
    return f"Task {task} added with ID of {new_id}"
#add new task

@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return f"Task {task_id} marked as complete"
    raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found")
#mark task deleted based on number
        
@app.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = []
    for task in tasks:
            if task["id"] != task_id:
                new_tasks.append(task)
    tasks = new_tasks

    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found")
    
    save_tasks(tasks)
    return f"Task number {task_id} was deleted"
#delete a task from your list

@app.delete("/tasks/reset")
async def reset():
    tasks = []
    save_tasks(tasks)  
    return "Tasks reset!"  
#deletes all tasks

def main():
    import uvicorn
    uvicorn.run("resolution_week3_YOUR_USERNAME.main:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()