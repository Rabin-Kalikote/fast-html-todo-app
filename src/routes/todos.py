from fasthtml import FastHTML
from flask import Blueprint, request, render_template, redirect, url_for
from ..database.models import TodoItem, db_session

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/todos', methods=['GET'])
def list_todos():
    todos = db_session.query(TodoItem).all()
    return render_template('todo_list.html', todos=todos)

@todos_bp.route('/todos/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    body = request.form.get('body')
    due_date = request.form.get('due_date')
    new_todo = TodoItem(title=title, body=body, due_date=due_date, is_completed=False)
    db_session.add(new_todo)
    db_session.commit()
    return redirect(url_for('todos.list_todos'))

@todos_bp.route('/todos/update/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo = db_session.query(TodoItem).get(todo_id)
    todo.is_completed = not todo.is_completed
    db_session.commit()
    return redirect(url_for('todos.list_todos'))

@todos_bp.route('/todos/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = db_session.query(TodoItem).get(todo_id)
    db_session.delete(todo)
    db_session.commit()
    return redirect(url_for('todos.list_todos'))