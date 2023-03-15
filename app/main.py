from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def todo_list():
    todo_list = Todo.query.all()
    return render_template("home.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("title")
    new_todo = Todo(task=task, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo_list"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("todo_list"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo_list"))


with app.app_context():
    db.create_all()
