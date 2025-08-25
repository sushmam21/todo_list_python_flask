from flask import Flask, render_template, request, redirect, jsonify
import json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path("data/tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        tasks = load_tasks()
        tasks.append({"task": task, "done": False})
        save_tasks(tasks)
    return redirect("/")


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)
    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)