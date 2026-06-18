# TodoApi
A todolist api utilizing fastapi

Shows list of tasks with an option for searching by completion or by keyword: /task 

(Add true/false to search for completed/incomplete tasks or a keyword to search for it or both)

Adds a new task to the list of tasks: /task/{NewTasksName}

Marks a task complete based on ID: /task/{task_id}/complete

Deletes a task based on ID: /task/{task_id}/delete

Resets and deletes entire Todolist: /task/reset

Download from TestPyPi here: https://test.pypi.org/project/resolution-week3-Waffl/#description
