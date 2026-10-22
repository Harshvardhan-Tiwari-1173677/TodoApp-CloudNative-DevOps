from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = [
    {"id": 1, "title": "Complete Assessment 1", "completed": False},
    {"id": 2, "title": "Test the To-Do application", "completed": False}
]
next_id = 3


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    original_count = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]

    if len(tasks) == original_count:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
