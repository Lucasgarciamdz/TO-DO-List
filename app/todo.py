from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="/Users/LucasG/Desktop/itc_soluciones/todo_list/template")
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/")
def todo_list():
    todo_list = Todo.query.all()
    return render_template("home", todo_list=todo_list)


if __name__ == "__main__":
    app.run(debug=True)
