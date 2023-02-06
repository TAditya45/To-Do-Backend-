from flask import Flask, request
import csv

app = Flask(__name__)

tasks = []

def add_task(task):
    task["marked"] = False
    tasks.append(task)
    with open("tasks.csv", "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["task", "marked"])
        writer.writerow(task)

def get_tasks():
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def update_task(task_id, task):
    tasks[task_id] = task
    with open("tasks.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["task", "marked"])
        writer.writeheader()
        writer.writerows(tasks)

def delete_task(task_id):
    del tasks[task_id]
    with open("tasks.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["task", "marked"])
        writer.writeheader()
        writer.writerows(tasks)

def mark_task(task_id):
    tasks[task_id]["marked"] = True
    with open("tasks.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["task", "marked"])
        writer.writeheader()
        writer.writerows(tasks)

def unmark_task(task_id):
    tasks[task_id]["marked"] = False
    with open("tasks.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["task", "marked"])
        writer.writeheader()
        writer.writerows(tasks)

@app.route("/tasks", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "POST":
        task = request.get_json()
        add_task(task)
        return "Task added", 201
    else:
        return get_tasks(), 200

@app.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def handle_task(task_id):
    if request.method == "PUT":
        task = request.get_json()
        update_task(task_id, task)
        return "Task updated", 200
    else:
        delete_task(task_id)
        return "Task deleted", 200

@app.route("/tasks/<int:task_id>/mark", methods=["PUT"])
def handle_mark_task(task_id):
    mark_task(task_id)
    return "Task marked", 200

@app.route("/tasks/<int:task_id>/unmark", methods=["PUT"])
def handle_unmark_task(task_id):
    unmark_task(task_id)
    return "Task unmarked", 200

if name == 'main':
app.run()