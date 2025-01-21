// This file contains the JavaScript code for client-side interactions in the todo tracker app.

document.addEventListener('DOMContentLoaded', function() {
    const addTodoForm = document.getElementById('add-todo-form');
    const todoList = document.getElementById('todo-list');

    addTodoForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const title = document.getElementById('todo-title').value;
        const body = document.getElementById('todo-body').value;
        const dueDate = document.getElementById('todo-due-date').value;

        // Add new todo item
        fetch('/todos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, body, due_date: dueDate })
        })
        .then(response => response.json())
        .then(data => {
            // Append new todo item to the list
            const todoItem = document.createElement('li');
            todoItem.textContent = `${data.title} - ${data.body}`;
            todoList.appendChild(todoItem);
            addTodoForm.reset();
        });
    });

    // Function to filter todos by completion status
    document.getElementById('filter-completed').addEventListener('change', function() {
        const showCompleted = this.checked;
        const todos = todoList.getElementsByTagName('li');
        for (let todo of todos) {
            if (showCompleted && !todo.classList.contains('completed')) {
                todo.style.display = 'none';
            } else {
                todo.style.display = 'list-item';
            }
        }
    });

    // Function to sort todos by creation date or due date
    document.getElementById('sort-todos').addEventListener('change', function() {
        const sortBy = this.value;
        const todosArray = Array.from(todoList.getElementsByTagName('li'));
        todosArray.sort((a, b) => {
            const aDate = new Date(a.dataset.creationTime);
            const bDate = new Date(b.dataset.creationTime);
            return sortBy === 'due_date' ? aDate - bDate : bDate - aDate;
        });
        todoList.innerHTML = '';
        todosArray.forEach(todo => todoList.appendChild(todo));
    });
});