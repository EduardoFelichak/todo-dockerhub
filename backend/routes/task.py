from flask           import Blueprint, request, jsonify
from models.task     import Task
from config.database import db

task_bp = Blueprint("task_bp", __name__)

@task_bp.route("/", methods = ["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route("/", methods = ["POST"])
def create_task():
    data  = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "Título é obrigatório"}), 400
    
    new_task = Task(title = title)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task não encontrada!"}), 404

    data = request.json
    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)
    db.session.commit()
    return jsonify(task.to_dict())

@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task não encontrada"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deletada com sucesso!"})