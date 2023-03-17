from flask import render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import connexion

app = connexion.FlaskApp(__name__, specification_dir="./")
app.add_api("swagger.yml")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def get_todo_list():
    todo_list = Todo.query.all()
    return render_template("home.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.json.get("task")
    if not task:
        return jsonify({"status": "error", "message": "Invalid input"}), 400
    new_todo = Todo(task=task, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"status": "success", "message": "Task added successfully"}), 201


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"status": "error", "message": "Task not found"}), 404
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("get_todo_list"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"status": "error", "message": "Task not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("get_todo_list"))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
